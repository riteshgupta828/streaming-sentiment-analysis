# Configuration Notes

## Required AWS Resource IDs

Before deploying this solution, you need to update the following placeholders with your actual AWS resource IDs:

### Knowledge Base Configuration
```bash
# Replace in lambda/sentiment-analyzer/lambda_function.py
KNOWLEDGE_BASE_ID=YOUR_KB_ID_HERE           # Example: VMX5NN4N00
DATA_SOURCE_ID=YOUR_DATA_SOURCE_ID_HERE     # Example: WOLLW07H00
```

### S3 Bucket Names
```bash
# Replace in all Lambda functions and CloudFormation templates
S3_BUCKET=your-streaming-sentiment-bucket   # Must be globally unique
```

### Environment Variables
After deploying infrastructure, update Lambda environment variables:

```bash
aws lambda update-function-configuration \
  --function-name bulk-sentiment-analyzer \
  --environment Variables='{
    "KNOWLEDGE_BASE_ID":"YOUR_ACTUAL_KB_ID",
    "DATA_SOURCE_ID":"YOUR_ACTUAL_DATA_SOURCE_ID",
    "S3_BUCKET":"your-actual-bucket-name",
    "MIN_MENTIONS_THRESHOLD":"3"
  }'
```

## Deployment Steps

### 1. Deploy Infrastructure First
```bash
aws cloudformation deploy \
  --template-file infrastructure/cloudformation/main.yaml \
  --stack-name streaming-sentiment-stack \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    BucketName=your-unique-bucket-name \
    NotificationEmail=your-email@domain.com
```

### 2. Get Resource IDs
```bash
# Get Knowledge Base ID
aws bedrock-agent list-knowledge-bases --query 'knowledgeBaseSummaries[?name==`Streaming-Sentiment-KB-development`].knowledgeBaseId' --output text

# Get Data Source ID  
aws bedrock-agent list-data-sources \
  --knowledge-base-id YOUR_KB_ID \
  --query 'dataSourceSummaries[0].dataSourceId' \
  --output text
```

### 3. Update Lambda Code
Replace placeholder values in lambda functions with actual resource IDs before deployment.

### 4. Deploy Lambda Functions
```bash
# Package and deploy each function
./scripts/deployment/package-lambdas.sh
```

## Sample Data Structure

### Input Data Format (S3: socialgist-raw/)
```json
{
  "response": {
    "Matches": {
      "Match": [
        {
          "Title": "Streaming service review",
          "Data": {
            "Body": "Customer feedback content here..."
          }
        }
      ]
    }
  }
}
```

### Output Data Format (S3: sentiment-trend-analyzer/)
```json
{
  "analysis_metadata": {
    "analysis_timestamp": "2025-06-12T10:30:00Z",
    "total_properties_analyzed": 15,
    "streaming_focus": true
  },
  "results": [
    {
      "topic": "Premium Streaming Service",
      "sentiment_trend": "positive",
      "total_mentions": 245,
      "confidence_score": 85.2
    }
  ]
}
```

## Security Considerations

### IAM Permissions
Ensure Lambda execution roles have minimum required permissions:
- S3: GetObject, PutObject on specific bucket
- Bedrock: InvokeModel, Retrieve on specific KB
- CloudWatch: CreateLogGroup, PutLogEvents

### Data Privacy
- No personally identifiable information (PII) stored
- All data processing occurs within your AWS account
- S3 encryption enabled by default

## Cost Optimization

### Expected Monthly Costs (Development)
- Lambda executions: $2-5
- S3 storage: $1-3  
- Bedrock API calls: $10-20
- CloudWatch logs: $1-2
- **Total: ~$15-30/month**

### Cost Monitoring
- CloudWatch cost alarms configured
- S3 lifecycle policies for old data
- Lambda timeout limits to prevent runaway costs

## Troubleshooting

### Common Issues
1. **Knowledge Base Access Denied**: Verify Bedrock model access enabled
2. **S3 Permissions**: Check IAM roles have correct bucket permissions
3. **Lambda Timeout**: Increase memory and timeout for large datasets

### Debugging Commands
```bash
# Check Lambda logs
aws logs tail /aws/lambda/bulk-sentiment-analyzer --follow

# Verify S3 structure
aws s3 ls s3://your-bucket/ --recursive

# Test Knowledge Base access
aws bedrock-agent retrieve \
  --knowledge-base-id YOUR_KB_ID \
  --retrieval-query text="streaming service"
```

## Support

For issues or questions:
1. Check CloudWatch logs for detailed error messages
2. Verify all placeholder values have been replaced
3. Ensure AWS CLI is configured with proper permissions
4. Review the troubleshooting guide in docs/troubleshooting.md
