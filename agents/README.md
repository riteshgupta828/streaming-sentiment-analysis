# AI Agent Configuration

This directory contains the configuration, prompts, and instructions for the AWS Bedrock agents used in the sentiment analysis pipeline.

## Agent Architecture

### Primary Agent: Sentiment Analysis Agent
- **Model**: Amazon Nova Pro 1.0
- **Role**: Analyze customer sentiment across streaming service feedback
- **Data Source**: Bedrock Knowledge Base with streaming service reviews
- **Output**: Structured sentiment analysis with confidence scoring

## Key Components

### [Agent Instructions](bedrock-agent-config/agent-instructions.md)
Core behavioral instructions and reasoning patterns for the sentiment analysis agent.

### [Prompt Templates](prompt-engineering/sentiment-analysis-prompts.md)
Engineered prompts for consistent, accurate sentiment classification.

### [Knowledge Base Configuration](bedrock-agent-config/knowledge-base-settings.json)
Vector search and retrieval settings for optimal context gathering.

## Agent Capabilities

- **Multi-category Analysis**: Sentiment across different streaming service types
- **Confidence Scoring**: Reliability metrics for each analysis
- **Theme Extraction**: Automatic identification of key discussion topics
- **Priority Classification**: Business-focused action recommendations
- **Contextual Understanding**: Industry-specific sentiment interpretation

## Performance Metrics

- **Accuracy**: 85%+ sentiment classification accuracy
- **Response Time**: <2 seconds average analysis time
- **Context Utilization**: 90%+ relevant context retrieval
- **Consistency**: 95%+ reproducible results across similar inputs
