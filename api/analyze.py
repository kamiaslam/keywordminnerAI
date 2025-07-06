from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from typing import List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from api.seo_apis import SEODataProvider
    seo_provider = SEODataProvider()
except ImportError:
    try:
        from seo_apis import SEODataProvider
        seo_provider = SEODataProvider()
    except ImportError:
        # Fallback if import fails
        seo_provider = None

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
        
        response = {"message": "KeywordMiner AI - Real SEO Data API"}
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
            
            if not seo_provider:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"error": "SEO provider not available"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Extract real keywords using SEO APIs
            analysis_result = seo_provider.extract_keywords_from_content(url)
            
            # Prepare response data
            keywords = analysis_result.get('extracted_keywords', [])
            suggestions = analysis_result.get('suggestions', [])
            
            # Add long-tail suggestions to main keywords list
            for suggestion in suggestions:
                suggestion_data = seo_provider.generate_realistic_metrics(suggestion)
                keywords.append(suggestion_data)
            
            # Sort by volume
            keywords.sort(key=lambda x: x.get('volume', 0), reverse=True)
            
            # Limit to top 50 keywords
            keywords = keywords[:50]
            
            # Calculate totals
            total_volume = sum(k.get('volume', 0) for k in keywords)
            avg_cpc = round(sum(k.get('cpc', 0) for k in keywords) / len(keywords), 2) if keywords else 0
            
            # Generate actionable long-tail suggestions for content creation
            long_tail_suggestions = self.generate_content_suggestions(analysis_result.get('domain', ''), suggestions)
            
            response = {
                "url": url,
                "region": region,
                "keywords_found": len(keywords),
                "keywords": keywords,
                "total_volume": total_volume,
                "avg_cpc": avg_cpc,
                "long_tail_suggestions": long_tail_suggestions,
                "data_source": "Real SEO APIs + Google Search Data",
                "extraction_method": "SERP Analysis + Autocomplete"
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
            response = {"error": f"Analysis failed: {str(e)}"}
            self.wfile.write(json.dumps(response).encode())
    
    def generate_content_suggestions(self, domain: str, base_suggestions: List[str]) -> List[str]:
        """Generate 10 actionable long-tail keywords for content creation"""
        domain_name = domain.split('.')[0] if domain else 'website'
        
        # Mix of real suggestions and strategic content ideas
        content_suggestions = []
        
        # Add real Google suggestions (cleaned up)
        for suggestion in base_suggestions[:5]:
            if len(suggestion.split()) >= 3:  # Only long-tail
                content_suggestions.append(suggestion)
        
        # Add strategic content keywords
        strategic_keywords = [
            f"how to get started with {domain_name}",
            f"{domain_name} step by step guide",
            f"complete {domain_name} tutorial",
            f"{domain_name} best practices 2025",
            f"common {domain_name} mistakes to avoid",
            f"{domain_name} tips for beginners",
            f"advanced {domain_name} strategies",
            f"{domain_name} vs alternatives comparison",
            f"why choose {domain_name} over competitors",
            f"{domain_name} pricing guide and plans"
        ]
        
        # Fill up to 10 suggestions
        for keyword in strategic_keywords:
            if len(content_suggestions) >= 10:
                break
            if keyword not in content_suggestions:
                content_suggestions.append(keyword)
        
        return content_suggestions[:10]