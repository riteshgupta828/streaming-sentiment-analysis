# Sample Data Structure

## Input Format
Place raw data in S3 path: `reddit/socialgist-raw/`

Example structure:
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

## Output Format
Results saved to: `sentiment-trend-analyzer/`

_See main README for detailed output schema._
