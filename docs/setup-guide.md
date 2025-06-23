# Complete Setup Guide

## Prerequisites

### AWS Account Requirements
- **AWS Account** with administrator access
- **AWS Bedrock** access in your region (us-east-1 recommended)
- **Service Quotas** verified for:
  - Lambda concurrent executions (100+)
  - S3 storage (no specific limit needed)
  - Bedrock model access (Nova Pro 1.0)

### Local Development Environment
- **Python 3.9+** installed
- **AWS CLI v2** configured with credentials
- **Git** for version control
- **Code Editor** (VS Code recommended)

### Estimated Costs
- **Development**: $5-10/month
- **Production**: $20-50/month (varies by data volume)

## Step 1: Repository Setup

### Clone and Initialize
```bash
# Clone the repository
git clone https://github.com/yourusername/wbd-sentiment-analysis.git
cd wbd-sentiment-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
```

### Configure AWS CLI
```bash
# Configure AWS credentials
aws configure
# AWS Access Key ID: [Your Access Key]
# AWS Secret Access Key: [Your Secret Key]
# Default region name: us-east-1
# Default output format: json

# Verify access
aws sts get-caller-identity
```

## Step 2: AWS Infrastructure Setup

### Option A: CloudFormation (Recommended)
```bash
# Deploy infrastructure stack
aws cloudformation deploy \
  --template-file infrastructure/cloudformation/main.yaml \
  --stack-name wbd-sentiment-stack \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    Environment=development \
    BucketName=your-unique-bucket-name

# Verify deployment
aws cloudformation describe-stacks --stack-name wbd-sentiment-stack
```

### Option B: Terraform
```bash
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var="environment=development"

# Apply infrastructure
terraform apply -var="environment=development"
```

### Manual Setup (If needed)
```bash
# Create S3 bucket
aws s3 mb s3://your-social-media-knowledge-base

# Enable S3 event notifications
aws s3api put-bucket-notification-configuration \
  --bucket your-social-media-knowledge-base \
  --notification-configuration file://config/s3-notifications.json
```

## Step 3: Bedrock Configuration

### Enable Model Access
```bash
# List available models
aws bedrock list-foundation-models --region us-east-1

# Request model access (if needed)
aws bedrock put-model-invocation-logging-configuration \
  --logging-config cloudWatchConfig='{logGroupName=/aws/bedrock/modelinvocations,roleArn=arn:aws:iam::ACCOUNT:role/BedrockLoggingRole}'
```

### Create Knowledge Base
```bash
# Create knowledge base
aws bedrock-agent create-knowledge-base \
  --name "WBD-Sentiment-KB" \
  --role-arn "arn:aws:iam::ACCOUNT:role/BedrockKBRole" \
  --knowledge-base-configuration '{
    "type": "VECTOR",
    "vectorKnowledgeBaseConfiguration": {
      "embeddingModelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
    }
  }' \
  --storage-configuration '{
    "type": "OPENSEARCH_SERVERLESS",
    "opensearchServerlessConfiguration": {
      "collectionArn": "arn:aws:aoss:us-east-1:ACCOUNT:collection/wbd-sentiment-collection",
      "vectorIndexName": "wbd-sentiment-index",
      "fieldMapping": {
        "vectorField": "vector",
        "textField": "text",
        "metadataField": "metadata"
      }
    }
  }'
```

## Step 4: Lambda Function Deployment

### Package Functions
```bash
# Run the packaging script
./scripts/deployment/package-lambdas.sh

# This will create deployment packages for:
# - lambda/data-cleaner/deployment.zip
# - lambda/kb-autosync/deployment.zip
# - lambda/sentiment-analyzer/deployment.zip
```

### Deploy Functions
```bash
# Deploy data cleaner
aws lambda create-function \
  --function-name SGJsonExtractor-RawtoClean \
  --runtime python3.9 \
  --role arn:aws:iam::ACCOUNT:role/LambdaExecutionRole \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda/data-cleaner/deployment.zip \
  --timeout 300 \
  --memory-size 512

# Deploy KB auto-sync
aws lambda create-function \
  --function-name KB-AutoSync-OnS3Upload \
  --runtime python3.9 \
  --role arn:aws:iam::ACCOUNT:role/LambdaExecutionRole \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda/kb-autosync/deployment.zip \
  --timeout 60 \
  --memory-size 256

# Deploy sentiment analyzer
aws lambda create-function \
  --function-name bulk-sentiment-analyzer \
  --runtime python3.9 \
  --role arn:aws:iam::ACCOUNT:role/LambdaExecutionRole \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda/sentiment-analyzer/deployment.zip \
  --timeout 900 \
  --memory-size 1024
```

