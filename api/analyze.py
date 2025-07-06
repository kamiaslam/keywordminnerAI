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
    return {"message": "KeywordMiner AI Analyze API is running"}

@app.post("/")
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

# Vercel handler
handler = app