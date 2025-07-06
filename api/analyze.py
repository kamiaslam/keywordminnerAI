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
        # Add base keyword
        volume = random.randint(1000, 50000)
        cpc = round(random.uniform(0.5, 5.0), 2)
        competition = random.choice(['Low', 'Medium', 'High'])
        
        keywords.append({
            'keyword': base,
            'volume': volume,
            'cpc': cpc,
            'competition': competition,
            'competition_score': round(random.uniform(0.1, 1.0), 2),
            'trend': random.choice(['Rising', 'Stable', 'Declining', 'Seasonal']),
            'type': 'short-tail',
            'intent': 'informational',
            'count': random.randint(1, 10)
        })
        
        # Add long-tail variations
        variations = [f"best {base}", f"how to {base}", f"{base} guide", f"{base} tips"]
        for var in variations[:2]:
            keywords.append({
                'keyword': var,
                'volume': random.randint(100, 5000),
                'cpc': round(random.uniform(0.3, 3.0), 2),
                'competition': random.choice(['Low', 'Medium']),
                'competition_score': round(random.uniform(0.1, 0.7), 2),
                'trend': random.choice(['Rising', 'Stable', 'Declining']),
                'type': 'long-tail',
                'intent': random.choice(['informational', 'commercial']),
                'count': random.randint(1, 5)
            })
    
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