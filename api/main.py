from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import hashlib
import random

app = FastAPI(title="KeywordMiner AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str
    region: Optional[str] = "auto"
    email: Optional[str] = None

class KeywordResult(BaseModel):
    keyword: str
    volume: Optional[int] = None
    cpc: Optional[float] = None
    competition: Optional[str] = None
    competition_score: Optional[float] = None
    trend: Optional[str] = None
    type: str
    intent: str
    count: Optional[int] = None

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

@app.get("/")
async def root():
    return {"message": "KeywordMiner AI API is running"}

@app.post("/analyze")
async def analyze_website(request: AnalyzeRequest):
    try:
        # Generate mock keywords for demo
        keywords = generate_mock_keywords(request.url, request.region)
        
        # Convert to KeywordResult format
        results = []
        for kw in keywords:
            result = KeywordResult(**kw)
            results.append(result)
        
        # Sort by volume
        results.sort(key=lambda x: x.volume or 0, reverse=True)
        
        return {
            "url": request.url,
            "region": request.region,
            "keywords_found": len(results),
            "keywords": [r.dict() for r in results],
            "total_volume": sum(r.volume or 0 for r in results),
            "avg_cpc": round(sum(r.cpc or 0 for r in results) / len(results), 2) if results else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-competitors")
async def analyze_competitors(request: AnalyzeRequest):
    try:
        domain = request.url.replace('https://', '').replace('http://', '').split('/')[0]
        
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
            comp['top_keywords'] = generate_mock_keywords(f"https://{comp['domain']}")[:10]
        
        return {
            "target_url": request.url,
            "region": request.region,
            "competitors_found": len(competitors),
            "competitors": competitors,
            "keyword_gaps": []  # Simplified for demo
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/regions")
async def get_supported_regions():
    return {
        "regions": [
            {"code": "us", "name": "United States"},
            {"code": "uk", "name": "United Kingdom"},
            {"code": "ae", "name": "United Arab Emirates"},
            {"code": "au", "name": "Australia"},
            {"code": "ca", "name": "Canada"},
            {"code": "in", "name": "India"},
            {"code": "global", "name": "Global"}
        ]
    }