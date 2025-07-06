from http.server import BaseHTTPRequestHandler
import json
import hashlib
import random
import urllib.parse
from typing import List

def get_intelligent_keywords(domain: str) -> List[str]:
    """Generate intelligent keywords based on domain analysis"""
    domain_lower = domain.lower()
    
    # AI/ML Companies
    if any(keyword in domain_lower for keyword in ['anthropic', 'openai', 'ai', 'ml', 'claude']):
        return [
            'artificial intelligence', 'machine learning', 'ai assistant', 'chatbot', 'claude ai',
            'conversational ai', 'language model', 'ai safety', 'natural language processing',
            'deep learning', 'neural networks', 'ai research', 'generative ai', 'ai tools',
            'ai platform', 'ai technology', 'machine intelligence', 'automated reasoning'
        ]
    
    # News/Media Companies
    elif any(keyword in domain_lower for keyword in ['cnn', 'bbc', 'news', 'times', 'reuters', 'fox', 'nbc', 'abc']):
        return [
            'breaking news', 'world news', 'politics', 'business news', 'technology news',
            'live news', 'news updates', 'current events', 'news analysis', 'international news',
            'local news', 'sports news', 'entertainment news', 'weather forecast', 'news today',
            'headlines', 'news alerts', 'press release', 'journalism', 'news reporter'
        ]
    
    # E-commerce/Shopping
    elif any(keyword in domain_lower for keyword in ['amazon', 'shop', 'store', 'buy', 'mart', 'commerce', 'ebay']):
        return [
            'online shopping', 'buy online', 'e-commerce', 'best deals', 'discount shopping',
            'free shipping', 'online store', 'product reviews', 'price comparison', 'shopping deals',
            'customer reviews', 'shopping cart', 'secure checkout', 'return policy', 'gift cards',
            'sale items', 'new arrivals', 'trending products', 'product catalog', 'order tracking'
        ]
    
    # Social Media/Tech
    elif any(keyword in domain_lower for keyword in ['facebook', 'twitter', 'instagram', 'social', 'meta', 'tiktok']):
        return [
            'social media', 'social network', 'connect with friends', 'share photos', 'social platform',
            'user engagement', 'social sharing', 'community building', 'social marketing', 'influencer',
            'social media management', 'content creation', 'viral content', 'social media strategy',
            'digital marketing', 'brand awareness', 'social analytics', 'user generated content'
        ]
    
    # Streaming/Entertainment
    elif any(keyword in domain_lower for keyword in ['netflix', 'youtube', 'stream', 'video', 'music', 'spotify']):
        return [
            'streaming', 'watch online', 'video streaming', 'movies online', 'tv shows',
            'entertainment', 'binge watch', 'original series', 'documentaries', 'streaming service',
            'video content', 'premium content', 'live streaming', 'on-demand', 'digital media',
            'content library', 'streaming platform', 'video quality', 'mobile streaming'
        ]
    
    # Financial/Banking
    elif any(keyword in domain_lower for keyword in ['bank', 'finance', 'pay', 'credit', 'invest', 'money']):
        return [
            'online banking', 'mobile banking', 'financial services', 'credit cards', 'personal loans',
            'investment', 'savings account', 'checking account', 'mortgage', 'financial planning',
            'wealth management', 'retirement planning', 'insurance', 'credit score', 'banking fees',
            'secure banking', 'financial advisor', 'money management', 'loan calculator'
        ]
    
    # Education/Learning
    elif any(keyword in domain_lower for keyword in ['edu', 'university', 'school', 'learn', 'course', 'academy']):
        return [
            'online courses', 'education', 'learning platform', 'skill development', 'certification',
            'degree programs', 'distance learning', 'e-learning', 'professional development',
            'academic courses', 'training programs', 'educational resources', 'study materials',
            'online university', 'continuing education', 'career advancement', 'learning management'
        ]
    
    # Travel/Booking
    elif any(keyword in domain_lower for keyword in ['travel', 'hotel', 'booking', 'flight', 'trip', 'airbnb']):
        return [
            'travel booking', 'hotel reservation', 'flight booking', 'vacation packages', 'travel deals',
            'accommodation', 'trip planning', 'travel guide', 'destination', 'travel insurance',
            'car rental', 'business travel', 'family vacation', 'weekend getaway', 'travel reviews',
            'booking confirmation', 'travel itinerary', 'last minute deals', 'travel tips'
        ]
    
    # Health/Medical
    elif any(keyword in domain_lower for keyword in ['health', 'medical', 'doctor', 'medicine', 'pharma', 'clinic']):
        return [
            'health information', 'medical advice', 'symptoms checker', 'health tips', 'wellness',
            'medical conditions', 'treatment options', 'healthcare', 'preventive care', 'nutrition',
            'fitness', 'mental health', 'medical research', 'health insurance', 'telemedicine',
            'prescription drugs', 'medical specialties', 'health screening', 'medical records'
        ]
    
    # Food/Restaurant
    elif any(keyword in domain_lower for keyword in ['food', 'restaurant', 'recipe', 'cook', 'eat', 'delivery']):
        return [
            'food delivery', 'restaurant menu', 'recipes', 'cooking tips', 'food ordering',
            'meal planning', 'nutrition facts', 'restaurant reviews', 'takeout', 'catering',
            'food safety', 'cooking techniques', 'ingredients', 'dietary restrictions', 'food blog',
            'restaurant finder', 'food photography', 'culinary arts', 'food trends'
        ]
    
    # Technology/Software
    elif any(keyword in domain_lower for keyword in ['tech', 'software', 'app', 'digital', 'cloud', 'data']):
        return [
            'technology solutions', 'software development', 'mobile app', 'cloud computing', 'data analytics',
            'cybersecurity', 'digital transformation', 'automation', 'innovation', 'tech support',
            'software tools', 'programming', 'web development', 'database management', 'IT services',
            'technology consulting', 'enterprise software', 'tech trends', 'digital innovation'
        ]
    
    # Generic business keywords
    else:
        # Generate industry-neutral business keywords
        return [
            'business solutions', 'professional services', 'customer support', 'contact us',
            'about company', 'our services', 'business consulting', 'industry expertise',
            'client testimonials', 'case studies', 'portfolio', 'company profile',
            'business strategy', 'market analysis', 'competitive advantage', 'quality assurance',
            'customer satisfaction', 'business growth', 'innovative solutions', 'service excellence'
        ]

