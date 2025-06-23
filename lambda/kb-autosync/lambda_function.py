# Code to ingest data from S3 bucket to Bedrock Knowledge Base with conflict handling
import json
import boto3
import logging
import uuid
import time
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock = boto3.client("bedrock-agent")

# Configuration
KB_ID = "YOUR KNOWLEDGEBASE ID"
DATA_SOURCE_ID = "YOUR SOURCE ID"
MAX_RETRIES = 3
RETRY_DELAY = 30  # seconds
WAIT_FOR_COMPLETION = False  # Set to True if you want to wait for job completion

def check_existing_jobs(kb_id):
    """Check if there are any running ingestion jobs"""
    try:
        response = bedrock.list_ingestion_jobs(
            knowledgeBaseId=kb_id,
            dataSourceId=DATA_SOURCE_ID,
            maxResults=10
        )
        
        running_jobs = [
            job for job in response.get('ingestionJobSummaries', [])
            if job['status'] in ['STARTING', 'IN_PROGRESS']
        ]
        
        logger.info(f"Found {len(running_jobs)} running ingestion jobs")
        return running_jobs
    
    except Exception as e:
        logger.error(f"Error checking existing jobs: {str(e)}")
        return []

def wait_for_job_completion(kb_id, job_id, timeout=300):
    """Wait for ingestion job to complete (optional)"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = bedrock.get_ingestion_job(
                knowledgeBaseId=kb_id,
                dataSourceId=DATA_SOURCE_ID,
                ingestionJobId=job_id
            )
            
            status = response['ingestionJob']['status']
            logger.info(f"Job {job_id} status: {status}")
            
            if status in ['COMPLETE', 'FAILED']:
                return status
            
            time.sleep(10)  # Check every 10 seconds
            
        except Exception as e:
            logger.error(f"Error checking job status: {str(e)}")
            break
    
    logger.warning(f"Job {job_id} did not complete within {timeout} seconds")
    return "TIMEOUT"

def start_ingestion_with_retry(kb_id, data_source_id, s3_key):
    """Start ingestion job with retry logic for conflicts"""
    
    for attempt in range(MAX_RETRIES):
        try:
            # Check for existing jobs first
            running_jobs = check_existing_jobs(kb_id)
            
            if running_jobs:
                logger.info(f"Attempt {attempt + 1}: Found {len(running_jobs)} running jobs")
                
                if attempt < MAX_RETRIES - 1:  # Not the last attempt
                    logger.info(f"Waiting {RETRY_DELAY} seconds before retry...")
                    time.sleep(RETRY_DELAY)
                    continue
                else:
                    logger.warning("Max retries reached. Existing job still running.")
                    return {
                        'success': False,
                        'reason': 'max_retries_exceeded',
                        'running_jobs': len(running_jobs)
                    }
            
            # Try to start the ingestion job
            logger.info(f"Attempt {attempt + 1}: Starting ingestion job for {s3_key}")
            
            response = bedrock.start_ingestion_job(
                knowledgeBaseId=kb_id,
                dataSourceId=data_source_id,
                clientToken=str(uuid.uuid4()),
                description=f"Auto-ingestion triggered by S3 upload: {s3_key}"
            )
            
            job_id = response['ingestionJob']['ingestionJobId']
            logger.info(f"Successfully started ingestion job: {job_id}")
            
            # Optionally wait for completion
            if WAIT_FOR_COMPLETION:
                final_status = wait_for_job_completion(kb_id, job_id)
                logger.info(f"Job {job_id} completed with status: {final_status}")
            
            return {
                'success': True,
                'job_id': job_id,
                'response': response['ingestionJob']
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == 'ConflictException':
                logger.warning(f"Attempt {attempt + 1}: ConflictException - KB already in use")
                
                if attempt < MAX_RETRIES - 1:
                    logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                    continue
                else:
                    logger.error("Max retries exceeded due to ConflictException")
                    return {
                        'success': False,
                        'reason': 'conflict_exception',
                        'error': str(e)
                    }
            else:
                logger.error(f"Unexpected AWS error: {error_code} - {str(e)}")
                return {
                    'success': False,
                    'reason': 'aws_error',
                    'error': str(e)
                }
                
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {str(e)}")
            return {
                'success': False,
                'reason': 'unexpected_error',
                'error': str(e)
            }
    
    return {
        'success': False,
        'reason': 'max_retries_exceeded'
    }

def lambda_handler(event, context):
    try:
        processed_files = []
        skipped_files = []
        
        # Handle manual testing vs actual S3 events
        if "Records" not in event:
            logger.warning("No 'Records' found in event - this appears to be a manual test")
            logger.info(f"Event received: {json.dumps(event, indent=2)}")
            
            # For manual testing, create a mock record
            test_file = event.get('test_file', 'socialgist-kb/test-file.jsonl')
            logger.info(f"Manual test mode - processing file: {test_file}")
            
            result = start_ingestion_with_retry(KB_ID, DATA_SOURCE_ID, test_file)
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Manual test completed",
                    "test_file": test_file,
                    "result": result
                })
            }
        
        for record in event["Records"]:
            s3_bucket = record["s3"]["bucket"]["name"]
            s3_key = record["s3"]["object"]["key"]
            event_name = record["eventName"]
            
            logger.info(f"Processing S3 event: {event_name} for {s3_key}")

            # Trigger only for content added to the KB folder
            if s3_key.startswith("socialgist-kb/") and s3_key.endswith(".jsonl"):
                logger.info(f"Valid KB file detected: {s3_key}")
                
                # Start ingestion with retry logic
                result = start_ingestion_with_retry(KB_ID, DATA_SOURCE_ID, s3_key)
                
                if result['success']:
                    processed_files.append({
                        'file': s3_key,
                        'job_id': result['job_id'],
                        'status': 'started'
                    })
                else:
                    processed_files.append({
                        'file': s3_key,
                        'status': 'failed',
                        'reason': result['reason'],
                        'error': result.get('error', 'Unknown error')
                    })
            else:
                logger.info(f"Skipping file - does not match KB pattern: {s3_key}")
                skipped_files.append(s3_key)

        # Summary response
        response_body = {
            "message": "S3 event processing completed",
            "processed_files": processed_files,
            "skipped_files": skipped_files,
            "total_processed": len(processed_files),
            "total_skipped": len(skipped_files)
        }

        logger.info(f"Processing summary: {json.dumps(response_body, indent=2)}")

        return {
            "statusCode": 200,
            "body": json.dumps(response_body)
        }

    except Exception as e:
        logger.error(f"Lambda handler error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "message": "Failed to process S3 event"
            })
        }