### Configure Environment Variables
```bash
# Set environment variables for each function
aws lambda update-function-configuration \
  --function-name bulk-sentiment-analyzer \
  --environment Variables='{
    "KNOWLEDGE_BASE_ID":"VMX5NN4NTA",
    "S3_BUCKET":"your-social-media-knowledge-base",
    "MIN_MENTIONS_THRESHOLD":"3"
  }'
```

## Step 5: S3 Bucket Configuration

### Create Directory Structure
```bash
# Create required S3 folders
aws s3api put-object --bucket your-social-media-knowledge-base --key reddit/socialgist-raw/
aws s3api put-object --bucket your-social-media-knowledge-base --key socialgist-processed/
aws s3api put-object --bucket your-social-media-knowledge-base --key socialgist-kb/
aws s3api put-object --bucket your-social-media-knowledge-base --key sentiment-trend-analyzer/
```

### Upload Sample Data
```bash
# Upload sample data for testing
./scripts/data/upload-sample-data.sh
```

## Step 6: Testing the Pipeline

### Unit Tests
```bash
# Run unit tests
cd tests
python -m pytest unit/ -v

# Run specific test
python -m pytest unit/test_data_cleaner.py::test_process_single_file -v
```

### Integration Tests
```bash
# Test end-to-end pipeline
python tests/integration/test_end_to_end.py

# Manual trigger test
aws lambda invoke \
  --function-name SGJsonExtractor-RawtoClean \
  --payload '{}' \
  response.json && cat response.json
```

## Step 7: QuickSight Dashboard Setup

### Prerequisites
- QuickSight account activated
- Permissions to read from S3 bucket

### Create Data Source
1. **Login to QuickSight Console**
2. **Navigate to Datasets** → New dataset
3. **Select S3** as data source
4. **Configure S3 connection**:
   - **Data source name**: WBD Sentiment Analysis
   - **S3 bucket**: your-social-media-knowledge-base
   - **Key**: sentiment-trend-analyzer/sentiment-trends-quicksight.json

### Import Dashboard Template
```bash
# Download dashboard template
aws quicksight describe-template \
  --aws-account-id ACCOUNT-ID \
  --template-id wbd-sentiment-template \
  --output json > dashboard-template.json

# Create dashboard from template
aws quicksight create-dashboard \
  --aws-account-id ACCOUNT-ID \
  --dashboard-id wbd-sentiment-dashboard \
  --name "WBD Sentiment Analysis Dashboard" \
  --source-entity TemplateSourceEntity='{
    "SourceTemplate": {
      "DataSetReferences": [...],
      "Arn": "arn:aws:quicksight:us-east-1:ACCOUNT:template/wbd-sentiment-template"
    }
  }'
```

## Step 8: Monitoring & Logging

### CloudWatch Setup
```bash
# Create log groups
aws logs create-log-group --log-group-name /aws/lambda/SGJsonExtractor-RawtoClean
aws logs create-log-group --log-group-name /aws/lambda/KB-AutoSync-OnS3Upload
aws logs create-log-group --log-group-name /aws/lambda/bulk-sentiment-analyzer

# Set retention policy
aws logs put-retention-policy \
  --log-group-name /aws/lambda/bulk-sentiment-analyzer \
  --retention-in-days 14
```

### Create Alarms
```bash
# Lambda error alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "WBD-Lambda-Errors" \
  --alarm-description "Lambda function errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 1
```

## Step 9: Verification & Validation

### System Health Check
```bash
# Run health check script
python scripts/monitoring/health-check.py

# Expected output:
# ✅ S3 bucket accessible
# ✅ Lambda functions deployed
# ✅ Bedrock knowledge base ready
# ✅ QuickSight dashboard configured
```

### Data Flow Test
```bash
# Upload test data
aws s3 cp sample-data/input/raw-socialgist-hbo.json \
  s3://your-social-media-knowledge-base/reddit/socialgist-raw/

# Monitor processing
aws logs tail /aws/lambda/SGJsonExtractor-RawtoClean --follow

# Verify processed files
aws s3 ls s3://your-social-media-knowledge-base/socialgist-processed/
aws s3 ls s3://your-social-media-knowledge-base/socialgist-kb/

# Run sentiment analysis
aws lambda invoke \
  --function-name bulk-sentiment-analyzer \
  --payload '{}' \
  sentiment-response.json

# Check results
aws s3 cp s3://your-social-media-knowledge-base/sentiment-trend-analyzer/sentiment-trends.json ./
```

