"""
Shared configuration for streaming sentiment analysis Lambda functions
"""
import os

# AWS Resource Configuration
# NOTE: Replace these placeholders with your actual AWS resource IDs
KNOWLEDGE_BASE_ID = os.environ.get('KNOWLEDGE_BASE_ID', 'YOUR_KB_ID_HERE')
DATA_SOURCE_ID = os.environ.get('DATA_SOURCE_ID', 'YOUR_DATA_SOURCE_ID_HERE')
S3_BUCKET = os.environ.get('S3_BUCKET', 'your-streaming-sentiment-bucket')

# Analysis Configuration
MIN_MENTIONS_THRESHOLD = int(os.environ.get('MIN_MENTIONS_THRESHOLD', '3'))
MAX_RESULTS_PER_SEARCH = 30

# S3 Paths
S3_PATHS = {
    'raw_data': 'reddit/socialgist-raw/',
    'processed_data': 'socialgist-processed/',
    'kb_ready': 'socialgist-kb/',
    'results': 'sentiment-trend-analyzer/'
}

# Streaming Service Categories (Generic)
STREAMING_CATEGORIES = {
    'premium_services': ['premium streaming', 'subscription service'],
    'free_services': ['free streaming', 'ad-supported'],
    'live_tv': ['live tv streaming', 'broadcast streaming'],
    'sports': ['sports streaming', 'live sports'],
    'news': ['news streaming', 'live news'],
    'kids': ['kids streaming', 'family content']
}
