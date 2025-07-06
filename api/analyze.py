from http.server import BaseHTTPRequestHandler
import json
import hashlib
import random
import urllib.parse
from typing import List

def analyze_domain_keywords(domain: str) -> List[str]:
    """Extract actual keywords from domain and generate relevant suggestions"""
    domain_lower = domain.lower()
    domain_parts = domain_lower.replace('.com', '').replace('.org', '').replace('.net', '').replace('.io', '').replace('.ai', '').split('.')
    
    # Extract keywords from domain name itself
    brand_keywords = []
    for part in domain_parts:
        if len(part) > 2:  # Ignore very short parts
            brand_keywords.append(part)
    
    # Generate specific keywords for known websites
    if 'anthropic' in domain_lower:
        return [
            # Brand/Direct keywords
            'anthropic', 'anthropic ai', 'anthropic claude', 'anthropic.com',
            # Core product keywords
            'claude ai', 'claude chatbot', 'claude assistant', 'claude api',
            'constitutional ai', 'ai safety', 'responsible ai',
            # Service keywords
            'ai conversation', 'ai writing assistant', 'ai code helper', 'ai research tool',
            # Long-tail informational
            'what is anthropic', 'how to use claude', 'claude vs chatgpt', 'anthropic ai safety',
            'claude ai pricing', 'claude ai capabilities', 'anthropic research papers',
            # Commercial keywords
            'claude ai subscription', 'anthropic enterprise', 'claude for business',
            'ai assistant for teams', 'enterprise ai solutions',
            # Technical keywords
            'large language model', 'constitutional ai training', 'ai alignment research',
            'harmless ai assistant', 'helpful ai chatbot'
        ]
    
    elif 'openai' in domain_lower:
        return [
            'openai', 'openai chatgpt', 'openai api', 'openai.com',
            'chatgpt', 'chatgpt plus', 'chatgpt api', 'gpt-4', 'gpt-3.5',
            'openai dall-e', 'dall-e 2', 'openai codex', 'openai whisper',
            'what is openai', 'how to use chatgpt', 'openai pricing', 'chatgpt vs claude',
            'openai for business', 'chatgpt enterprise', 'openai playground',
            'ai art generator', 'ai image generator', 'ai writing tool',
            'conversational ai', 'generative ai', 'artificial intelligence platform'
        ]
    
    elif any(news in domain_lower for news in ['cnn', 'bbc', 'reuters', 'nytimes', 'fox']):
        news_brand = domain_parts[0] if domain_parts else 'news'
        return [
            # Brand keywords
            news_brand, f'{news_brand} news', f'{news_brand}.com', f'{news_brand} live',
            # Core content
            'breaking news', 'world news', 'politics news', 'business news',
            'technology news', 'sports news', 'entertainment news', 'health news',
            # Long-tail
            f'{news_brand} breaking news', f'{news_brand} politics', f'{news_brand} business',
            f'watch {news_brand} live', f'{news_brand} weather', f'{news_brand} sports',
            'latest news today', 'news headlines', 'current events',
            # Local/specific
            'international news', 'national news', 'local news', 'news analysis',
            'live news updates', 'news alerts', 'trending news'
        ]
    
    elif any(ecom in domain_lower for ecom in ['amazon', 'ebay', 'shopify', 'etsy']):
        brand = domain_parts[0] if domain_parts else 'shop'
        return [
            # Brand keywords
            brand, f'{brand}.com', f'{brand} shopping', f'{brand} store',
            # Core shopping
            'online shopping', 'buy online', 'free shipping', 'best deals',
            'product reviews', 'customer reviews', 'price comparison',
            # Long-tail
            f'buy from {brand}', f'{brand} deals', f'{brand} coupons', f'{brand} sale',
            f'{brand} customer service', f'{brand} return policy',
            'secure checkout', 'order tracking', 'gift cards', 'wishlist',
            # Categories
            'electronics', 'clothing', 'home goods', 'books', 'toys'
        ]
    
    elif any(social in domain_lower for social in ['facebook', 'twitter', 'instagram', 'linkedin', 'tiktok']):
        platform = domain_parts[0] if domain_parts else 'social'
        return [
            platform, f'{platform}.com', f'{platform} app', f'{platform} login',
            f'{platform} profile', f'{platform} page', f'{platform} account',
            'social media', 'social network', 'connect with friends', 'share photos',
            f'how to use {platform}', f'{platform} for business', f'{platform} marketing',
            f'{platform} advertising', f'{platform} analytics', f'{platform} tips',
            'social media management', 'content creation', 'influencer marketing',
            'social engagement', 'viral content', 'social media strategy'
        ]
    
    # Generic analysis for any domain
    else:
        # Extract meaningful parts from domain
        domain_keywords = []
        main_domain = domain_parts[0] if domain_parts else domain_lower.split('.')[0]
        
        # Generate keywords based on domain structure
        domain_keywords.extend([
            # Brand/Direct
            main_domain, f'{main_domain}.com', f'{main_domain} website',
            f'{main_domain} company', f'{main_domain} official site',
            
            # Service-based
            f'{main_domain} services', f'{main_domain} solutions', f'{main_domain} platform',
            f'{main_domain} app', f'{main_domain} software', f'{main_domain} tool',
            
            # Informational
            f'what is {main_domain}', f'how to use {main_domain}', f'{main_domain} review',
            f'{main_domain} pricing', f'{main_domain} features', f'{main_domain} demo',
            
            # Commercial
            f'{main_domain} login', f'{main_domain} sign up', f'{main_domain} free trial',
            f'{main_domain} subscription', f'{main_domain} premium', f'{main_domain} pro',
            
            # Support/Help
            f'{main_domain} support', f'{main_domain} help', f'{main_domain} tutorial',
            f'{main_domain} guide', f'{main_domain} documentation', f'{main_domain} api'
        ])
        
        return domain_keywords

