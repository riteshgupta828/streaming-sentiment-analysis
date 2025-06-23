# Response Formatting Standards

## JSON Schema Standards

### Primary Analysis Response Format
```json
{
  "analysis_metadata": {
    "analysis_id": "uuid",
    "timestamp": "ISO-8601",
    "agent_version": "string",
    "processing_time_ms": "number",
    "confidence_threshold_met": "boolean"
  },
  "streaming_service_analysis": {
    "service_category": "string",
    "sentiment_classification": {
      "overall_score": "number (0-100)",
      "sentiment_label": "string (positive/negative/neutral/mixed)",
      "confidence_level": "number (0-100)",
      "score_breakdown": {
        "positive_indicators": "number",
        "negative_indicators": "number", 
        "neutral_indicators": "number",
        "weighted_score": "number"
      }
    },
    "mention_analytics": {
      "total_mentions": "number",
      "unique_sources": "number",
      "date_range": {
        "earliest": "date",
        "latest": "date"
      },
      "geographic_distribution": "object",
      "demographic_insights": "object"
    },
    "theme_analysis": [
      {
        "theme_name": "string",
        "theme_sentiment": "number (0-100)",
        "mention_count": "number",
        "relevance_score": "number (0-10)",
        "business_impact": "string (high/medium/low)",
        "supporting_quotes": ["array of strings"],
        "trend_direction": "string (improving/declining/stable)"
      }
    ],
    "business_intelligence": {
      "priority_level": "string (high/medium/low)",
      "action_required": "boolean",
      "urgency_score": "number (1-10)",
      "estimated_customer_impact": "number",
      "revenue_implications": "string",
      "competitive_positioning": "string"
    },
    "recommendations": {
      "immediate_actions": [
        {
          "action": "string",
          "priority": "number (1-10)",
          "estimated_effort": "string (low/medium/high)",
          "expected_impact": "string",
          "timeline": "string",
          "owner": "string (department/role)"
        }
      ],
      "strategic_initiatives": [
        {
          "initiative": "string",
          "business_case": "string",
          "resource_requirements": "string",
          "success_metrics": ["array of strings"],
          "timeline": "string"
        }
      ]
    },
    "quality_indicators": {
      "data_sufficiency": "string (excellent/good/fair/poor)",
      "analysis_reliability": "number (0-100)",
      "recommendation_confidence": "number (0-100)",
      "requires_human_review": "boolean",
      "validation_notes": "string"
    }
  }
}
```
## Executive Summary Format

### Dashboard Summary Template
```json
{
  "executive_summary": {
    "portfolio_overview": {
      "total_properties_analyzed": "number",
      "overall_portfolio_sentiment": "number (0-100)", 
      "total_customer_mentions": "number",
      "analysis_period": "string",
      "confidence_level": "number (0-100)"
    },
    "key_insights": [
      {
        "insight_type": "string (opportunity/risk/trend)",
        "description": "string",
        "business_impact": "string (high/medium/low)",
        "supporting_data": "string"
      }
    ],
    "critical_alerts": [
      {
        "alert_level": "string (urgent/high/medium)",
        "service_affected": "string",
        "issue_description": "string",
        "customer_impact": "string",
        "recommended_response": "string",
        "timeline": "string"
      }
    ],
    "performance_highlights": {
      "top_performing_services": ["array of objects"],
      "improvement_opportunities": ["array of objects"],
      "competitive_advantages": ["array of strings"],
      "market_positioning": "string"
    },
    "strategic_recommendations": {
      "next_30_days": ["array of actions"],
      "next_90_days": ["array of initiatives"], 
      "long_term_strategy": ["array of strategic moves"]
    }
  }
}
```
## Error Handling Formats

### Insufficient Data Response
```json
{
  "analysis_status": "insufficient_data",
  "error_details": {
    "data_volume": "number",
    "minimum_required": "number",
    "confidence_impact": "string",
    "recommendations": [
      "Collect additional feedback data",
      "Extend analysis time period", 
      "Broaden search criteria",
      "Consider qualitative research supplement"
    ]
  },
  "partial_analysis": {
    "available_insights": "object",
    "reliability_warnings": ["array of strings"],
    "suggested_next_steps": ["array of strings"]
  }
}
```
### Conflicting Data Response
```json
{
  "analysis_status": "conflicting_signals",
  "conflict_details": {
    "conflict_type": "string",
    "conflicting_themes": ["array of themes"],
    "data_splits": "object",
    "possible_explanations": ["array of strings"]
  },
  "multiple_scenarios": [
    {
      "scenario_name": "string",
      "probability": "number (0-100)",
      "sentiment_outcome": "object",
      "business_implications": "string",
      "validation_approach": "string"
    }
  ],
  "recommended_approach": "string"
}
```
## Confidence Indicators
HIGH CONFIDENCE (90-100%):
- ✅ Large sample size (>500 mentions)
- ✅ Consistent sentiment patterns
- ✅ Recent data (last 30 days)
- ✅ Multiple source validation
- ✅ Clear business themes

MEDIUM CONFIDENCE (70-89%):
- ⚠️ Moderate sample size (100-500 mentions)
- ⚠️ Some sentiment variation
- ⚠️ Mixed timeframe data
- ⚠️ Limited source diversity
- ⚠️ Emerging themes

LOW CONFIDENCE (0-69%):
- ❌ Small sample size (<100 mentions)
- ❌ Inconsistent patterns
- ❌ Outdated data (>90 days)
- ❌ Single source dependency
- ❌ Unclear themes

## Validation Requirements
BUSINESS VALIDATION:
- Strategic alignment with company goals
- Resource feasibility assessment
- ROI potential evaluation
- Competitive impact analysis
- Customer value consideration

TECHNICAL VALIDATION:
- Data quality verification
- Algorithm performance check
- Bias detection and mitigation
- Reproducibility confirmation
- Error rate assessment

STAKEHOLDER VALIDATION:
- Executive leadership review
- Product team alignment
- Customer success validation
- Marketing strategy consistency
- Operations feasibility check
