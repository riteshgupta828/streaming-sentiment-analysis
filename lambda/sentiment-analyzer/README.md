# Bulk Sentiment Analyzer Lambda Function

## Purpose
Analyzes customer sentiment across streaming service properties and generates business intelligence reports.

## Functionality
- Retrieves data from Bedrock Knowledge Base
- Performs weighted keyword-based sentiment analysis
- Groups feedback by streaming service categories
- Generates QuickSight-ready output with confidence scoring

## Environment Variables
- `KNOWLEDGE_BASE_ID`: Bedrock Knowledge Base ID
- `S3_BUCKET`: Output bucket for results
- `MIN_MENTIONS_THRESHOLD`: Minimum mentions to include property (default: 3)

## Output
- Comprehensive sentiment analysis in JSON format
- QuickSight-optimized flat data structure
- Executive summary with actionable insights
- Confidence scoring and priority levels

## Business Value
- Identifies trending sentiment across streaming portfolio
- Prioritizes properties requiring immediate attention
- Provides data-driven insights for strategic decisions
