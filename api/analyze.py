from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from typing import List, Dict

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from api.seo_apis import SEODataProvider
    from api.google_trends_api import GoogleTrendsAPI
    seo_provider = SEODataProvider()
    trends_api = GoogleTrendsAPI()
except ImportError:
    try:
        from seo_apis import SEODataProvider
        from google_trends_api import GoogleTrendsAPI
        seo_provider = SEODataProvider()
        trends_api = GoogleTrendsAPI()
    except ImportError:
        # Fallback if import fails
        seo_provider = None
        trends_api = None

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
            
            if not seo_provider or not trends_api:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"error": "SEO provider not available"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Extract domain for keyword generation
            domain = url.replace('https://', '').replace('http://', '').split('/')[0]
            domain_name = domain.split('.')[0]
            
            # Get Google Trends style data for main keywords
            main_keywords = [
                domain_name,
                f"{domain_name} features",
                f"{domain_name} pricing", 
                f"{domain_name} reviews",
                f"what is {domain_name}"
            ]
            
            keywords = []
            for keyword in main_keywords:
                trends_data = trends_api.get_google_trends_data(keyword, region)
                keyword_info = {
                    'keyword': keyword,
                    'volume': trends_data['search_volume']['monthly_searches'],
                    'cpc': trends_data['suggested_bid']['suggested_bid'],
                    'competition': trends_data['competition_level']['level'],
                    'competition_score': trends_data['competition_level']['score'],
                    'trend': trends_data['seasonal_patterns']['volatility'],
                    'type': 'branded' if domain_name in keyword else 'generic',
                    'intent': trends_data['search_intent']['primary_intent'],
                    'difficulty': trends_data['competition_level']['difficulty_rating'],
                    'trend_data': trends_data['trend_data'],
                    'related_queries': trends_data['related_queries'][:5],
                    'regional_interest': trends_data['interest_by_region'][:5]
                }
                keywords.append(keyword_info)
            
            # Get additional keyword ideas using Google Keyword Planner style
            keyword_ideas = trends_api.get_keyword_ideas(domain_name, region)
            for idea in keyword_ideas[:15]:  # Add top 15 keyword ideas
                idea['trend_data'] = []  # Keep response size manageable
                idea['related_queries'] = []
                idea['regional_interest'] = []
                keywords.append(idea)
            
            # Sort by volume
            keywords.sort(key=lambda x: x.get('volume', 0), reverse=True)
            
            # Limit to top 30 keywords for better performance
            keywords = keywords[:30]
            
            # Calculate totals
            total_volume = sum(k.get('volume', 0) for k in keywords)
            avg_cpc = round(sum(k.get('cpc', 0) for k in keywords) / len(keywords), 2) if keywords else 0
            
            # Generate actionable long-tail suggestions for content creation
            long_tail_suggestions = self.generate_content_suggestions(domain_name, [k['keyword'] for k in keywords if 'how' in k['keyword'] or 'what' in k['keyword']])
            
            # Get trend overview for main domain keyword
            main_trend_data = None
            if keywords:
                main_keyword = next((k for k in keywords if k['keyword'] == domain_name), keywords[0])
                main_trend_data = main_keyword.get('trend_data', [])
            
            response = {
                "url": url,
                "region": region,
                "keywords_found": len(keywords),
                "keywords": keywords,
                "total_volume": total_volume,
                "avg_cpc": avg_cpc,
                "long_tail_suggestions": long_tail_suggestions,
                "trend_overview": main_trend_data,
                "top_regions": keywords[0].get('regional_interest', []) if keywords else [],
                "data_source": "Google Trends API + Keyword Planner Style Data",
                "extraction_method": "Real SEO Analytics + Trend Analysis",
                "seasonal_insights": self.get_seasonal_insights(keywords)
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
    
    def get_seasonal_insights(self, keywords: List[Dict]) -> Dict:
        """Generate seasonal insights from keyword data"""
        if not keywords:
            return {}
        
        # Get keywords with trend data
        trending_keywords = [k for k in keywords if k.get('trend_data')]
        
        if not trending_keywords:
            return {"message": "No trend data available"}
        
        # Analyze trends
        rising_keywords = [k for k in keywords if k.get('trend', '').lower() == 'rising']
        declining_keywords = [k for k in keywords if k.get('trend', '').lower() == 'declining']
        
        return {
            "total_keywords_analyzed": len(keywords),
            "rising_keywords_count": len(rising_keywords),
            "declining_keywords_count": len(declining_keywords),
            "trend_status": "Growing market" if len(rising_keywords) > len(declining_keywords) else "Stable market",
            "top_rising": [k['keyword'] for k in rising_keywords[:3]],
            "recommendations": [
                "Focus on rising keyword opportunities",
                "Monitor seasonal patterns for content planning", 
                "Target informational keywords for awareness"
            ]
        }