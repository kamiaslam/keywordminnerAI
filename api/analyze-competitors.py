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
                {'domain': 'openai.com', 'name': 'OpenAI', 'estimated_traffic': 180000000, 'domain_authority': 85, 'description': 'Creator of ChatGPT and GPT models'},
                {'domain': 'cohere.ai', 'name': 'Cohere', 'estimated_traffic': 2500000, 'domain_authority': 72, 'description': 'Enterprise AI platform'},
                {'domain': 'huggingface.co', 'name': 'Hugging Face', 'estimated_traffic': 25000000, 'domain_authority': 78, 'description': 'Open-source AI community'},
                {'domain': 'stability.ai', 'name': 'Stability AI', 'estimated_traffic': 8000000, 'domain_authority': 68, 'description': 'Creator of Stable Diffusion'}
            ]
        
        # News/Media Companies
        elif any(keyword in domain_lower for keyword in ['cnn', 'bbc', 'news', 'times', 'reuters', 'fox', 'nbc', 'abc']):
            return [
                {'domain': 'bbc.com', 'name': 'BBC News', 'estimated_traffic': 1200000000, 'domain_authority': 95, 'description': 'British Broadcasting Corporation'},
                {'domain': 'cnn.com', 'name': 'CNN', 'estimated_traffic': 800000000, 'domain_authority': 92, 'description': 'Cable News Network'},
                {'domain': 'reuters.com', 'name': 'Reuters', 'estimated_traffic': 250000000, 'domain_authority': 88, 'description': 'International news agency'},
                {'domain': 'nytimes.com', 'name': 'The New York Times', 'estimated_traffic': 400000000, 'domain_authority': 92, 'description': 'American newspaper'}
            ]
        
        # E-commerce/Shopping
        elif any(keyword in domain_lower for keyword in ['amazon', 'shop', 'store', 'buy', 'mart', 'commerce', 'ebay']):
            return [
                {'domain': 'amazon.com', 'name': 'Amazon', 'estimated_traffic': 2500000000, 'domain_authority': 96, 'description': 'Global e-commerce marketplace'},
                {'domain': 'ebay.com', 'name': 'eBay', 'estimated_traffic': 850000000, 'domain_authority': 92, 'description': 'Online auction platform'},
                {'domain': 'shopify.com', 'name': 'Shopify', 'estimated_traffic': 120000000, 'domain_authority': 91, 'description': 'E-commerce platform'},
                {'domain': 'etsy.com', 'name': 'Etsy', 'estimated_traffic': 400000000, 'domain_authority': 91, 'description': 'Handmade & vintage marketplace'}
            ]
        
        # Social Media/Tech
        elif any(keyword in domain_lower for keyword in ['facebook', 'twitter', 'instagram', 'social', 'meta', 'tiktok']):
            return [
                {'domain': 'facebook.com', 'name': 'Facebook', 'estimated_traffic': 2200000000, 'domain_authority': 96, 'description': 'Social networking platform'},
                {'domain': 'twitter.com', 'name': 'Twitter', 'estimated_traffic': 800000000, 'domain_authority': 94, 'description': 'Microblogging platform'},
                {'domain': 'instagram.com', 'name': 'Instagram', 'estimated_traffic': 1500000000, 'domain_authority': 95, 'description': 'Photo sharing platform'},
                {'domain': 'linkedin.com', 'name': 'LinkedIn', 'estimated_traffic': 900000000, 'domain_authority': 98, 'description': 'Professional networking'}
            ]
        
        # Streaming/Entertainment
        elif any(keyword in domain_lower for keyword in ['netflix', 'youtube', 'stream', 'video', 'music', 'spotify']):
            return [
                {'domain': 'netflix.com', 'name': 'Netflix', 'estimated_traffic': 800000000, 'domain_authority': 93, 'description': 'Streaming entertainment service'},
                {'domain': 'youtube.com', 'name': 'YouTube', 'estimated_traffic': 8000000000, 'domain_authority': 100, 'description': 'Video sharing platform'},
                {'domain': 'hulu.com', 'name': 'Hulu', 'estimated_traffic': 180000000, 'domain_authority': 89, 'description': 'TV streaming service'},
                {'domain': 'disneyplus.com', 'name': 'Disney+', 'estimated_traffic': 120000000, 'domain_authority': 78, 'description': 'Disney streaming service'}
            ]
        
        # Financial/Banking
        elif any(keyword in domain_lower for keyword in ['bank', 'finance', 'pay', 'credit', 'invest', 'money']):
            return [
                {'domain': 'chase.com', 'name': 'JPMorgan Chase', 'estimated_traffic': 200000000, 'domain_authority': 89, 'description': 'Major American bank'},
                {'domain': 'bankofamerica.com', 'name': 'Bank of America', 'estimated_traffic': 180000000, 'domain_authority': 88, 'description': 'Global banking corporation'},
                {'domain': 'paypal.com', 'name': 'PayPal', 'estimated_traffic': 650000000, 'domain_authority': 92, 'description': 'Digital payment platform'},
                {'domain': 'wells.com', 'name': 'Wells Fargo', 'estimated_traffic': 120000000, 'domain_authority': 85, 'description': 'Diversified financial services'}
            ]
        
        # Education/Learning
        elif any(keyword in domain_lower for keyword in ['edu', 'university', 'school', 'learn', 'course', 'academy']):
            return [
                {'domain': 'coursera.org', 'name': 'Coursera', 'estimated_traffic': 180000000, 'domain_authority': 87, 'description': 'Online learning platform'},
                {'domain': 'edx.org', 'name': 'edX', 'estimated_traffic': 45000000, 'domain_authority': 82, 'description': 'University-level online courses'},
                {'domain': 'udemy.com', 'name': 'Udemy', 'estimated_traffic': 120000000, 'domain_authority': 85, 'description': 'Online course marketplace'},
                {'domain': 'khanacademy.org', 'name': 'Khan Academy', 'estimated_traffic': 80000000, 'domain_authority': 89, 'description': 'Free online education'}
            ]
        
        # Travel/Booking
        elif any(keyword in domain_lower for keyword in ['travel', 'hotel', 'booking', 'flight', 'trip', 'airbnb']):
            return [
                {'domain': 'booking.com', 'name': 'Booking.com', 'estimated_traffic': 650000000, 'domain_authority': 91, 'description': 'Hotel booking platform'},
                {'domain': 'expedia.com', 'name': 'Expedia', 'estimated_traffic': 180000000, 'domain_authority': 88, 'description': 'Travel booking service'},
                {'domain': 'airbnb.com', 'name': 'Airbnb', 'estimated_traffic': 400000000, 'domain_authority': 92, 'description': 'Vacation rental marketplace'},
                {'domain': 'tripadvisor.com', 'name': 'TripAdvisor', 'estimated_traffic': 300000000, 'domain_authority': 89, 'description': 'Travel review platform'}
            ]
        
        # Health/Medical
        elif any(keyword in domain_lower for keyword in ['health', 'medical', 'doctor', 'medicine', 'pharma', 'clinic']):
            return [
                {'domain': 'webmd.com', 'name': 'WebMD', 'estimated_traffic': 180000000, 'domain_authority': 88, 'description': 'Health information website'},
                {'domain': 'mayoclinic.org', 'name': 'Mayo Clinic', 'estimated_traffic': 120000000, 'domain_authority': 89, 'description': 'Medical center & research'},
                {'domain': 'healthline.com', 'name': 'Healthline', 'estimated_traffic': 200000000, 'domain_authority': 85, 'description': 'Health information platform'},
                {'domain': 'nih.gov', 'name': 'NIH', 'estimated_traffic': 80000000, 'domain_authority': 92, 'description': 'National Institutes of Health'}
            ]
        
        # Food/Restaurant
        elif any(keyword in domain_lower for keyword in ['food', 'restaurant', 'recipe', 'cook', 'eat', 'delivery']):
            return [
                {'domain': 'ubereats.com', 'name': 'Uber Eats', 'estimated_traffic': 150000000, 'domain_authority': 78, 'description': 'Food delivery service'},
                {'domain': 'doordash.com', 'name': 'DoorDash', 'estimated_traffic': 120000000, 'domain_authority': 76, 'description': 'Restaurant delivery platform'},
                {'domain': 'grubhub.com', 'name': 'Grubhub', 'estimated_traffic': 80000000, 'domain_authority': 75, 'description': 'Online food ordering'},
                {'domain': 'allrecipes.com', 'name': 'Allrecipes', 'estimated_traffic': 100000000, 'domain_authority': 82, 'description': 'Recipe sharing community'}
            ]
        
        # Generic business competitors based on domain characteristics
        else:
            # Try to categorize based on domain extension and generate relevant competitors
            if domain_lower.endswith('.org'):
                return [
                    {'domain': 'wikipedia.org', 'name': 'Wikipedia', 'estimated_traffic': 1800000000, 'domain_authority': 93, 'description': 'Free online encyclopedia'},
                    {'domain': 'archive.org', 'name': 'Internet Archive', 'estimated_traffic': 80000000, 'domain_authority': 91, 'description': 'Digital library'},
                    {'domain': 'mozilla.org', 'name': 'Mozilla', 'estimated_traffic': 45000000, 'domain_authority': 89, 'description': 'Open-source software'}
                ]
            elif domain_lower.endswith('.gov'):
                return [
                    {'domain': 'usa.gov', 'name': 'USA.gov', 'estimated_traffic': 25000000, 'domain_authority': 92, 'description': 'Official US government portal'},
                    {'domain': 'irs.gov', 'name': 'IRS', 'estimated_traffic': 180000000, 'domain_authority': 89, 'description': 'Internal Revenue Service'},
                    {'domain': 'cdc.gov', 'name': 'CDC', 'estimated_traffic': 120000000, 'domain_authority': 91, 'description': 'Centers for Disease Control'}
                ]
            else:
                # Generate industry-relevant competitors with proper names
                main_domain = domain_lower.split('.')[0]
                base_competitors = [
                    {'domain': f'{main_domain}-alternative.com', 'name': f'{main_domain.title()} Alternative', 'estimated_traffic': random.randint(5000000, 50000000), 'domain_authority': random.randint(65, 85), 'description': f'Alternative to {main_domain}'},
                    {'domain': f'best-{main_domain}.com', 'name': f'Best {main_domain.title()}', 'estimated_traffic': random.randint(3000000, 25000000), 'domain_authority': random.randint(60, 80), 'description': f'Top {main_domain} service'},
                    {'domain': f'{main_domain}-pro.com', 'name': f'{main_domain.title()} Pro', 'estimated_traffic': random.randint(2000000, 20000000), 'domain_authority': random.randint(55, 75), 'description': f'Professional {main_domain} platform'}
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