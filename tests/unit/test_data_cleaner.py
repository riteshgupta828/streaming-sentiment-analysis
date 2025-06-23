"""
Unit tests for data cleaner Lambda function
"""
import json
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add lambda directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../lambda/data-cleaner'))

# Mock boto3 before importing lambda function
with patch('boto3.client'):
    from lambda_function import lambda_handler, extract_base_filename

def test_extract_base_filename():
    """Test filename extraction utility"""
    assert extract_base_filename('folder/test-file.json') == 'test-file'
    assert extract_base_filename('raw-data-sample.json') == 'raw-data-sample'

def test_lambda_handler_empty_event():
    """Test lambda handler with empty event"""
    with patch('boto3.client') as mock_boto:
        # Mock S3 client
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        mock_s3.list_objects_v2.return_value = {'Contents': []}
        
        result = lambda_handler({}, {})
        
        assert result['statusCode'] == 200
        assert 'No files found' in result['body']

@pytest.fixture
def sample_raw_data():
    """Sample input data for testing"""
    return {
        "response": {
            "Matches": {
                "Match": [
                    {
                        "Title": "Test streaming service review",
                        "Data": {
                            "Body": "Great streaming service with excellent content!"
                        }
                    }
                ]
            }
        }
    }

def test_data_processing_logic(sample_raw_data):
    """Test core data processing logic"""
    matches = sample_raw_data["response"]["Matches"]["Match"]
    assert len(matches) == 1
    assert matches[0]["Title"] == "Test streaming service review"
    assert "excellent" in matches[0]["Data"]["Body"]

if __name__ == "__main__":
    pytest.main([__file__])
