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
    def get_intelligent_competitors(self, domain):
        """Intelligent competitor detection based on domain analysis"""
        domain_lower = domain.lower()
        
        # AI/ML Companies
        if any(keyword in domain_lower for keyword in ['anthropic', 'openai', 'ai', 'ml', 'claude']):
            return [
                {'domain': 'openai.com', 'estimated_traffic': 180000000, 'domain_authority': 85},
                {'domain': 'cohere.ai', 'estimated_traffic': 2500000, 'domain_authority': 72},
                {'domain': 'huggingface.co', 'estimated_traffic': 25000000, 'domain_authority': 78},
                {'domain': 'stability.ai', 'estimated_traffic': 8000000, 'domain_authority': 68}
            ]
        
        # News/Media Companies
        elif any(keyword in domain_lower for keyword in ['cnn', 'bbc', 'news', 'times', 'reuters', 'fox', 'nbc', 'abc']):
            return [
                {'domain': 'bbc.com', 'estimated_traffic': 1200000000, 'domain_authority': 95},
                {'domain': 'cnn.com', 'estimated_traffic': 800000000, 'domain_authority': 92},
                {'domain': 'reuters.com', 'estimated_traffic': 250000000, 'domain_authority': 88},
                {'domain': 'nytimes.com', 'estimated_traffic': 400000000, 'domain_authority': 92}
            ]
        
        # E-commerce/Shopping
        elif any(keyword in domain_lower for keyword in ['amazon', 'shop', 'store', 'buy', 'mart', 'commerce', 'ebay']):
            return [
                {'domain': 'amazon.com', 'estimated_traffic': 2500000000, 'domain_authority': 96},
                {'domain': 'ebay.com', 'estimated_traffic': 850000000, 'domain_authority': 92},
                {'domain': 'shopify.com', 'estimated_traffic': 120000000, 'domain_authority': 91},
                {'domain': 'etsy.com', 'estimated_traffic': 400000000, 'domain_authority': 91}
            ]
        
        # Social Media/Tech
        elif any(keyword in domain_lower for keyword in ['facebook', 'twitter', 'instagram', 'social', 'meta', 'tiktok']):
            return [
                {'domain': 'facebook.com', 'estimated_traffic': 2200000000, 'domain_authority': 96},
                {'domain': 'twitter.com', 'estimated_traffic': 800000000, 'domain_authority': 94},
                {'domain': 'instagram.com', 'estimated_traffic': 1500000000, 'domain_authority': 95},
                {'domain': 'linkedin.com', 'estimated_traffic': 900000000, 'domain_authority': 98}
            ]
        
        # Streaming/Entertainment
        elif any(keyword in domain_lower for keyword in ['netflix', 'youtube', 'stream', 'video', 'music', 'spotify']):
            return [
                {'domain': 'netflix.com', 'estimated_traffic': 800000000, 'domain_authority': 93},
                {'domain': 'youtube.com', 'estimated_traffic': 8000000000, 'domain_authority': 100},
                {'domain': 'hulu.com', 'estimated_traffic': 180000000, 'domain_authority': 89},
                {'domain': 'disneyplus.com', 'estimated_traffic': 120000000, 'domain_authority': 78}
            ]
        
        # Financial/Banking
        elif any(keyword in domain_lower for keyword in ['bank', 'finance', 'pay', 'credit', 'invest', 'money']):
            return [
                {'domain': 'chase.com', 'estimated_traffic': 200000000, 'domain_authority': 89},
                {'domain': 'bankofamerica.com', 'estimated_traffic': 180000000, 'domain_authority': 88},
                {'domain': 'paypal.com', 'estimated_traffic': 650000000, 'domain_authority': 92},
                {'domain': 'wells.com', 'estimated_traffic': 120000000, 'domain_authority': 85}
            ]
        
        # Education/Learning
        elif any(keyword in domain_lower for keyword in ['edu', 'university', 'school', 'learn', 'course', 'academy']):
            return [
                {'domain': 'coursera.org', 'estimated_traffic': 180000000, 'domain_authority': 87},
                {'domain': 'edx.org', 'estimated_traffic': 45000000, 'domain_authority': 82},
                {'domain': 'udemy.com', 'estimated_traffic': 120000000, 'domain_authority': 85},
                {'domain': 'khanacademy.org', 'estimated_traffic': 80000000, 'domain_authority': 89}
            ]
        
        # Travel/Booking
        elif any(keyword in domain_lower for keyword in ['travel', 'hotel', 'booking', 'flight', 'trip', 'airbnb']):
            return [
                {'domain': 'booking.com', 'estimated_traffic': 650000000, 'domain_authority': 91},
                {'domain': 'expedia.com', 'estimated_traffic': 180000000, 'domain_authority': 88},
                {'domain': 'airbnb.com', 'estimated_traffic': 400000000, 'domain_authority': 92},
                {'domain': 'tripadvisor.com', 'estimated_traffic': 300000000, 'domain_authority': 89}
            ]
        
        # Health/Medical
        elif any(keyword in domain_lower for keyword in ['health', 'medical', 'doctor', 'medicine', 'pharma', 'clinic']):
            return [
                {'domain': 'webmd.com', 'estimated_traffic': 180000000, 'domain_authority': 88},
                {'domain': 'mayoclinic.org', 'estimated_traffic': 120000000, 'domain_authority': 89},
                {'domain': 'healthline.com', 'estimated_traffic': 200000000, 'domain_authority': 85},
                {'domain': 'nih.gov', 'estimated_traffic': 80000000, 'domain_authority': 92}
            ]
        
        # Food/Restaurant
        elif any(keyword in domain_lower for keyword in ['food', 'restaurant', 'recipe', 'cook', 'eat', 'delivery']):
            return [
                {'domain': 'ubereats.com', 'estimated_traffic': 150000000, 'domain_authority': 78},
                {'domain': 'doordash.com', 'estimated_traffic': 120000000, 'domain_authority': 76},
                {'domain': 'grubhub.com', 'estimated_traffic': 80000000, 'domain_authority': 75},
                {'domain': 'allrecipes.com', 'estimated_traffic': 100000000, 'domain_authority': 82}
            ]
        
        # Generic business competitors based on domain characteristics
        else:
            # Try to categorize based on domain extension and generate relevant competitors
            if domain_lower.endswith('.org'):
                return [
                    {'domain': 'wikipedia.org', 'estimated_traffic': 1800000000, 'domain_authority': 93},
                    {'domain': 'archive.org', 'estimated_traffic': 80000000, 'domain_authority': 91},
                    {'domain': 'mozilla.org', 'estimated_traffic': 45000000, 'domain_authority': 89}
                ]
            elif domain_lower.endswith('.gov'):
                return [
                    {'domain': 'usa.gov', 'estimated_traffic': 25000000, 'domain_authority': 92},
                    {'domain': 'irs.gov', 'estimated_traffic': 180000000, 'domain_authority': 89},
                    {'domain': 'cdc.gov', 'estimated_traffic': 120000000, 'domain_authority': 91}
                ]
            else:
                # Generate industry-relevant competitors based on common business patterns
                base_competitors = [
                    {'domain': f'{domain_lower.replace(".com", "")}-alternative.com', 'estimated_traffic': random.randint(5000000, 50000000), 'domain_authority': random.randint(65, 85)},
                    {'domain': f'best-{domain_lower.split(".")[0]}.com', 'estimated_traffic': random.randint(3000000, 25000000), 'domain_authority': random.randint(60, 80)},
                    {'domain': f'{domain_lower.split(".")[0]}-competitor.com', 'estimated_traffic': random.randint(2000000, 20000000), 'domain_authority': random.randint(55, 75)}
                ]
                return base_competitors

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
            
            # Intelligent competitor detection based on domain patterns and industry
            competitors = self.get_intelligent_competitors(domain)
            
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