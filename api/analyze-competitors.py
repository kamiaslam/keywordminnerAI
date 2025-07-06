from http.server import BaseHTTPRequestHandler
import json
import hashlib
import random
import urllib.parse
from typing import List

def generate_mock_keywords(url: str, region: str = "us") -> List[dict]:
    """Generate mock keywords for demo purposes"""
    
    # Extract domain for consistent results
    domain = url.replace('https://', '').replace('http://', '').split('/')[0]
    seed = int(hashlib.md5(domain.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    
    # Sample keywords based on domain
    if 'anthropic' in domain.lower():
        base_keywords = [
            'claude', 'ai assistant', 'anthropic', 'large language model', 
            'conversational ai', 'ai safety', 'constitutional ai', 'research',
            'machine learning', 'artificial intelligence', 'chatbot', 'nlp'
        ]
    elif 'cnn' in domain.lower():
        base_keywords = [
            'breaking news', 'world news', 'politics', 'business news',
            'technology news', 'health news', 'sports', 'entertainment',
            'weather', 'live updates', 'analysis', 'opinion'
        ]
    elif 'bbc' in domain.lower():
        base_keywords = [
            'bbc news', 'uk news', 'world news', 'sport', 'weather',
            'iplayer', 'radio', 'tv guide', 'brexit', 'politics',
            'business', 'technology', 'health', 'education'
        ]
    else:
        base_keywords = [
            'website', 'homepage', 'about', 'contact', 'services',
            'products', 'news', 'blog', 'support', 'help'
        ]
    
    # Generate keyword variations
    keywords = []
    for base in base_keywords:
        keywords.append({
            'keyword': base,
            'volume': random.randint(1000, 50000),
            'cpc': round(random.uniform(0.5, 5.0), 2),
            'competition': random.choice(['Low', 'Medium', 'High']),
            'competition_score': round(random.uniform(0.1, 1.0), 2),
            'trend': random.choice(['Rising', 'Stable', 'Declining', 'Seasonal']),
            'type': 'short-tail',
            'intent': 'informational',
            'count': random.randint(1, 10)
        })
    
    return keywords[:10]  # Limit to 10 keywords

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
        
        response = {"message": "KeywordMiner AI Competitor Analysis API is running"}
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
            
            domain = url.replace('https://', '').replace('http://', '').split('/')[0]
            
            # Mock competitor data based on domain
            if 'anthropic' in domain.lower():
                competitors = [
                    {'domain': 'openai.com', 'estimated_traffic': 180000000, 'domain_authority': 85},
                    {'domain': 'cohere.ai', 'estimated_traffic': 2500000, 'domain_authority': 72},
                    {'domain': 'huggingface.co', 'estimated_traffic': 25000000, 'domain_authority': 78}
                ]
            elif 'cnn' in domain.lower():
                competitors = [
                    {'domain': 'bbc.com', 'estimated_traffic': 1200000000, 'domain_authority': 95},
                    {'domain': 'reuters.com', 'estimated_traffic': 250000000, 'domain_authority': 88},
                    {'domain': 'nytimes.com', 'estimated_traffic': 400000000, 'domain_authority': 92}
                ]
            else:
                competitors = [
                    {'domain': 'example-competitor1.com', 'estimated_traffic': 50000000, 'domain_authority': 75},
                    {'domain': 'example-competitor2.com', 'estimated_traffic': 30000000, 'domain_authority': 70}
                ]
            
            # Add mock keyword data for competitors
            for comp in competitors:
                comp['total_keywords'] = random.randint(20, 100)
                comp['avg_cpc'] = round(random.uniform(1.0, 4.0), 2)
                comp['total_volume'] = random.randint(100000, 1000000)
                comp['top_keywords'] = generate_mock_keywords(f"https://{comp['domain']}")
            
            response = {
                "target_url": url,
                "region": region,
                "competitors_found": len(competitors),
                "competitors": competitors,
                "keyword_gaps": []  # Simplified for demo
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