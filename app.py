from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import json
from datetime import datetime, timedelta
import random
import re
from collections import Counter
import numpy as np

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app)

# ML Model Simulation
class MLSentimentAnalyzer:
    def __init__(self):
        self.model_name = "Advanced Sentiment Analyzer v2.0"
    
    def analyze_sentiment(self, text):
        """Enhanced sentiment analysis with ML simulation"""
        # Simulate ML processing
        positive_words = ['good', 'great', 'awesome', 'amazing', 'love', 'excellent', 'fantastic', 'perfect', 'best', 'wonderful']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'dislike', 'boring', 'stupid', 'waste']
        
        text_lower = text.lower()
        positive_score = sum(1 for word in positive_words if word in text_lower)
        negative_score = sum(1 for word in negative_words if word in text_lower)
        
        # Simulate ML confidence
        total_score = positive_score + negative_score
        if total_score == 0:
            sentiment = "neutral"
            confidence = random.uniform(0.6, 0.8)
        elif positive_score > negative_score:
            sentiment = "positive"
            confidence = min(0.95, 0.7 + (positive_score / 10))
        else:
            sentiment = "negative"
            confidence = min(0.95, 0.7 + (negative_score / 10))
        
        return sentiment, round(confidence, 2)
    
    def detect_toxicity(self, text):
        """Simulate toxicity detection"""
        toxic_words = ['hate', 'stupid', 'idiot', 'moron', 'kill', 'die', 'terrible', 'awful', 'disgusting']
        text_lower = text.lower()
        
        toxic_count = sum(1 for word in toxic_words if word in text_lower)
        toxicity_level = min(1.0, toxic_count * 0.2)
        
        return round(toxicity_level, 2)
    
    def extract_keywords(self, text):
        """Extract keywords from text"""
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        word_freq = Counter(filtered_words)
        top_keywords = word_freq.most_common(15)
        
        return [{'text': word, 'frequency': min(5, max(1, count))} for word, count in top_keywords]

# Initialize analyzer
ml_analyzer = MLSentimentAnalyzer()

@app.route('/')
def index():
    """Serve the main dashboard"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"""
        <html>
            <head><title>Error</title></head>
            <body>
                <h1>Template Error</h1>
                <p>Could not load index.html. Please make sure:</p>
                <ol>
                    <li>You have a 'templates' folder in your project directory</li>
                    <li>The 'templates' folder contains 'index.html'</li>
                    <li>Your folder structure is correct</li>
                </ol>
                <p>Error details: {str(e)}</p>
            </body>
        </html>
        """, 500

@app.route('/api/analyze', methods=['POST'])
def analyze_comments():
    """Main analysis endpoint with ML integration"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        platform = data.get('platform', 'youtube')
        analysis_type = data.get('analysis_type', 'advanced_ml')
        
        print(f"Analyzing {platform} content: {url}")
        
        # Generate realistic mock data based on platform
        analysis_data = generate_ml_analysis(platform, analysis_type)
        
        return jsonify({
            'success': True,
            'data': analysis_data,
            'analysis_id': f"ML_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'model_used': ml_analyzer.model_name
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Analysis failed. Please try again.'
        }), 500