def generate_mock_keywords(url: str, region: str = "us") -> List[dict]:
    """Generate intelligent keywords based on domain analysis"""
    
    # Extract domain for consistent results
    domain = url.replace('https://', '').replace('http://', '').split('/')[0]
    seed = int(hashlib.md5(domain.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    
    # Get intelligent keywords based on domain
    base_keywords = get_intelligent_keywords(domain)
    
    # Generate keyword variations with intelligent metrics
    keywords = []
    
    for i, base in enumerate(base_keywords):
        # Determine keyword characteristics based on length and content
        word_count = len(base.split())
        
        # Determine keyword type based on word count and content
        if word_count == 1:
            keyword_type = 'short-tail'
            base_volume = random.randint(10000, 100000)
            base_cpc = round(random.uniform(2.0, 8.0), 2)
            competition_prob = ['High', 'High', 'Medium']
        elif word_count == 2:
            keyword_type = 'mid-tail'
            base_volume = random.randint(3000, 25000)
            base_cpc = round(random.uniform(1.5, 5.0), 2)
            competition_prob = ['Medium', 'Medium', 'High', 'Low']
        else:
            keyword_type = 'long-tail'
            base_volume = random.randint(500, 8000)
            base_cpc = round(random.uniform(0.8, 3.0), 2)
            competition_prob = ['Low', 'Low', 'Medium']
        
        # Determine intent based on keyword content
        if any(word in base.lower() for word in ['buy', 'price', 'cost', 'deal', 'discount', 'order', 'purchase']):
            intent = 'commercial'
        elif any(word in base.lower() for word in ['how to', 'what is', 'guide', 'tips', 'tutorial', 'learn']):
            intent = 'informational'
        elif any(word in base.lower() for word in ['best', 'top', 'review', 'compare', 'vs']):
            intent = 'commercial'
        elif any(word in base.lower() for word in ['near me', 'location', 'address', 'contact']):
            intent = 'navigational'
        else:
            intent = random.choice(['informational', 'commercial', 'navigational'])
        
        # Adjust metrics based on intent
        if intent == 'commercial':
            base_cpc *= 1.5  # Commercial keywords typically have higher CPC
            base_volume = int(base_volume * 0.7)  # But often lower volume
        elif intent == 'navigational':
            base_volume = int(base_volume * 1.3)  # Brand searches have higher volume
            base_cpc *= 0.6  # But lower CPC
        
        # Generate realistic trends based on keyword type
        if 'ai' in base.lower() or 'digital' in base.lower() or 'online' in base.lower():
            trend = random.choice(['Rising', 'Rising', 'Stable'])
        elif 'traditional' in base.lower() or 'legacy' in base.lower():
            trend = random.choice(['Declining', 'Stable'])
        else:
            trend = random.choice(['Rising', 'Stable', 'Declining', 'Seasonal'])
        
        keywords.append({
            'keyword': base,
            'volume': base_volume,
            'cpc': round(base_cpc, 2),
            'competition': random.choice(competition_prob),
            'competition_score': round(random.uniform(0.1, 1.0), 2),
            'trend': trend,
            'type': keyword_type,
            'intent': intent,
            'count': random.randint(1, 15)
        })
        
        # Add some long-tail variations for popular keywords
        if i < 8 and keyword_type in ['short-tail', 'mid-tail']:
            variations = []
            if intent == 'informational':
                variations = [f"what is {base}", f"how to use {base}", f"{base} explained"]
            elif intent == 'commercial':
                variations = [f"best {base}", f"{base} reviews", f"cheap {base}"]
            else:
                variations = [f"{base} near me", f"{base} location"]
            
            for var in variations[:2]:
                var_volume = int(base_volume * random.uniform(0.1, 0.4))
                var_cpc = round(base_cpc * random.uniform(0.7, 1.2), 2)
                
                keywords.append({
                    'keyword': var,
                    'volume': var_volume,
                    'cpc': var_cpc,
                    'competition': random.choice(['Low', 'Medium']),
                    'competition_score': round(random.uniform(0.1, 0.6), 2),
                    'trend': trend,
                    'type': 'long-tail',
                    'intent': intent,
                    'count': random.randint(1, 8)
                })
    
    # Sort by volume descending
    keywords.sort(key=lambda x: x['volume'], reverse=True)
    return keywords[:30]  # Limit to 30 keywords

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {"message": "KeywordMiner AI Analyze API is running"}
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            url = data.get('url', '')
            region = data.get('region', 'auto')
            
            if not url:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"error": "URL is required"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Generate mock keywords
            keywords = generate_mock_keywords(url, region)
            
            # Sort by volume
            keywords.sort(key=lambda x: x.get('volume', 0), reverse=True)
            
            response = {
                "url": url,
                "region": region,
                "keywords_found": len(keywords),
                "keywords": keywords,
                "total_volume": sum(k.get('volume', 0) for k in keywords),
                "avg_cpc": round(sum(k.get('cpc', 0) for k in keywords) / len(keywords), 2) if keywords else 0
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"error": str(e)}
            self.wfile.write(json.dumps(response).encode())