from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncio
from backend.scraper import KeywordScraperAgent
from backend.nlp_engine import NLPKeywordEngine
from backend.keyword_metrics import KeywordMetricsService
from backend.competitor_analysis import CompetitorAnalysisService
import logging
import traceback

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

@app.get("/")
async def root():
    return {"message": "KeywordMiner AI API is running"}

@app.post("/analyze")
async def analyze_website(request: AnalyzeRequest):
    try:
        scraper = KeywordScraperAgent()
        content = await scraper.scrape_website(request.url)
        
        nlp_engine = NLPKeywordEngine()
        keywords = nlp_engine.extract_keywords(content)
        
        metrics_service = KeywordMetricsService()
        
        results = []
        for keyword in keywords:
            # Get metrics for each keyword
            metrics = metrics_service.get_keyword_metrics(keyword['keyword'], request.region)
            
            result = KeywordResult(
                keyword=keyword['keyword'],
                volume=metrics['volume'],
                cpc=metrics['cpc'],
                competition=metrics['competition'],
                competition_score=metrics['competition_score'],
                trend=metrics['trend'],
                type=keyword['type'],
                intent=keyword['intent'],
                count=keyword.get('count', 0)
            )
            results.append(result)
        
        # Sort by volume (highest first)
        results.sort(key=lambda x: x.volume or 0, reverse=True)
        
        return {
            "url": request.url,
            "region": request.region,
            "keywords_found": len(results),
            "keywords": results,
            "total_volume": sum(r.volume or 0 for r in results),
            "avg_cpc": round(sum(r.cpc or 0 for r in results) / len(results), 2) if results else 0
        }
    except Exception as e:
        logging.error(f"Error analyzing website: {e}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-competitors")
async def analyze_competitors(request: AnalyzeRequest):
    try:
        competitor_service = CompetitorAnalysisService()
        analysis = await competitor_service.analyze_competitors(request.url, request.region)
        
        return analysis
    except Exception as e:
        logging.error(f"Error in competitor analysis: {e}")
        logging.error(traceback.format_exc())
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