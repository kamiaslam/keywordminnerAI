from http.server import BaseHTTPRequestHandler
import json
import hashlib
import random
import urllib.parse
from typing import List, Dict
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from api.scraper import WebsiteScraper
    scraper = WebsiteScraper()
except:
    # Fallback if scraper import fails
    scraper = None

def analyze_website_keywords(url: str) -> Dict:
    """Analyze actual website content and extract keywords"""
    
    if not scraper:
        # If scraper is not available, use fallback
        return generate_fallback_keywords(url)
    
    try:
        # Scrape the website
        content = scraper.scrape_website(url)
        
        if not content:
            # Fallback to basic analysis if scraping fails
            return generate_fallback_keywords(url)
        
        # Extract keywords from content
        extracted_keywords = scraper.extract_keywords(content)
        
        # Generate suggestions
        domain = url.replace('https://', '').replace('http://', '').split('/')[0]
        suggestions = scraper.generate_keyword_suggestions(domain, extracted_keywords)
        
        return suggestions
    except:
        # If any error occurs, use fallback
        return generate_fallback_keywords(url)

def generate_fallback_keywords(url: str) -> Dict:
    """Fallback keyword generation if scraping fails"""
    domain = url.replace('https://', '').replace('http://', '').split('/')[0]
    domain_name = domain.split('.')[0]
    
    # Basic keywords based on domain
    basic_keywords = [
        {'keyword': domain_name, 'count': 50, 'type': 'single'},
        {'keyword': f'{domain_name} services', 'count': 30, 'type': 'phrase'},
        {'keyword': f'{domain_name} platform', 'count': 25, 'type': 'phrase'},
        {'keyword': f'{domain_name} solutions', 'count': 20, 'type': 'phrase'},
        {'keyword': f'{domain_name} features', 'count': 15, 'type': 'phrase'}
    ]
    
    # Long-tail suggestions
    long_tail_suggestions = [
        f"what is {domain_name}",
        f"how to use {domain_name}",
        f"{domain_name} pricing and plans",
        f"{domain_name} vs competitors",
        f"{domain_name} customer reviews",
        f"getting started with {domain_name}",
        f"{domain_name} best practices",
        f"{domain_name} tutorial for beginners",
        f"benefits of using {domain_name}",
        f"{domain_name} alternatives comparison"
    ]
    
    return {
        'extracted_keywords': basic_keywords,
        'long_tail_suggestions': long_tail_suggestions,
        'top_keywords': [kw['keyword'] for kw in basic_keywords[:5]]
    }

def generate_keyword_metrics(keyword: str, base_volume: int = None) -> Dict:
    """Generate realistic metrics for a keyword"""
    word_count = len(keyword.split())
    
    # Base volume calculation
    if not base_volume:
        if word_count == 1:
            base_volume = random.randint(5000, 50000)
        elif word_count == 2:
            base_volume = random.randint(1000, 15000)
        elif word_count == 3:
            base_volume = random.randint(100, 5000)
        else:
            base_volume = random.randint(10, 1000)
    
    # CPC calculation based on word count and intent
    if any(word in keyword.lower() for word in ['buy', 'price', 'cost', 'cheap', 'discount']):
        base_cpc = random.uniform(2.0, 8.0)
    elif any(word in keyword.lower() for word in ['how', 'what', 'why', 'when']):
        base_cpc = random.uniform(0.5, 3.0)
    else:
        base_cpc = random.uniform(1.0, 5.0)
    
    # Competition determination
    if base_volume > 10000:
        competition = random.choice(['High', 'High', 'Medium'])
    elif base_volume > 1000:
        competition = random.choice(['Medium', 'Medium', 'Low'])
    else:
        competition = random.choice(['Low', 'Low', 'Medium'])
    
    # Intent determination
    if any(word in keyword.lower() for word in ['buy', 'price', 'cost', 'purchase', 'order']):
        intent = 'commercial'
    elif any(word in keyword.lower() for word in ['how', 'what', 'why', 'guide', 'tutorial']):
        intent = 'informational'
    elif any(word in keyword.lower() for word in ['login', 'sign in', 'account']):
        intent = 'navigational'
    else:
        intent = 'informational'
    
    # Keyword type
    if word_count == 1:
        keyword_type = 'short-tail'
    elif word_count <= 3:
        keyword_type = 'mid-tail'
    else:
        keyword_type = 'long-tail'
    
    return {
        'keyword': keyword,
        'volume': base_volume,
        'cpc': round(base_cpc, 2),
        'competition': competition,
        'competition_score': round(random.uniform(0.1, 1.0), 2),
        'trend': random.choice(['Rising', 'Stable', 'Declining', 'Seasonal']),
        'type': keyword_type,
        'intent': intent
    }

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
            
            # Analyze the actual website
            analysis_result = analyze_website_keywords(url)
            
            # Convert extracted keywords to full keyword objects with metrics
            keywords = []
            for kw in analysis_result['extracted_keywords']:
                keyword_data = generate_keyword_metrics(kw['keyword'], kw.get('count', 1) * 100)
                keywords.append(keyword_data)
            
            # Add long-tail suggestions with metrics
            for suggestion in analysis_result['long_tail_suggestions']:
                keyword_data = generate_keyword_metrics(suggestion)
                keywords.append(keyword_data)
            
            # Sort by volume
            keywords.sort(key=lambda x: x.get('volume', 0), reverse=True)
            
            # Calculate totals
            total_volume = sum(k.get('volume', 0) for k in keywords)
            avg_cpc = round(sum(k.get('cpc', 0) for k in keywords) / len(keywords), 2) if keywords else 0
            
            response = {
                "url": url,
                "region": region,
                "keywords_found": len(keywords),
                "keywords": keywords[:50],  # Limit to 50 keywords
                "total_volume": total_volume,
                "avg_cpc": avg_cpc,
                "long_tail_suggestions": analysis_result['long_tail_suggestions'],
                "top_extracted": analysis_result.get('top_keywords', [])
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