# Data Cleaner Lambda Function

## Purpose
Processes raw social media data and converts it into clean, structured format for analysis.

## Functionality
- Reads raw JSON files from S3 (`reddit/socialgist-raw/`)
- Removes duplicates and validates data quality
- Outputs cleaned JSON and JSONL files
- Triggers knowledge base synchronization

## Environment Variables
- `S3_BUCKET`: Target S3 bucket name
- `ENVIRONMENT`: Deployment environment (dev/staging/prod)

## Input/Output
- **Input**: Raw social media JSON files
- **Output**: Cleaned data in `socialgist-processed/` and `socialgist-kb/`

## Error Handling
- Continues processing on individual file failures
- Comprehensive logging for troubleshooting
- Graceful handling of malformed data
