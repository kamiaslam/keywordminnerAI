import random
import hashlib
from typing import Dict, Optional

class KeywordMetricsService:
    def __init__(self):
        self.mock_data = True  # Set to False when real APIs are integrated
        
    def get_keyword_metrics(self, keyword: str, region: str = "us") -> Dict:
        """
        Get keyword metrics including volume, CPC, and competition.
        Currently uses mock data for demonstration.
        """
        if self.mock_data:
            return self._generate_mock_metrics(keyword, region)
        else:
            # TODO: Integrate with real APIs like:
            # - Google Keyword Planner API
            # - SEMrush API
            # - Ahrefs API
            # - Ubersuggest API
            return self._get_real_metrics(keyword, region)
    
    def _generate_mock_metrics(self, keyword: str, region: str) -> Dict:
        """Generate realistic mock data based on keyword characteristics"""
        
        # Create consistent random values based on keyword hash
        seed = int(hashlib.md5(keyword.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        # Base metrics influenced by keyword length and type
        word_count = len(keyword.split())
        keyword_lower = keyword.lower()
        
        # Volume calculation (higher for shorter, common keywords)
        if word_count == 1:
            base_volume = random.randint(5000, 50000)
        elif word_count == 2:
            base_volume = random.randint(1000, 15000)
        else:
            base_volume = random.randint(100, 5000)
        
        # Adjust for common commercial keywords
        commercial_keywords = ['buy', 'price', 'cost', 'cheap', 'best', 'review', 'deal']
        if any(word in keyword_lower for word in commercial_keywords):
            base_volume = int(base_volume * 1.5)
        
        # CPC calculation (higher for commercial intent)
        if any(word in keyword_lower for word in commercial_keywords):
            base_cpc = random.uniform(1.50, 8.50)
        elif 'how' in keyword_lower or 'what' in keyword_lower:
            base_cpc = random.uniform(0.25, 2.50)
        else:
            base_cpc = random.uniform(0.50, 3.50)
        
        # Competition level
        if base_volume > 10000:
            competition_score = random.uniform(0.7, 1.0)
            competition_level = "High"
        elif base_volume > 2000:
            competition_score = random.uniform(0.4, 0.7)
            competition_level = "Medium"
        else:
            competition_score = random.uniform(0.1, 0.4)
            competition_level = "Low"
        
        # Regional adjustments
        region_multipliers = {
            "us": 1.0,
            "uk": 0.8,
            "ca": 0.6,
            "au": 0.5,
            "ae": 0.3,
            "in": 0.7,
            "global": 1.2
        }
        
        multiplier = region_multipliers.get(region, 1.0)
        final_volume = int(base_volume * multiplier)
        final_cpc = round(base_cpc * multiplier, 2)
        
        return {
            "volume": final_volume,
            "cpc": final_cpc,
            "competition": competition_level,
            "competition_score": round(competition_score, 2),
            "trend": self._get_trend_data(keyword),
            "related_keywords": self._get_related_keywords(keyword)
        }
    
    def _get_trend_data(self, keyword: str) -> str:
        """Generate trend information"""
        trends = ["Rising", "Stable", "Declining", "Seasonal"]
        seed = int(hashlib.md5(keyword.encode()).hexdigest()[:4], 16)
        random.seed(seed)
        return random.choice(trends)
    
    def _get_related_keywords(self, keyword: str) -> list:
        """Generate related keywords"""
        base_words = keyword.split()
        related = []
        
        if len(base_words) > 0:
            # Add some variations
            related.append(f"{keyword} guide")
            related.append(f"best {keyword}")
            related.append(f"{keyword} tips")
        
        return related[:3]
    
    def _get_real_metrics(self, keyword: str, region: str) -> Dict:
        """
        TODO: Implement real API integrations
        """
        # Example implementation would go here
        # This would call actual APIs like Google Keyword Planner
        pass
    
    def get_batch_metrics(self, keywords: list, region: str = "us") -> Dict:
        """Get metrics for multiple keywords at once"""
        results = {}
        for keyword in keywords:
            results[keyword] = self.get_keyword_metrics(keyword, region)
        return results