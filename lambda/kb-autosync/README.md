# Knowledge Base Auto-Sync Lambda Function

## Purpose
Automatically triggers Bedrock Knowledge Base ingestion when new files are uploaded to S3.

## Functionality
- Triggered by S3 events on `socialgist-kb/` folder
- Handles concurrent ingestion job conflicts with retry logic
- Monitors ingestion job status and completion

## Environment Variables
- `KNOWLEDGE_BASE_ID`: Bedrock Knowledge Base identifier
- `DATA_SOURCE_ID`: Bedrock Data Source identifier

## Features
- Conflict resolution for concurrent KB operations
- Retry mechanism with exponential backoff
- Detailed status reporting and error handling

## Trigger
S3 ObjectCreated events for `*.jsonl` files in `socialgist-kb/` prefix