def get_intelligent_keywords(domain: str) -> List[str]:
    """Generate comprehensive keyword suggestions including actual site keywords"""
    
    # Get domain-specific keywords
    domain_keywords = analyze_domain_keywords(domain)
    
    # Add industry context keywords based on domain analysis
    domain_lower = domain.lower()
    industry_keywords = []
    
    # AI/ML Companies
    if any(keyword in domain_lower for keyword in ['anthropic', 'openai', 'ai', 'ml', 'claude']):
        industry_keywords = [
            'artificial intelligence', 'machine learning', 'deep learning', 'neural networks',
            'natural language processing', 'computer vision', 'generative ai',
            'ai ethics', 'machine intelligence', 'automated reasoning', 'ai research'
        ]
    
    # News/Media Companies
    elif any(keyword in domain_lower for keyword in ['cnn', 'bbc', 'news', 'times', 'reuters', 'fox', 'nbc', 'abc']):
        industry_keywords = [
            'journalism', 'media coverage', 'news reporting', 'press freedom',
            'editorial content', 'investigative journalism', 'news anchor',
            'breaking news alerts', 'live coverage', 'news network'
        ]
    
    # E-commerce
    elif any(keyword in domain_lower for keyword in ['shop', 'store', 'buy', 'commerce', 'market']):
        industry_keywords = [
            'e-commerce platform', 'online marketplace', 'digital commerce',
            'retail technology', 'shopping experience', 'payment processing',
            'inventory management', 'customer service', 'logistics', 'fulfillment'
        ]
    
    # Technology/Software
    elif any(keyword in domain_lower for keyword in ['tech', 'software', 'app', 'digital', 'cloud', 'data']):
        industry_keywords = [
            'software development', 'cloud computing', 'data analytics', 'cybersecurity',
            'digital transformation', 'enterprise software', 'saas platform',
            'api integration', 'tech innovation', 'automation tools'
        ]
    
    # Default industry keywords for unknown domains
    else:
        industry_keywords = [
            'business solutions', 'professional services', 'digital services',
            'customer experience', 'industry expertise', 'innovation',
            'technology solutions', 'service excellence', 'market leader'
        ]
    
    # Combine domain-specific and industry keywords
    all_keywords = domain_keywords + industry_keywords
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for keyword in all_keywords:
        if keyword not in seen:
            seen.add(keyword)
            unique_keywords.append(keyword)
    
    return unique_keywords

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