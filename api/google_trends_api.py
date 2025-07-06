import requests
import json
from typing import List, Dict, Optional
import re
from urllib.parse import quote_plus
import random
from datetime import datetime, timedelta

class GoogleTrendsAPI:
    """Enhanced SEO data provider with Google Trends style analytics"""
    
    def __init__(self):
        # API endpoints for real data
        self.trends_url = "https://trends.google.com/trends/api/explore"
        self.autocomplete_url = "https://suggestqueries.google.com/complete/search"
        self.keyword_planner_url = "https://ads.google.com/intl/en_us/aw/keywordplanner"
        
    def get_google_trends_data(self, keyword: str, region: str = "US") -> Dict:
        """Get Google Trends style data for keywords"""
        try:
            # For now, generate realistic trends data
            # In production, you'd use the official Google Trends API or pytrends
            return self.generate_realistic_trends_data(keyword, region)
        except Exception as e:
            print(f"Error getting trends data: {e}")
            return self.generate_realistic_trends_data(keyword, region)
    
    def generate_realistic_trends_data(self, keyword: str, region: str = "US") -> Dict:
        """Generate realistic Google Trends style data"""
        
        # Generate 12 months of trend data
        trend_data = []
        base_interest = random.randint(40, 100)
        
        for i in range(12):
            date = datetime.now() - timedelta(days=30 * (11 - i))
            
            # Add seasonal variation
            seasonal_factor = 1.0
            if date.month in [11, 12]:  # Holiday season
                seasonal_factor = 1.3
            elif date.month in [6, 7, 8]:  # Summer
                seasonal_factor = 1.1
            elif date.month in [1, 2]:  # Post-holiday dip
                seasonal_factor = 0.8
            
            interest = int(base_interest * seasonal_factor * random.uniform(0.7, 1.3))
            interest = min(100, max(0, interest))
            
            trend_data.append({
                "date": date.strftime("%Y-%m"),
                "interest": interest
            })
        
        # Generate related queries
        related_queries = self.generate_related_queries(keyword)
        rising_queries = self.generate_rising_queries(keyword)
        
        # Calculate average search volume
        search_volume = self.calculate_realistic_search_volume(keyword)
        
        return {
            "keyword": keyword,
            "region": region,
            "search_volume": search_volume,
            "trend_data": trend_data,
            "related_queries": related_queries,
            "rising_queries": rising_queries,
            "interest_by_region": self.generate_regional_interest(keyword),
            "seasonal_patterns": self.analyze_seasonal_patterns(trend_data),
            "competition_level": self.calculate_competition_level(keyword),
            "suggested_bid": self.calculate_suggested_bid(keyword),
            "search_intent": self.classify_search_intent(keyword)
        }
    
    def generate_related_queries(self, keyword: str) -> List[Dict]:
        """Generate related queries like Google Keyword Planner"""
        base_word = keyword.split()[0].lower()
        
        # Common query patterns
        patterns = [
            f"{keyword} tutorial",
            f"{keyword} guide",
            f"how to {keyword}",
            f"{keyword} tips",
            f"{keyword} vs",
            f"best {keyword}",
            f"{keyword} review",
            f"{keyword} pricing",
            f"{keyword} features",
            f"{keyword} alternatives",
            f"free {keyword}",
            f"{keyword} online",
            f"{keyword} download",
            f"{keyword} app",
            f"{keyword} software"
        ]
        
        related = []
        for pattern in patterns[:8]:
            volume = random.randint(100, 10000)
            competition = random.choice(["Low", "Medium", "High"])
            cpc = round(random.uniform(0.5, 8.0), 2)
            
            related.append({
                "query": pattern,
                "volume": volume,
                "competition": competition,
                "cpc": cpc,
                "trend": random.choice(["Rising", "Stable", "Declining"])
            })
        
        return sorted(related, key=lambda x: x["volume"], reverse=True)
    
    def generate_rising_queries(self, keyword: str) -> List[Dict]:
        """Generate rising/trending queries"""
        current_year = datetime.now().year
        base_word = keyword.split()[0].lower()
        
        rising_patterns = [
            f"{keyword} {current_year}",
            f"{keyword} AI",
            f"{keyword} automation",
            f"{keyword} mobile",
            f"{keyword} API",
            f"{keyword} integration",
            f"new {keyword}",
            f"{keyword} update"
        ]
        
        rising = []
        for pattern in rising_patterns[:6]:
            growth = random.randint(150, 500)  # % growth
            volume = random.randint(50, 2000)
            
            rising.append({
                "query": pattern,
                "volume": volume,
                "growth_percentage": f"+{growth}%",
                "trend_status": "Rising"
            })
        
        return rising
    
    def generate_regional_interest(self, keyword: str) -> List[Dict]:
        """Generate interest by region data"""
        regions = [
            {"region": "United States", "interest": random.randint(70, 100)},
            {"region": "United Kingdom", "interest": random.randint(60, 90)},
            {"region": "Canada", "interest": random.randint(50, 80)},
            {"region": "Australia", "interest": random.randint(40, 75)},
            {"region": "Germany", "interest": random.randint(30, 70)},
            {"region": "France", "interest": random.randint(25, 65)},
            {"region": "India", "interest": random.randint(35, 85)},
            {"region": "Japan", "interest": random.randint(20, 60)}
        ]
        
        return sorted(regions, key=lambda x: x["interest"], reverse=True)
    
    def analyze_seasonal_patterns(self, trend_data: List[Dict]) -> Dict:
        """Analyze seasonal patterns in the data"""
        monthly_avg = {}
        for data_point in trend_data:
            month = int(data_point["date"].split("-")[1])
            if month not in monthly_avg:
                monthly_avg[month] = []
            monthly_avg[month].append(data_point["interest"])
        
        # Calculate averages
        seasonal_analysis = {}
        for month, values in monthly_avg.items():
            avg = sum(values) / len(values)
            month_name = datetime(2024, month, 1).strftime("%B")
            seasonal_analysis[month_name] = round(avg, 1)
        
        # Determine peak season
        peak_month = max(seasonal_analysis.items(), key=lambda x: x[1])
        low_month = min(seasonal_analysis.items(), key=lambda x: x[1])
        
        return {
            "monthly_averages": seasonal_analysis,
            "peak_season": f"{peak_month[0]} (Interest: {peak_month[1]})",
            "low_season": f"{low_month[0]} (Interest: {low_month[1]})",
            "volatility": "Medium" if max(seasonal_analysis.values()) - min(seasonal_analysis.values()) > 20 else "Low"
        }
    
    def calculate_realistic_search_volume(self, keyword: str) -> Dict:
        """Calculate realistic search volume like Google Keyword Planner"""
        word_count = len(keyword.split())
        keyword_lower = keyword.lower()
        
        # Base volume calculation
        if word_count == 1:
            if len(keyword) <= 4:  # Short branded terms
                monthly_volume = random.randint(50000, 500000)
            else:
                monthly_volume = random.randint(10000, 100000)
        elif word_count == 2:
            monthly_volume = random.randint(5000, 50000)
        elif word_count == 3:
            monthly_volume = random.randint(1000, 20000)
        else:
            monthly_volume = random.randint(100, 5000)
        
        # Adjust for commercial intent
        if any(word in keyword_lower for word in ['buy', 'price', 'cost', 'cheap', 'sale', 'discount']):
            monthly_volume = int(monthly_volume * 0.6)  # Commercial keywords often have lower volume
        
        # Generate range (like Google Keyword Planner)
        low_range = int(monthly_volume * 0.7)
        high_range = int(monthly_volume * 1.3)
        
        return {
            "monthly_searches": monthly_volume,
            "search_range": f"{low_range:,} - {high_range:,}",
            "average_monthly": monthly_volume,
            "peak_month_volume": int(monthly_volume * 1.4),
            "low_month_volume": int(monthly_volume * 0.6)
        }
    
    def calculate_competition_level(self, keyword: str) -> Dict:
        """Calculate competition level with details"""
        keyword_lower = keyword.lower()
        
        # Determine competition based on keyword characteristics
        if any(word in keyword_lower for word in ['buy', 'price', 'cost', 'cheap', 'sale']):
            competition = "High"
            score = random.uniform(0.7, 1.0)
        elif any(word in keyword_lower for word in ['how', 'what', 'why', 'guide', 'tutorial']):
            competition = "Low"
            score = random.uniform(0.1, 0.4)
        elif any(word in keyword_lower for word in ['best', 'top', 'review', 'compare']):
            competition = "High"
            score = random.uniform(0.6, 0.9)
        else:
            competition = "Medium"
            score = random.uniform(0.3, 0.7)
        
        return {
            "level": competition,
            "score": round(score, 2),
            "indexed_pages": random.randint(100000, 50000000),
            "competing_domains": random.randint(5000, 500000),
            "difficulty_rating": f"{int(score * 100)}/100"
        }
    
    def calculate_suggested_bid(self, keyword: str) -> Dict:
        """Calculate suggested bid like Google Ads"""
        keyword_lower = keyword.lower()
        
        # Base CPC calculation
        if any(word in keyword_lower for word in ['insurance', 'loan', 'lawyer', 'attorney']):
            base_cpc = random.uniform(15.0, 50.0)
        elif any(word in keyword_lower for word in ['buy', 'price', 'cost', 'purchase']):
            base_cpc = random.uniform(2.0, 15.0)
        elif any(word in keyword_lower for word in ['software', 'app', 'service']):
            base_cpc = random.uniform(3.0, 12.0)
        else:
            base_cpc = random.uniform(0.5, 5.0)
        
        return {
            "suggested_bid": round(base_cpc, 2),
            "low_range": round(base_cpc * 0.7, 2),
            "high_range": round(base_cpc * 1.5, 2),
            "top_page_bid": round(base_cpc * 2.0, 2),
            "currency": "USD"
        }
    
    def classify_search_intent(self, keyword: str) -> Dict:
        """Classify search intent like Google does"""
        keyword_lower = keyword.lower()
        
        if any(word in keyword_lower for word in ['buy', 'purchase', 'order', 'price', 'cost', 'cheap']):
            intent = "Commercial"
            confidence = 0.9
        elif any(word in keyword_lower for word in ['how', 'what', 'why', 'guide', 'tutorial', 'learn']):
            intent = "Informational"
            confidence = 0.85
        elif any(word in keyword_lower for word in ['login', 'sign', 'account', 'contact', 'support']):
            intent = "Navigational"
            confidence = 0.8
        elif any(word in keyword_lower for word in ['best', 'top', 'review', 'compare', 'vs']):
            intent = "Commercial Investigation"
            confidence = 0.75
        else:
            intent = "Informational"
            confidence = 0.6
        
        return {
            "primary_intent": intent,
            "confidence": confidence,
            "secondary_intents": self.get_secondary_intents(keyword_lower),
            "user_journey_stage": self.determine_journey_stage(intent)
        }
    
    def get_secondary_intents(self, keyword: str) -> List[str]:
        """Get secondary search intents"""
        intents = []
        if 'how' in keyword or 'tutorial' in keyword:
            intents.append("Educational")
        if 'best' in keyword or 'top' in keyword:
            intents.append("Research")
        if 'price' in keyword or 'cost' in keyword:
            intents.append("Price Comparison")
        return intents[:2]  # Limit to 2 secondary intents
    
    def determine_journey_stage(self, intent: str) -> str:
        """Determine user journey stage"""
        journey_map = {
            "Informational": "Awareness",
            "Commercial Investigation": "Consideration", 
            "Commercial": "Decision",
            "Navigational": "Action"
        }
        return journey_map.get(intent, "Awareness")
    
    def get_keyword_ideas(self, seed_keyword: str, region: str = "US") -> List[Dict]:
        """Get keyword ideas like Google Keyword Planner"""
        base_word = seed_keyword.split()[0].lower()
        
        # Generate keyword ideas using various patterns
        keyword_ideas = []
        
        # Long-tail variations
        long_tail_patterns = [
            f"how to use {seed_keyword}",
            f"{seed_keyword} for beginners",
            f"best {seed_keyword} tools",
            f"{seed_keyword} step by step",
            f"{seed_keyword} tips and tricks",
            f"free {seed_keyword}",
            f"{seed_keyword} online",
            f"{seed_keyword} tutorial",
            f"{seed_keyword} guide",
            f"{seed_keyword} examples"
        ]
        
        # Question-based keywords
        question_patterns = [
            f"what is {seed_keyword}",
            f"how does {seed_keyword} work",
            f"why use {seed_keyword}",
            f"when to use {seed_keyword}",
            f"where to find {seed_keyword}"
        ]
        
        # Commercial keywords
        commercial_patterns = [
            f"{seed_keyword} price",
            f"{seed_keyword} cost",
            f"buy {seed_keyword}",
            f"{seed_keyword} discount",
            f"{seed_keyword} deals",
            f"cheap {seed_keyword}"
        ]
        
        all_patterns = long_tail_patterns + question_patterns + commercial_patterns
        
        for pattern in all_patterns[:20]:  # Limit to 20 suggestions
            trends_data = self.get_google_trends_data(pattern, region)
            keyword_ideas.append({
                "keyword": pattern,
                "search_volume": trends_data["search_volume"]["monthly_searches"],
                "competition": trends_data["competition_level"]["level"],
                "cpc": trends_data["suggested_bid"]["suggested_bid"],
                "trend": random.choice(["Rising", "Stable", "Declining"]),
                "intent": trends_data["search_intent"]["primary_intent"],
                "difficulty": trends_data["competition_level"]["difficulty_rating"]
            })
        
        return sorted(keyword_ideas, key=lambda x: x["search_volume"], reverse=True)