@app.route('/api/user/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # In a real app, you'd save to database and hash passwords
        user_data = {
            'name': data.get('name'),
            'email': data.get('email'),
            'userType': data.get('userType', 'professional'),
            'occupation': data.get('occupation', ''),
            'company': data.get('company', ''),
            'bio': data.get('bio', ''),
            'type': 'basic'
        }
        
        # Store in session (in real app, use database)
        session['current_user'] = user_data
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': user_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/user/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # In a real app, verify against database
        # For demo, create a mock user
        user_data = {
            'name': 'Demo User',
            'email': email,
            'userType': 'professional',
            'occupation': 'Digital Marketer',
            'company': 'Social Media Agency',
            'bio': 'Passionate about data-driven social media strategies',
            'type': 'premium'
        }
        
        session['current_user'] = user_data
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/user/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    session.pop('current_user', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/user/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    user = session.get('current_user')
    if user:
        return jsonify({'success': True, 'user': user})
    else:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

def generate_ml_analysis(platform, analysis_type):
    """Generate comprehensive ML analysis data"""
    
    # Platform-specific comment generation
    comments = generate_platform_comments(platform, count=50)
    
    # ML Analysis
    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
    analyzed_comments = []
    all_text = ""
    total_toxicity = 0
    
    for comment in comments:
        sentiment, confidence = ml_analyzer.analyze_sentiment(comment['text'])
        toxicity = ml_analyzer.detect_toxicity(comment['text'])
        
        analyzed_comment = {
            'user': comment['user'],
            'text': comment['text'],
            'sentiment': sentiment,
            'ml_score': confidence,
            'toxicity': toxicity,
            'timestamp': comment.get('timestamp', datetime.now().isoformat())
        }
        
        analyzed_comments.append(analyzed_comment)
        sentiment_counts[sentiment] += 1
        all_text += " " + comment['text']
        total_toxicity += toxicity
    
    # Calculate metrics
    total_comments = len(comments)
    avg_toxicity = total_toxicity / total_comments
    
    # ML Metrics
    ml_metrics = {
        'confidence': random.randint(85, 98),
        'toxicity': round(avg_toxicity * 100, 1),
        'engagement_score': random.randint(65, 95),
        'virality_potential': random.randint(70, 95)
    }
    
    # ML Insights
    ml_insights = generate_ml_insights(sentiment_counts, ml_metrics, platform)
    
    # Keywords
    keywords = ml_analyzer.extract_keywords(all_text)
    
    # Time series data
    time_series = generate_time_series_data(sentiment_counts)
    
    # Emotion analysis
    emotions = generate_emotion_analysis(analyzed_comments)
    
    return {
        'platform': platform,
        'totalComments': total_comments,
        'sentiment': {
            'positive': round((sentiment_counts['positive'] / total_comments) * 100, 1),
            'neutral': round((sentiment_counts['neutral'] / total_comments) * 100, 1),
            'negative': round((sentiment_counts['negative'] / total_comments) * 100, 1)
        },
        'ml_metrics': ml_metrics,
        'ml_insights': ml_insights,
        'keywords': keywords,
        'comments': analyzed_comments[:10],  # Return first 10 comments
        'timeLabels': time_series['labels'],
        'positiveData': time_series['positive'],
        'neutralData': time_series['neutral'],
        'negativeData': time_series['negative'],
        'emotions': list(emotions.keys()),
        'emotionData': list(emotions.values()),
        'content_metadata': {
            'category': categorize_content(platform),
            'target_audience': estimate_audience(sentiment_counts),
            'engagement_level': calculate_engagement(sentiment_counts),
            'recommended_actions': generate_recommendations(sentiment_counts, ml_metrics)
        }
    }

def generate_platform_comments(platform, count=50):
    """Generate platform-specific comments"""
    base_comments = [
        {"user": "User123", "text": "This is absolutely amazing! Love it! ❤️"},
        {"user": "CoolViewer", "text": "Not bad, but could be better."},
        {"user": "RandomPerson", "text": "I don't understand this at all."},
        {"user": "HappyFan", "text": "Best content I've seen in ages!"},
        {"user": "CriticalThinker", "text": "The quality has really gone down lately."},
        {"user": "SupportiveUser", "text": "Keep up the great work! You're doing awesome!"},
        {"user": "QuestionGuy", "text": "Why did you make this decision?"},
        {"user": "ExcitedFan", "text": "Can't wait for the next one! So excited!"},
        {"user": "DisappointedUser", "text": "This is terrible, I expected more."},
        {"user": "NeutralViewer", "text": "It's okay, nothing special."},
        {"user": "TechEnthusiast", "text": "The technical aspects are impressive!"},
        {"user": "CreativeMind", "text": "Love the creativity and innovation!"},
        {"user": "DetailedViewer", "text": "The attention to detail is remarkable."},
        {"user": "CasualWatcher", "text": "Pretty good, I enjoyed watching this."},
        {"user": "HarshCritic", "text": "This is the worst thing I've ever seen."}
    ]
    
    # Platform-specific comments
    platform_comments = {
        'youtube': [
            {"user": "YouTubeFan", "text": "Great video! Liked and subscribed! 👍"},
            {"user": "ContentCreator", "text": "Awesome editing skills! What software do you use?"},
            {"user": "BingeWatcher", "text": "Bingeing your channel all day! 😍"},
            {"user": "TechReviewer", "text": "The production quality is outstanding!"}
        ],
        'instagram': [
            {"user": "InstaFamous", "text": "Fire content! 🔥"},
            {"user": "PhotoLover", "text": "Amazing aesthetics! 📸"},
            {"user": "SocialUser", "text": "This deserves more likes! ❤️"},
            {"user": "Influencer", "text": "Great storytelling through images!"}
        ],
        'twitter': [
            {"user": "TwitterUser", "text": "Based take! Retweeting this! 🔁"},
            {"user": "ThreadReader", "text": "Great thread! Learned a lot!"},
            {"user": "TrendWatcher", "text": "This is trending material! 📈"},
            {"user": "DebateLover", "text": "Interesting perspective, let's discuss!"}
        ],
        'tiktok': [
            {"user": "TikToker", "text": "This is viral content! 🚀"},
            {"user": "GenZUser", "text": "No cap, this is fire! 🔥"},
            {"user": "ShortFormFan", "text": "Perfect for TikTok! 👏"},
            {"user": "DanceLover", "text": "The transitions are smooth! 💃"}
        ]
    }
    
    # Combine and select comments
    all_comments = base_comments + platform_comments.get(platform, [])
    selected_comments = random.sample(all_comments, min(count, len(all_comments)))
    
    # Add timestamps
    for comment in selected_comments:
        comment['timestamp'] = (datetime.now() - timedelta(hours=random.randint(0, 168))).isoformat()
    
    return selected_comments

def generate_ml_insights(sentiment_counts, ml_metrics, platform):
    """Generate AI-powered insights"""
    total = sum(sentiment_counts.values())
    positive_ratio = sentiment_counts['positive'] / total
    
    insights = {
        'toxicity': "Low toxicity levels detected in comments" if ml_metrics['toxicity'] < 10 else "Moderate toxicity detected, consider moderation",
        'engagement': "High engagement potential with current sentiment" if positive_ratio > 0.6 else "Moderate engagement, consider content optimization",
        'audience': f"Primarily engages 18-34 demographic on {platform}",
        'content': "Consider creating follow-up content on trending topics" if positive_ratio > 0.7 else "Experiment with different content formats"
    }
    
    return insights

def generate_time_series_data(sentiment_counts):
    """Generate time series data for charts"""
    days = 7
    base_positive = sentiment_counts['positive']
    base_neutral = sentiment_counts['neutral']
    base_negative = sentiment_counts['negative']
    
    labels = []
    positive_data = []
    neutral_data = []
    negative_data = []
    
    for i in range(days, 0, -1):
        date = (datetime.now() - timedelta(days=i)).strftime('%b %d')
        labels.append(date)
        
        # Add realistic variations
        variation = random.uniform(-0.2, 0.2)
        positive_data.append(max(10, min(90, base_positive * (1 + variation))))
        neutral_data.append(max(5, min(50, base_neutral * (1 + variation * 0.5))))
        negative_data.append(max(5, min(40, base_negative * (1 + variation * 0.3))))
    
    return {
        'labels': labels,
        'positive': positive_data,
        'neutral': neutral_data,
        'negative': negative_data
    }

def generate_emotion_analysis(comments):
    """Generate emotion distribution"""
    emotions = {
        'Joy': 0,
        'Surprise': 0,
        'Anger': 0,
        'Sadness': 0,
        'Fear': 0,
        'Disgust': 0
    }
    
    # Simple emotion detection based on keywords
    emotion_keywords = {
        'Joy': ['happy', 'love', 'great', 'awesome', 'amazing', 'good', 'excited'],
        'Surprise': ['wow', 'surprised', 'unexpected', 'shocked'],
        'Anger': ['angry', 'mad', 'hate', 'terrible', 'awful', 'bad'],
        'Sadness': ['sad', 'upset', 'disappointed', 'sorry'],
        'Fear': ['scared', 'afraid', 'worried', 'nervous'],
        'Disgust': ['disgusting', 'gross', 'nasty']
    }
    
    for comment in comments:
        text_lower = comment['text'].lower()
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                emotions[emotion] += 1
    
    # Normalize to percentages
    total = sum(emotions.values())
    if total > 0:
        for emotion in emotions:
            emotions[emotion] = round((emotions[emotion] / total) * 100, 1)
    
    return emotions

def categorize_content(platform):
    """Categorize content based on platform"""
    categories = {
        'youtube': ['Entertainment', 'Education', 'Technology', 'Gaming', 'Music'],
        'instagram': ['Lifestyle', 'Fashion', 'Travel', 'Food', 'Art'],
        'twitter': ['News', 'Politics', 'Technology', 'Sports', 'Entertainment'],
        'tiktok': ['Entertainment', 'Dance', 'Comedy', 'Education', 'Beauty']
    }
    return random.choice(categories.get(platform, ['Entertainment']))

def estimate_audience(sentiment_counts):
    """Estimate target audience"""
    audiences = ['General Audience', 'Teens', 'Young Adults', 'Professionals', 'All Ages']
    return random.choice(audiences)

def calculate_engagement(sentiment_counts):
    """Calculate engagement level"""
    positive_ratio = sentiment_counts['positive'] / sum(sentiment_counts.values())
    
    if positive_ratio > 0.7:
        return 'Very High'
    elif positive_ratio > 0.5:
        return 'High'
    elif positive_ratio > 0.3:
        return 'Medium'
    else:
        return 'Low'

def generate_recommendations(sentiment_counts, ml_metrics):
    """Generate content recommendations"""
    recommendations = []
    
    if sentiment_counts['positive'] > sentiment_counts['negative'] * 2:
        recommendations.append("Continue with similar content style")
    else:
        recommendations.append("Experiment with different content formats")
    
    if ml_metrics['toxicity'] > 15:
        recommendations.append("Implement comment moderation")
    
    if ml_metrics['engagement_score'] > 80:
        recommendations.append("Consider expanding to similar topics")
    
    return recommendations

if __name__ == '__main__':
    # Print current working directory and template folder path
    print(f"Current working directory: {os.getcwd()}")
    print(f"Template folder path: {os.path.join(os.getcwd(), 'templates')}")
    
    # Check if templates folder exists
    templates_path = os.path.join(os.getcwd(), 'templates')
    if os.path.exists(templates_path):
        print("✓ Templates folder exists")
        # List files in templates folder
        template_files = os.listdir(templates_path)
        print(f"Files in templates folder: {template_files}")
    else:
        print("✗ Templates folder does not exist. Creating it...")
        os.makedirs(templates_path)
    
    app.run(debug=True, host='0.0.0.0', port=5000)