### Performance Validation
```bash
# Test with larger dataset
python tests/load/test_performance.py --records 1000

# Monitor costs
python scripts/monitoring/monitor-costs.py --start-date 2025-06-01
```

## Step 10: Production Readiness

### Security Hardening
```bash
# Enable S3 encryption
aws s3api put-bucket-encryption \
  --bucket your-social-media-knowledge-base \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Enable CloudTrail logging
aws cloudtrail create-trail \
  --name wbd-sentiment-trail \
  --s3-bucket-name your-cloudtrail-bucket
```

### Backup Strategy
```bash
# Enable S3 versioning
aws s3api put-bucket-versioning \
  --bucket your-social-media-knowledge-base \
  --versioning-configuration Status=Enabled

# Set lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket your-social-media-knowledge-base \
  --lifecycle-configuration file://config/s3-lifecycle.json
```

### Cost Optimization
```bash
# Set up cost budgets
aws budgets create-budget \
  --account-id ACCOUNT-ID \
  --budget '{
    "BudgetName": "WBD-Sentiment-Monthly",
    "BudgetLimit": {
      "Amount": "50",
      "Unit": "USD"
    },
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST"
  }'
```

## Troubleshooting

### Common Issues

#### 1. Bedrock Access Denied
```bash
# Check model access
aws bedrock list-foundation-models --region us-east-1

# Request access if needed
# Navigate to AWS Console → Bedrock → Model access
```

#### 2. Lambda Timeout Errors
```bash
# Increase timeout
aws lambda update-function-configuration \
  --function-name bulk-sentiment-analyzer \
  --timeout 900

# Increase memory
aws lambda update-function-configuration \
  --function-name bulk-sentiment-analyzer \
  --memory-size 1024
```

#### 3. S3 Permissions Issues
```bash
# Check bucket policy
aws s3api get-bucket-policy --bucket your-social-media-knowledge-base

# Update IAM role permissions
aws iam attach-role-policy \
  --role-name LambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```

#### 4. Knowledge Base Sync Failures
```bash
# Check ingestion job status
aws bedrock-agent list-ingestion-jobs \
  --knowledge-base-id VMX5NN4NTA \
  --data-source-id WOLLW07HOG

# Check CloudWatch logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/KB-AutoSync-OnS3Upload \
  --start-time $(date -d '1 hour ago' +%s)000
```

### Getting Help

#### Log Analysis
```bash
# Real-time log monitoring
aws logs tail /aws/lambda/bulk-sentiment-analyzer --follow

# Search for errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/bulk-sentiment-analyzer \
  --filter-pattern "ERROR"
```

#### Performance Monitoring
```bash
# Check Lambda metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=bulk-sentiment-analyzer \
  --start-time $(date -d '1 hour ago' -u +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average,Maximum
```

## Next Steps

### Development Workflow
1. **Create Feature Branch**: `git checkout -b feature/new-enhancement`
2. **Make Changes**: Update code and tests
3. **Test Locally**: Run unit and integration tests
4. **Deploy to Dev**: Use CI/CD pipeline or manual deployment
5. **Validate**: Test end-to-end functionality
6. **Create PR**: Submit for code review
7. **Deploy to Prod**: Merge and auto-deploy

### Enhancement Ideas
- **Real-time Processing**: Add Kinesis for streaming data
- **Advanced Analytics**: Integrate with SageMaker for ML models
- **Multi-Region**: Deploy across multiple AWS regions
- **API Gateway**: Add REST API for external integrations
- **Notification System**: Add SNS/SQS for alerts

### Maintenance Tasks
- **Weekly**: Review CloudWatch metrics and costs
- **Monthly**: Update security patches and dependencies
- **Quarterly**: Review and optimize infrastructure costs
- **Annually**: Conduct security audit and architecture review

## Support

### Documentation Resources
- **AWS Bedrock Documentation**: https://docs.aws.amazon.com/bedrock/
- **Lambda Best Practices**: https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html
- **QuickSight User Guide**: https://docs.aws.amazon.com/quicksight/

### Community Support
- **GitHub Issues**: Submit bugs and feature requests
- **AWS Forums**: Get help from AWS community
- **Stack Overflow**: Tag questions with `aws-bedrock`, `aws-lambda`

### Professional Support
- **AWS Support**: Technical support plans available
- **AWS Professional Services**: Architecture and implementation help
- **Partner Network**: Certified AWS consulting partners

---

**🎉 Congratulations!** Your WBD Sentiment Analysis Platform is now ready for production use. Monitor the system closely during the first few days and adjust configurations as needed based on actual usage patterns.
