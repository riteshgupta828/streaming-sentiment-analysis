🏗️ Architecture
mermaidgraph TB
    A[Raw Social Media Data] --> B[S3 Raw Storage]
    B --> C[Lambda: Data Cleaner]
    C --> D[S3 Processed Storage]
    D --> E[Lambda: KB Sync]
    E --> F[Bedrock Knowledge Base]
    F --> G[Bedrock Agent - Nova Pro]
    G --> H[Lambda: Sentiment Analyzer]
    H --> I[S3 Results Storage]
    I --> J[QuickSight Dashboard]
    
    style A fill:#e1f5fe
    style J fill:#f3e5f5
    style G fill:#fff3e0
