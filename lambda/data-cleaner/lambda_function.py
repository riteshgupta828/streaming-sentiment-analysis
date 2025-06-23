# Code to clean raw data from Social Gist json files and save to S3 bucket for use in Knowledge Base.
import json
import boto3
import logging
from datetime import datetime
import os

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def extract_base_filename(s3_key):
    """Extract base filename without path and extension"""
    filename = os.path.basename(s3_key)
    return os.path.splitext(filename)[0]

def process_single_file(bucket, input_key):
    """Process a single JSON file"""
    try:
        logger.info(f"Processing file: {input_key}")
        
        # Extract base filename for output naming
        base_filename = extract_base_filename(input_key)
        timestamp = datetime.utcnow().strftime('%m%d%Y-%H%M%S')
        
        # Define output paths with original filename
        cleaned_key = f'socialgist-processed/clean-{base_filename}.json'
        summary_key = f'socialgist-processed/summary-{base_filename}.json'
        kb_jsonl_key = f'socialgist-kb/ready-{base_filename}.jsonl'
        
        # Load input file
        response = s3.get_object(Bucket=bucket, Key=input_key)
        file_content = response['Body'].read().decode('utf-8')
        raw_data = json.loads(file_content)

        records = raw_data.get("response", {}).get("Matches", {}).get("Match", [])
        logger.info(f"Found {len(records)} records in {input_key}")

        seen = set()
        cleaned = []
        jsonl_lines = []
        skipped_no_title = 0
        skipped_no_body = 0
        duplicates_removed = 0

        for item in records:
            title = item.get("Title")
            body = item.get("Data", {}).get("Body")

            if not title:
                skipped_no_title += 1
                continue
            if not body:
                skipped_no_body += 1
                continue

            fingerprint = f"{title.strip()}::{body.strip()}"

            if fingerprint not in seen:
                seen.add(fingerprint)
                record = {
                    "title": title.strip(),
                    "body": body.strip(),
                    "source_file": input_key,
                    "processed_at": datetime.utcnow().isoformat()
                }
                cleaned.append(record)

                # Add to KB jsonl list
                jsonl_text = f"Title: {record['title']}\nBody: {record['body']}"
                jsonl_lines.append(json.dumps({"text": jsonl_text}))
            else:
                duplicates_removed += 1

        # Save cleaned JSON
        s3.put_object(
            Bucket=bucket,
            Key=cleaned_key,
            Body=json.dumps(cleaned, indent=2),
            ContentType='application/json'
        )

        # Save KB-ready JSONL
        s3.put_object(
            Bucket=bucket,
            Key=kb_jsonl_key,
            Body="\n".join(jsonl_lines),
            ContentType='application/json'
        )

        # Create summary
        summary = {
            'processing_timestamp': timestamp,
            'input_file': f's3://{bucket}/{input_key}',
            'output_file': f's3://{bucket}/{cleaned_key}',
            'kb_jsonl_file': f's3://{bucket}/{kb_jsonl_key}',
            'total_input_records': len(records),
            'cleaned_records': len(cleaned),
            'duplicates_removed': duplicates_removed,
            'skipped_no_title': skipped_no_title,
            'skipped_no_body': skipped_no_body
        }

        # Save summary
        s3.put_object(
            Bucket=bucket,
            Key=summary_key,
            Body=json.dumps(summary, indent=2),
            ContentType='application/json'
        )

        return summary

    except Exception as e:
        logger.error(f"Error processing {input_key}: {str(e)}")
        raise

def lambda_handler(event, context):
    # Configuration
    bucket = 'YOUR S3 BUCKET'
    raw_folder = 'YOUR S3 RAW FOLDER'
    
    try:
        logger.info(f"Starting batch processing from folder: {raw_folder}")
        
        # List all files in the raw folder
        response = s3.list_objects_v2(Bucket=bucket, Prefix=raw_folder)
        
        if 'Contents' not in response:
            logger.warning(f"No files found in {raw_folder}")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': f'No files found in {raw_folder}',
                    'processed_files': 0
                })
            }
        
        # Filter for JSON files only
        json_files = [
            obj['Key'] for obj in response['Contents'] 
            if obj['Key'].lower().endswith('.json') and obj['Key'] != raw_folder
        ]
        
        logger.info(f"Found {len(json_files)} JSON files to process")
        
        processed_summaries = []
        failed_files = []
        
        # Process each file
        for file_key in json_files:
            try:
                summary = process_single_file(bucket, file_key)
                processed_summaries.append(summary)
                logger.info(f"Successfully processed: {file_key}")
            except Exception as e:
                failed_files.append({
                    'file': file_key,
                    'error': str(e)
                })
                logger.error(f"Failed to process {file_key}: {str(e)}")
        
        # Create overall summary
        total_input_records = sum(s['total_input_records'] for s in processed_summaries)
        total_cleaned_records = sum(s['cleaned_records'] for s in processed_summaries)
        
        result = {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Batch processing completed',
                'files_processed': len(processed_summaries),
                'files_failed': len(failed_files),
                'total_input_records': total_input_records,
                'total_cleaned_records': total_cleaned_records,
                'failed_files': failed_files,
                'processed_summaries': processed_summaries
            })
        }
        
        logger.info(f"Batch processing completed: {len(processed_summaries)} successful, {len(failed_files)} failed")
        return result

    except Exception as e:
        logger.error(f"Error during batch processing: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'source_folder': f's3://{bucket}/{raw_folder}'
            })
        }
