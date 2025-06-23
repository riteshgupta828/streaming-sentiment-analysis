# QuickSight Dashboard Setup

## Data Source Configuration

### S3 Data Source
```json
{
  "bucket": "your-streaming-sentiment-bucket",
  "key": "sentiment-trend-analyzer/sentiment-trends-quicksight.json",
  "format": "JSON",
  "refresh_schedule": "daily"
}
```
## Key Fields for Visualization
- `property_name`: Streaming service category
- `sentiment_score`: Numerical sentiment (0-100)
- `total_mentions`: Volume of customer feedback
- `trend`: Categorical trend indicator
- `action_required`: Boolean flag for priority items

## Recommended Visualizations
1. Executive Summary (KPI Cards)
- Total mentions analyzed
- Overall portfolio sentiment
- Properties needing attention
- Analysis confidence score

2. Property Performance (Horizontal Bar Chart)
- X-axis: Sentiment score
- Y-axis: Property names
- Color coding by sentiment category

3. Mention Volume vs Sentiment (Scatter Plot)
- X-axis: Total mentions (engagement)
- Y-axis: Sentiment score
- Bubble size: Confidence level

4. Trend Analysis (Line Chart)
- Time series of sentiment changes
- Multiple lines for different properties
- Trend indicators and forecasting

## Filter Controls
* Date range selector
* Property category filter
* Sentiment threshold slider
* Action required toggle
