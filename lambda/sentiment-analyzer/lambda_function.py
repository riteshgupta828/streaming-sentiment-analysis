def generate_executive_summary(results):
    """
    Enhanced executive summary for business stakeholders
    """
    if not results:
        return "No streaming properties analyzed - insufficient data in Knowledge Base."
    
    total_mentions = sum(r['total_mentions'] for r in results)
    total_properties = len(results)
    
    # Business insights
    high_priority = [r for r in results if 'Action Needed' in r.get('priority_level', '')]
    positive_trending = [# Enhanced Streaming Service Bulk Sentiment Analyzer with QuickSight optimizations
import json
import boto3
import re
from collections import defaultdict
import datetime
from typing import Dict, List
import uuid
import os

def lambda_handler(event, context):
    """
    Enhanced Lambda function for streaming service sentiment analysis
    Optimized for QuickSight dashboard consumption
    """
    print("🚀 Starting Streaming Service Bulk Sentiment Analysis (Enhanced Edition)...")
    
    # Initialize clients
    bedrock_agent_client = boto3.client('bedrock-agent-runtime')
    s3_client = boto3.client('s3')
    
    # Configuration from environment variables
    config = {
        'knowledge_base_id': os.environ.get('KNOWLEDGE_BASE_ID', 'YOUR_KB_ID_HERE'),
        's3_bucket': os.environ.get('S3_BUCKET', 'your-streaming-sentiment-bucket'),
        's3_output_key': 'sentiment-trend-analyzer/sentiment-trends.json',
        'min_mentions_threshold': int(os.environ.get('MIN_MENTIONS_THRESHOLD', '3')),
        'max_results_per_search': 30  # Increased for better coverage
    }
    
    try:
        # Step 1: Get all feedback data from Knowledge Base
        print("📥 Step 1: Retrieving feedback data from Knowledge Base...")
        all_feedback_data = get_streaming_feedback_data(bedrock_agent_client, config)
        print(f"✅ Retrieved {len(all_feedback_data)} feedback records")
        
        if not all_feedback_data:
            return create_response(400, {'error': 'No data retrieved from Knowledge Base'})
        
        # Step 2: Group by streaming properties
        print("🏷️  Step 2: Grouping feedback by streaming properties...")
        streaming_property_groups = group_by_streaming_properties(all_feedback_data, config['min_mentions_threshold'])
        print(f"✅ Found {len(streaming_property_groups)} streaming properties: {list(streaming_property_groups.keys())}")
        
        # Step 3: Analyze each streaming property
        print("📊 Step 3: Analyzing sentiment for each property...")
        analysis_results = []
        
        for i, (property_name, feedback_texts) in enumerate(streaming_property_groups.items(), 1):
            print(f"   Processing {i}/{len(streaming_property_groups)}: {property_name} ({len(feedback_texts)} mentions)")
            
            try:
                result = analyze_streaming_property_sentiment(property_name, feedback_texts)
                analysis_results.append(result)
                print(f"   ✅ {property_name}: {result['sentiment_trend']} ({result['total_mentions']} mentions)")
                
            except Exception as e:
                print(f"   ❌ Error analyzing {property_name}: {str(e)}")
                continue
        
        # Step 4: Sort and enhance results
        analysis_results.sort(key=lambda x: x['total_mentions'], reverse=True)
        
        # Add ranking for QuickSight
        for i, result in enumerate(analysis_results, 1):
            result['ranking_by_mentions'] = i
            result['market_share_percentage'] = round((result['total_mentions'] / sum(r['total_mentions'] for r in analysis_results)) * 100, 2)
        
        # Step 5: Save to S3 with enhanced structure
        print("💾 Step 4: Saving results to S3...")
        save_results_to_s3(s3_client, analysis_results, config)
        
        # Generate summary
        summary = generate_executive_summary(analysis_results)
        
        print(f"🎉 Successfully analyzed {len(analysis_results)} WBD properties!")
        if analysis_results:
            print(f"📈 Top property: {analysis_results[0]['topic']} with {analysis_results[0]['total_mentions']} mentions")
        
        return create_response(200, {
            'message': f'Streaming service sentiment analysis completed successfully',
            'properties_analyzed': len(analysis_results),
            'total_feedback_entries': len(all_feedback_data),
            's3_location': f"s3://{config['s3_bucket']}/{config['s3_output_key']}",
            'top_properties': [r['topic'] for r in analysis_results[:5]],
            'executive_summary': summary,
            'analysis_timestamp': datetime.datetime.now().isoformat(),
            'quicksight_ready': True
        })
        
    except Exception as e:
        print(f"💥 Critical error: {str(e)}")
        return create_response(500, {'error': str(e), 'timestamp': datetime.datetime.now().isoformat()})

def get_streaming_feedback_data(bedrock_agent_client, config):
    """
    Enhanced data retrieval with better error handling and coverage
    """
    all_data = []
    
    # Generic streaming service search terms (no specific brand references)
    streaming_search_terms = [
        # Core streaming services (high priority)
        'streaming service reviews', 'video streaming platform', 'subscription streaming',
        'on demand content', 'streaming app feedback',
        
        # Content categories (medium priority)
        'original series streaming', 'movie streaming service', 'live TV streaming',
        'sports streaming platform', 'news streaming service',
        
        # Technical aspects (lower priority but comprehensive)
        'streaming quality issues', 'buffering problems', 'app crashes',
        'streaming device compatibility', 'streaming subscription cost',
        
        # General streaming sentiment
        'cord cutting experience', 'streaming vs cable', 
        'streaming platform comparison', 'binge watching experience'
    ]
    
    successful_searches = 0
    failed_searches = 0
    
    try:
        for search_term in streaming_search_terms:
            try:
                response = bedrock_agent_client.retrieve(
                    knowledgeBaseId=config['knowledge_base_id'],
                    retrievalQuery={'text': search_term},
                    retrievalConfiguration={
                        'vectorSearchConfiguration': {
                            'numberOfResults': config['max_results_per_search']
                        }
                    }
                )
                
                for result in response['retrievalResults']:
                    content = result['content']['text']
                    # Enhanced metadata
                    all_data.append({
                        'content': content,
                        'relevance_score': result.get('score', 0),
                        'search_term': search_term,
                        'content_length': len(content),
                        'retrieved_at': datetime.datetime.now().isoformat()
                    })
                
                successful_searches += 1
                print(f"   📥 '{search_term}': {len(response['retrievalResults'])} results")
                
            except Exception as e:
                failed_searches += 1
                print(f"   ⚠️  Search term '{search_term}' failed: {str(e)}")
                continue
        
        print(f"📊 Search summary: {successful_searches} successful, {failed_searches} failed")
        
        # Enhanced deduplication
        unique_data = []
        seen_content = set()
        
        for item in all_data:
            # Use longer hash for better deduplication
            content_hash = hash(item['content'][:500])
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_data.append(item)
        
        print(f"📊 Deduplication: {len(all_data)} -> {len(unique_data)} unique entries")
        return unique_data
        
    except Exception as e:
        print(f"❌ Critical error in data retrieval: {str(e)}")
        return []

def group_by_streaming_properties(feedback_data, min_mentions_threshold=3):
    """
    Enhanced property grouping with better categorization for generic streaming services
    """
    # Generic streaming properties mapping (no specific brand names)
    streaming_properties = {
        # Tier 1: Major Streaming Categories
        'Premium Streaming Service': ['premium streaming', 'subscription service', 'streaming platform', 'video service'],
        'Movie Streaming Platform': ['movie streaming', 'film streaming', 'cinema streaming', 'movie platform'],
        'TV Streaming Service': ['tv streaming', 'television streaming', 'tv shows online', 'series streaming'],
        
        # Tier 2: Content Categories
        'Sports Streaming': ['sports streaming', 'live sports', 'sports content', 'athletic events streaming'],
        'News Streaming': ['news streaming', 'live news', 'news content', 'breaking news streaming'],
        'Kids Content Streaming': ['kids streaming', 'children shows', 'family content', 'cartoon streaming'],
        'Documentary Streaming': ['documentary streaming', 'educational content', 'documentary platform'],
        
        # Tier 3: Specialized Services
        'Live TV Streaming': ['live tv streaming', 'live television', 'broadcast streaming', 'tv channels online'],
        'Music Streaming': ['music streaming', 'audio streaming', 'music platform', 'song streaming'],
        'Gaming Streaming': ['game streaming', 'gaming content', 'esports streaming', 'gaming platform'],
        
        # Tier 4: Technical Categories
        'Mobile Streaming': ['mobile streaming', 'smartphone streaming', 'tablet streaming', 'mobile app'],
        'Smart TV Streaming': ['smart tv streaming', 'tv app', 'television app', 'streaming on tv'],
        'Free Streaming Service': ['free streaming', 'ad-supported streaming', 'free content platform'],
        
        # Tier 5: Generic Categories
        'International Content': ['international streaming', 'foreign content', 'global streaming', 'international shows'],
        'Original Content Platform': ['original content', 'exclusive shows', 'original series', 'platform originals']
    }
    
    property_groups = defaultdict(list)
    feedback_matched = 0
    
    for feedback_item in feedback_data:
        content = feedback_item['content'].lower()
        matched_properties = set()
        
        # Check each streaming property with weighted scoring
        for property_name, variations in streaming_properties.items():
            match_score = 0
            for variation in variations:
                if variation.lower() in content:
                    match_score += 1
            
            if match_score > 0:
                matched_properties.add(property_name)
        
        # Add to groups
        if matched_properties:
            feedback_matched += 1
            for prop in matched_properties:
                property_groups[prop].append({
                    'content': content,
                    'metadata': feedback_item
                })
        else:
            # Generic streaming fallback with stricter criteria
            streaming_terms = ['streaming service', 'video platform', 'subscription service']
            if any(term in content for term in streaming_terms):
                property_groups['General Streaming'].append({
                    'content': content,
                    'metadata': feedback_item
                })
    
    print(f"📊 Property matching: {feedback_matched}/{len(feedback_data)} feedback items matched to streaming properties")
    
    # Filter by minimum mentions threshold
    filtered_groups = {}
    for k, v in property_groups.items():
        if len(v) >= min_mentions_threshold:
            # Extract just the content for analysis
            filtered_groups[k] = [item['content'] for item in v]
        else:
            print(f"   ⚠️  Excluded {k}: only {len(v)} mentions (below threshold of {min_mentions_threshold})")
    
    return filtered_groups

def analyze_streaming_property_sentiment(property_name, feedback_texts):
    """
    Enhanced sentiment analysis with confidence scoring for streaming properties
    """
    # Refined sentiment keywords with weights
    sentiment_keywords = {
        'positive': {
            # High confidence positive (weight 2)
            'love': 2, 'amazing': 2, 'excellent': 2, 'fantastic': 2, 'perfect': 2,
            'best': 2, 'outstanding': 2, 'brilliant': 2, 'incredible': 2,
            
            # Medium confidence positive (weight 1.5)
            'great': 1.5, 'good': 1.5, 'awesome': 1.5, 'wonderful': 1.5,
            'recommend': 1.5, 'favorite': 1.5, 'satisfied': 1.5,
            
            # Streaming-specific positive (weight 1.5)
            'binge watch': 1.5, 'addicted': 1.5, 'must watch': 1.5,
            'quality content': 1.5, 'worth it': 1.5, 'impressed': 1.5,
            
            # Basic positive (weight 1)
            'like': 1, 'enjoy': 1, 'fine': 1, 'decent': 1, 'okay': 1
        },
        
        'negative': {
            # High confidence negative (weight 2)
            'hate': 2, 'terrible': 2, 'awful': 2, 'horrible': 2, 'worst': 2,
            'pathetic': 2, 'garbage': 2, 'sucks': 2, 'disappointing': 2,
            
            # Medium confidence negative (weight 1.5)
            'frustrating': 1.5, 'annoying': 1.5, 'bad': 1.5, 'poor': 1.5,
            'waste of money': 1.5, 'overpriced': 1.5, 'cancel': 1.5,
            
            # Technical issues (weight 1.5)
            'buffering': 1.5, 'crashes': 1.5, 'slow': 1.5, 'broken': 1.5,
            'error': 1.5, 'glitchy': 1.5, 'loading problems': 1.5,
            
            # Basic negative (weight 1)
            'dislike': 1, 'meh': 1, 'boring': 1, 'limited': 1
        }
    }
    
    # Enhanced analysis
    sentiment_scores = {'positive': 0, 'negative': 0}
    theme_mentions = defaultdict(int)
    confidence_scores = []
    
    for text in feedback_texts:
        text_lower = text.lower()
        text_pos_score = 0
        text_neg_score = 0
        
        # Calculate weighted sentiment scores
        for word, weight in sentiment_keywords['positive'].items():
            if word in text_lower:
                text_pos_score += weight
        
        for word, weight in sentiment_keywords['negative'].items():
            if word in text_lower:
                text_neg_score += weight
        
        # Classify with confidence
        if text_pos_score > text_neg_score:
            sentiment_scores['positive'] += 1
            confidence_scores.append(text_pos_score / (text_pos_score + text_neg_score + 0.1))
        elif text_neg_score > text_pos_score:
            sentiment_scores['negative'] += 1
            confidence_scores.append(text_neg_score / (text_pos_score + text_neg_score + 0.1))
        else:
            confidence_scores.append(0.1)  # Low confidence for neutral
        
        # Extract themes
        themes = extract_themes_from_text(text_lower)
        for theme in themes:
            theme_mentions[theme] += 1
    
    # Calculate metrics
    total_mentions = len(feedback_texts)
    neutral_count = total_mentions - sentiment_scores['positive'] - sentiment_scores['negative']
    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
    
    # Enhanced trend determination
    sentiment_trend = determine_sentiment_trend_enhanced(sentiment_scores, neutral_count, avg_confidence)
    
    # Generate business summary
    summary = generate_property_summary_enhanced(property_name, sentiment_scores, neutral_count, theme_mentions, total_mentions, avg_confidence)
    
    return {
        "topic": property_name,
        "topic_summary": summary,
        "key_themes": list(dict(sorted(theme_mentions.items(), key=lambda x: x[1], reverse=True)[:5]).keys()),
        "sentiment_trend": sentiment_trend,
        "positive_count": sentiment_scores['positive'],
        "negative_count": sentiment_scores['negative'],
        "neutral_count": neutral_count,
        "total_mentions": total_mentions,
        "positive_percentage": round((sentiment_scores['positive'] / total_mentions) * 100, 1),
        "negative_percentage": round((sentiment_scores['negative'] / total_mentions) * 100, 1),
        "neutral_percentage": round((neutral_count / total_mentions) * 100, 1),
        "confidence_score": round(avg_confidence * 100, 1),
        "analysis_method": "enhanced_keyword_weighted",
        "processed_at": datetime.datetime.now().isoformat(),
        # QuickSight-friendly fields
        "sentiment_category": get_sentiment_category(sentiment_trend),
        "priority_level": get_priority_level(total_mentions, sentiment_trend),
        "action_required": requires_action(sentiment_scores, total_mentions)
    }

def determine_sentiment_trend_enhanced(sentiment_scores, neutral_count, confidence):
    """
    Enhanced sentiment trend with confidence weighting
    """
    total = sentiment_scores['positive'] + sentiment_scores['negative'] + neutral_count
    if total == 0:
        return 'neutral'
    
    pos_pct = (sentiment_scores['positive'] / total) * 100
    neg_pct = (sentiment_scores['negative'] / total) * 100
    
    # Confidence adjustment
    confidence_multiplier = min(confidence * 2, 1.5)  # Cap at 1.5x
    
    adjusted_pos = pos_pct * confidence_multiplier
    adjusted_neg = neg_pct * confidence_multiplier
    
    if adjusted_pos >= 70:
        return 'strongly_positive'
    elif adjusted_pos >= 55:
        return 'positive'
    elif adjusted_neg >= 70:
        return 'strongly_negative'
    elif adjusted_neg >= 55:
        return 'negative'
    elif adjusted_pos > adjusted_neg:
        return 'mixed_positive'
    elif adjusted_neg > adjusted_pos:
        return 'mixed_negative'
    else:
        return 'neutral'

def get_sentiment_category(sentiment_trend):
    """
    QuickSight-friendly sentiment categorization
    """
    if 'positive' in sentiment_trend:
        return 'Positive'
    elif 'negative' in sentiment_trend:
        return 'Negative'
    else:
        return 'Neutral'

def get_priority_level(total_mentions, sentiment_trend):
    """
    Business priority level for QuickSight dashboards
    """
    if total_mentions >= 50:
        priority_base = 'High'
    elif total_mentions >= 20:
        priority_base = 'Medium'
    else:
        priority_base = 'Low'
    
    if 'strongly_negative' in sentiment_trend or 'negative' in sentiment_trend:
        return f'{priority_base} - Action Needed'
    else:
        return priority_base

def requires_action(sentiment_scores, total_mentions):
    """
    Determine if property requires immediate action
    """
    if total_mentions < 5:
        return False
    
    neg_percentage = (sentiment_scores['negative'] / total_mentions) * 100
    return neg_percentage >= 40

def extract_themes_from_text(text):
    """
    Enhanced theme extraction for streaming service context
    """
    theme_patterns = {
        'content_quality': ['content quality', 'show quality', 'programming', 'originals', 'exclusive content'],
        'pricing_value': ['price', 'cost', 'expensive', 'value', 'subscription', 'worth it', 'money'],
        'user_experience': ['app experience', 'interface', 'navigation', 'search function', 'ease of use'],
        'technical_performance': ['streaming quality', 'buffering', 'video quality', 'loading speed', 'connectivity'],
        'content_variety': ['content selection', 'variety', 'catalog size', 'library', 'options'],
        'customer_service': ['customer support', 'help', 'service', 'response time'],
        'competitor_comparison': ['vs netflix', 'compared to disney', 'better than hulu', 'amazon prime'],
        'advertising': ['ads', 'commercials', 'interruptions', 'ad-free'],
        'device_compatibility': ['roku', 'apple tv', 'smart tv', 'mobile app', 'casting'],
        'content_discovery': ['recommendations', 'finding shows', 'browse', 'categories']
    }
    
    themes_found = []
    for theme, keywords in theme_patterns.items():
        if any(keyword in text for keyword in keywords):
            themes_found.append(theme.replace('_', ' '))
    
    return themes_found

def generate_property_summary_enhanced(property_name, sentiment_scores, neutral_count, theme_mentions, total_mentions, confidence):
    """
    Enhanced business summary with confidence metrics
    """
    total = sentiment_scores['positive'] + sentiment_scores['negative'] + neutral_count
    if total == 0:
        return f"Analysis of {property_name} based on {total_mentions} customer feedback entries."
    
    pos_pct = round((sentiment_scores['positive'] / total) * 100, 1)
    neg_pct = round((sentiment_scores['negative'] / total) * 100, 1)
    confidence_pct = round(confidence * 100, 1)
    
    # Top themes
    top_themes = sorted(theme_mentions.items(), key=lambda x: x[1], reverse=True)[:3]
    theme_text = ', '.join([theme.replace('_', ' ') for theme, _ in top_themes]) if top_themes else "general feedback"
    
    # Sentiment description
    if pos_pct >= 60:
        sentiment_desc = "predominantly positive"
    elif neg_pct >= 60:
        sentiment_desc = "predominantly negative"  
    elif pos_pct > neg_pct:
        sentiment_desc = "moderately positive"
    elif neg_pct > pos_pct:
        sentiment_desc = "moderately negative"
    else:
        sentiment_desc = "mixed"
    
    return f"Customer feedback analysis for {property_name} reveals {sentiment_desc} sentiment ({pos_pct}% positive, {neg_pct}% negative) across {total_mentions} mentions with {confidence_pct}% confidence. Key discussion areas include {theme_text}."

def generate_executive_summary(results):
    """
    Enhanced executive summary for business stakeholders
    """
    if not results:
        return "No streaming properties analyzed - insufficient data in Knowledge Base."
    
    total_mentions = sum(r['total_mentions'] for r in results)
    total_properties = len(results)
    
    # Business insights
    high_priority = [r for r in results if 'Action Needed' in r.get('priority_level', '')]
    positive_trending = [r for r in results if r['sentiment_category'] == 'Positive']
    negative_trending = [r for r in results if r['sentiment_category'] == 'Negative']
    
    # Top performers by mentions
    top_3 = results[:3]
    
    summary = f"""🎯 Streaming Service Portfolio Sentiment Analysis - Executive Summary

📊 ANALYSIS SCOPE:
• {total_properties} streaming properties analyzed across {total_mentions:,} customer feedback mentions
• Analysis confidence: High (weighted keyword classification with theme extraction)
• Data source: Knowledge Base via Bedrock Agent retrieval

🏆 TOP PERFORMING PROPERTIES:
{chr(10).join([f'• {r["topic"]}: {r["total_mentions"]} mentions ({r["sentiment_trend"].replace("_", " ").title()})' for r in top_3])}

📈 BUSINESS INSIGHTS:
• Properties trending positive: {len(positive_trending)} ({round(len(positive_trending)/total_properties*100)}% of portfolio)
• Properties needing attention: {len(negative_trending)} requiring review
• High-priority action items: {len(high_priority)} properties

💡 STRATEGIC RECOMMENDATIONS:
• Focus resources on {results[0]['topic']} (highest customer engagement)
• {"Address negative sentiment in " + ", ".join([r['topic'] for r in high_priority[:2]]) if high_priority else "Continue current positive momentum"}
• Monitor emerging themes: content quality, pricing value, technical performance"""
    
    return summary

def save_results_to_s3(s3_client, results, config):
    """
    Enhanced S3 save with QuickSight optimization
    """
    try:
        timestamp = datetime.datetime.now()
        
        # Prepare QuickSight-optimized output
        output_data = {
            "analysis_metadata": {
                "analysis_timestamp": timestamp.isoformat(),
                "analysis_date": timestamp.strftime('%Y-%m-%d'),
                "analysis_time": timestamp.strftime('%H:%M:%S'),
                "analysis_id": str(uuid.uuid4()),
                "analysis_method": "enhanced_keyword_weighted",
                "total_properties_analyzed": len(results),
                "total_mentions_processed": sum(r['total_mentions'] for r in results),
                "streaming_focus": True,
                "version": "2.0",
                "quicksight_optimized": True
            },
            "results": results,
            "dashboard_summary": {
                "top_5_by_mentions": [
                    {
                        "property": r['topic'], 
                        "mentions": r['total_mentions'],
                        "sentiment": r['sentiment_category'],
                        "trend": r['sentiment_trend']
                    } for r in results[:5]
                ],
                "sentiment_distribution": {
                    "positive_properties": len([r for r in results if r['sentiment_category'] == 'Positive']),
                    "negative_properties": len([r for r in results if r['sentiment_category'] == 'Negative']),
                    "neutral_properties": len([r for r in results if r['sentiment_category'] == 'Neutral'])
                },
                "priority_analysis": {
                    "high_priority": [r['topic'] for r in results if 'High' in r.get('priority_level', '')],
                    "action_required": [r['topic'] for r in results if r.get('action_required', False)]
                },
                "key_metrics": {
                    "avg_confidence": round(sum(r['confidence_score'] for r in results) / len(results), 1) if results else 0,
                    "total_engagement": sum(r['total_mentions'] for r in results),
                    "properties_with_high_confidence": len([r for r in results if r['confidence_score'] >= 70])
                }
            },
            # Flat structure for QuickSight table imports
            "quicksight_flat_data": [
                {
                    "property_name": r['topic'],
                    "total_mentions": r['total_mentions'],
                    "positive_count": r['positive_count'],
                    "negative_count": r['negative_count'],
                    "neutral_count": r['neutral_count'],
                    "positive_percentage": r['positive_percentage'],
                    "negative_percentage": r['negative_percentage'],
                    "sentiment_trend": r['sentiment_trend'],
                    "sentiment_category": r['sentiment_category'],
                    "confidence_score": r['confidence_score'],
                    "priority_level": r['priority_level'],
                    "action_required": r['action_required'],
                    "ranking": r['ranking_by_mentions'],
                    "market_share": r['market_share_percentage'],
                    "analysis_date": timestamp.strftime('%Y-%m-%d'),
                    "primary_theme": r['key_themes'][0] if r['key_themes'] else 'general'
                } for r in results
            ]
        }
        
        # Save main file
        s3_client.put_object(
            Bucket=config['s3_bucket'],
            Key=config['s3_output_key'],
            Body=json.dumps(output_data, indent=2, ensure_ascii=False),
            ContentType='application/json',
            Metadata={
                'analysis-timestamp': timestamp.isoformat(),
                'total-properties': str(len(results)),
                'analysis-method': 'enhanced-keyword-weighted',
                'quicksight-ready': 'true'
            }
        )
        
        # Save QuickSight-specific flat file
        quicksight_key = config['s3_output_key'].replace('.json', '-quicksight.json')
        s3_client.put_object(
            Bucket=config['s3_bucket'],
            Key=quicksight_key,
            Body=json.dumps(output_data['quicksight_flat_data'], indent=2, ensure_ascii=False),
            ContentType='application/json'
        )
        
        print(f"✅ Results saved to:")
        print(f"   📊 Main: s3://{config['s3_bucket']}/{config['s3_output_key']}")
        print(f"   📈 QuickSight: s3://{config['s3_bucket']}/{quicksight_key}")
        
    except Exception as e:
        print(f"❌ Error saving to S3: {str(e)}")
        raise

def create_response(status_code, body):
    """
    Enhanced Lambda response with CORS and metadata
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'X-Analysis-Method': 'enhanced-keyword-weighted',
            'X-Timestamp': datetime.datetime.now().isoformat()
        },
        'body': json.dumps(body, ensure_ascii=False, default=str)
    }
