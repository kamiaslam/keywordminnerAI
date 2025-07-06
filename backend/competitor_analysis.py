import asyncio
from typing import List, Dict, Optional
from backend.scraper import KeywordScraperAgent
from backend.nlp_engine import NLPKeywordEngine
from backend.keyword_metrics import KeywordMetricsService
import hashlib

class CompetitorAnalysisService:
    def __init__(self):
        self.scraper = KeywordScraperAgent()
        self.nlp_engine = NLPKeywordEngine()
        self.metrics_service = KeywordMetricsService()
    
    async def analyze_competitors(self, target_url: str, region: str = "us") -> Dict:
        """
        Analyze competitors by finding similar websites and their keywords
        """
        try:
            # First analyze the target website once
            target_content = await self.scraper.scrape_website(target_url)
            target_keywords = self.nlp_engine.extract_keywords(target_content)
            
            # Get competitors based on target analysis
            competitors = await self._find_competitors_from_content(target_content, target_keywords, target_url)
            
            competitor_analysis = []
            
            for competitor in competitors:
                try:
                    # Scrape competitor website
                    content = await self.scraper.scrape_website(competitor['url'])
                    
                    # Extract keywords
                    keywords = self.nlp_engine.extract_keywords(content)
                    
                    # Get top 20 keywords with metrics
                    top_keywords = []
                    total_volume = 0
                    total_cpc = 0
                    
                    for keyword_data in keywords[:20]:  # Limit to top 20 for performance
                        metrics = self.metrics_service.get_keyword_metrics(
                            keyword_data['keyword'], region
                        )
                        
                        keyword_with_metrics = {
                            'keyword': keyword_data['keyword'],
                            'volume': metrics['volume'],
                            'cpc': metrics['cpc'],
                            'competition': metrics['competition'],
                            'type': keyword_data['type'],
                            'intent': keyword_data['intent']
                        }
                        
                        top_keywords.append(keyword_with_metrics)
                        total_volume += metrics['volume'] or 0
                        total_cpc += metrics['cpc'] or 0
                    
                    avg_cpc = round(total_cpc / len(top_keywords), 2) if top_keywords else 0
                    
                    competitor_analysis.append({
                        'website': competitor['url'],
                        'domain': competitor['domain'],
                        'estimated_traffic': competitor['estimated_traffic'],
                        'domain_authority': competitor['domain_authority'],
                        'total_keywords': len(keywords),
                        'top_keywords': top_keywords,
                        'total_volume': total_volume,
                        'avg_cpc': avg_cpc,
                        'keyword_overlap': self._calculate_overlap(target_url, competitor['url'])
                    })
                    
                except Exception as e:
                    print(f"Error analyzing competitor {competitor['url']}: {e}")
                    continue
            
            # Sort by estimated traffic
            competitor_analysis.sort(key=lambda x: x['estimated_traffic'], reverse=True)
            
            # Use the already analyzed content for debugging
            detected_industries = self._identify_industry(target_keywords, target_content)
            
            return {
                'target_url': target_url,
                'region': region,
                'competitors_found': len(competitor_analysis),
                'competitors': competitor_analysis,
                'keyword_gaps': await self._find_keyword_gaps_from_content(target_content, target_keywords, competitor_analysis, region),
                'debug_info': {
                    'detected_industries': detected_industries,
                    'title': target_content.get('title', ''),
                    'meta_description': target_content.get('meta_description', ''),
                    'top_keywords': [kw['keyword'] for kw in target_keywords[:10]]
                }
            }
            
        except Exception as e:
            raise Exception(f"Error in competitor analysis: {str(e)}")
    
    async def _find_competitors_from_content(self, target_content: Dict, target_keywords: List[Dict], target_url: str) -> List[Dict]:
        """
        Find relevant competitor websites based on already analyzed content
        """
        try:
            # Extract key topics and industry indicators
            industry_keywords = self._identify_industry(target_keywords, target_content)
            
            # Find competitors based on identified industry
            competitors = self._get_industry_competitors(industry_keywords, target_url)
            
            return competitors[:4]  # Return top 4 competitors
            
        except Exception as e:
            print(f"Error finding competitors: {e}")
            # Fallback to basic domain-based suggestions
            return self._get_fallback_competitors(target_url)
    
    def _identify_industry(self, keywords: List[Dict], content: Dict) -> List[str]:
        """
        Identify the industry/niche based on website content
        """
        # Extract key terms from title, headings, and top keywords
        title = content.get('title', '').lower()
        meta_desc = content.get('meta_description', '').lower()
        headings = ' '.join([h for heading_list in content.get('headings', {}).values() for h in heading_list]).lower()
        
        all_text = f"{title} {meta_desc} {headings}"
        top_keywords = [kw['keyword'].lower() for kw in keywords[:20]]
        
        # Industry classification patterns
        industry_patterns = {
            'ai_ml': ['artificial intelligence', 'machine learning', 'ai', 'neural', 'deep learning', 'language model', 'llm', 'chatbot', 'gpt', 'claude', 'anthropic', 'openai', 'transformer', 'nlp', 'conversational', 'assistant', 'generative', 'text generation', 'ai research', 'research lab', 'large language', 'chatgpt'],
            'ecommerce': ['shop', 'buy', 'store', 'ecommerce', 'retail', 'cart', 'checkout', 'payment', 'marketplace', 'product', 'amazon', 'shopify'],
            'saas': ['software', 'saas', 'platform', 'cloud', 'api', 'dashboard', 'subscription', 'enterprise', 'solution', 'tool'],
            'finance': ['finance', 'fintech', 'banking', 'payment', 'cryptocurrency', 'bitcoin', 'trading', 'investment', 'lending'],
            'healthcare': ['health', 'medical', 'doctor', 'patient', 'healthcare', 'medicine', 'clinic', 'hospital'],
            'education': ['education', 'learning', 'course', 'student', 'teacher', 'university', 'school', 'training'],
            'media': ['news', 'media', 'content', 'blog', 'journalism', 'video', 'streaming', 'entertainment'],
            'social': ['social', 'community', 'network', 'connect', 'share', 'post', 'follow', 'friend'],
            'productivity': ['productivity', 'project', 'management', 'collaboration', 'workflow', 'task', 'team']
        }
        
        detected_industries = []
        
        for industry, patterns in industry_patterns.items():
            score = 0
            matched_patterns = []
            for pattern in patterns:
                if pattern in all_text:
                    score += 3
                    matched_patterns.append(f"text:{pattern}")
                if any(pattern in kw for kw in top_keywords):
                    score += 2
                    matched_patterns.append(f"keyword:{pattern}")
            
            if score > 0:  # Lower threshold and log all scores
                detected_industries.append((industry, score, matched_patterns))
                print(f"Industry detection - {industry}: score={score}, matches={matched_patterns}")
        
        # Sort by score and return top industries
        detected_industries.sort(key=lambda x: x[1], reverse=True)
        
        # Debug output
        print(f"Content analysis:")
        print(f"Title: {content.get('title', '')}")
        print(f"Meta: {content.get('meta_description', '')}")
        print(f"Top keywords: {[kw['keyword'] for kw in keywords[:10]]}")
        print(f"Detected industries: {[(ind, score) for ind, score, _ in detected_industries]}")
        
        return [industry for industry, score, _ in detected_industries[:2] if score >= 2]
    
    def _get_industry_competitors(self, industries: List[str], target_url: str) -> List[Dict]:
        """
        Get competitors based on identified industries
        """
        domain = target_url.replace('https://', '').replace('http://', '').split('/')[0]
        
        competitor_db = {
            'ai_ml': [
                {'url': 'https://openai.com', 'domain': 'openai.com', 'estimated_traffic': 180000000, 'domain_authority': 85},
                {'url': 'https://cohere.ai', 'domain': 'cohere.ai', 'estimated_traffic': 2500000, 'domain_authority': 72},
                {'url': 'https://huggingface.co', 'domain': 'huggingface.co', 'estimated_traffic': 25000000, 'domain_authority': 78},
                {'url': 'https://mistral.ai', 'domain': 'mistral.ai', 'estimated_traffic': 1800000, 'domain_authority': 68},
                {'url': 'https://ai.google.dev', 'domain': 'ai.google.dev', 'estimated_traffic': 15000000, 'domain_authority': 88},
                {'url': 'https://together.ai', 'domain': 'together.ai', 'estimated_traffic': 800000, 'domain_authority': 65}
            ],
            'ecommerce': [
                {'url': 'https://shopify.com', 'domain': 'shopify.com', 'estimated_traffic': 120000000, 'domain_authority': 89},
                {'url': 'https://amazon.com', 'domain': 'amazon.com', 'estimated_traffic': 2800000000, 'domain_authority': 95},
                {'url': 'https://ebay.com', 'domain': 'ebay.com', 'estimated_traffic': 850000000, 'domain_authority': 92},
                {'url': 'https://etsy.com', 'domain': 'etsy.com', 'estimated_traffic': 480000000, 'domain_authority': 87}
            ],
            'saas': [
                {'url': 'https://salesforce.com', 'domain': 'salesforce.com', 'estimated_traffic': 95000000, 'domain_authority': 90},
                {'url': 'https://hubspot.com', 'domain': 'hubspot.com', 'estimated_traffic': 85000000, 'domain_authority': 88},
                {'url': 'https://slack.com', 'domain': 'slack.com', 'estimated_traffic': 25000000, 'domain_authority': 85},
                {'url': 'https://notion.so', 'domain': 'notion.so', 'estimated_traffic': 90000000, 'domain_authority': 82}
            ],
            'finance': [
                {'url': 'https://stripe.com', 'domain': 'stripe.com', 'estimated_traffic': 45000000, 'domain_authority': 87},
                {'url': 'https://paypal.com', 'domain': 'paypal.com', 'estimated_traffic': 780000000, 'domain_authority': 91},
                {'url': 'https://coinbase.com', 'domain': 'coinbase.com', 'estimated_traffic': 65000000, 'domain_authority': 84},
                {'url': 'https://robinhood.com', 'domain': 'robinhood.com', 'estimated_traffic': 25000000, 'domain_authority': 79}
            ],
            'social': [
                {'url': 'https://twitter.com', 'domain': 'twitter.com', 'estimated_traffic': 1200000000, 'domain_authority': 93},
                {'url': 'https://linkedin.com', 'domain': 'linkedin.com', 'estimated_traffic': 890000000, 'domain_authority': 94},
                {'url': 'https://instagram.com', 'domain': 'instagram.com', 'estimated_traffic': 1800000000, 'domain_authority': 95},
                {'url': 'https://discord.com', 'domain': 'discord.com', 'estimated_traffic': 180000000, 'domain_authority': 83}
            ]
        }
        
        # Prioritize the primary industry (first one with highest score)
        all_competitors = []
        
        if industries:
            # First, try to get competitors from the primary industry
            primary_industry = industries[0]
            if primary_industry in competitor_db:
                all_competitors = competitor_db[primary_industry].copy()
            
            # If we don't have enough competitors, add from secondary industries
            if len(all_competitors) < 4 and len(industries) > 1:
                for secondary_industry in industries[1:]:
                    if secondary_industry in competitor_db:
                        all_competitors.extend(competitor_db[secondary_industry])
        
        # Filter out the target domain itself
        filtered_competitors = [comp for comp in all_competitors if comp['domain'] not in domain]
        
        # Sort by estimated traffic and return top results
        filtered_competitors.sort(key=lambda x: x['estimated_traffic'], reverse=True)
        
        return filtered_competitors[:4] if filtered_competitors else self._get_fallback_competitors(target_url)
    
    def _get_fallback_competitors(self, target_url: str) -> List[Dict]:
        """
        Fallback competitors when industry detection fails
        """
        return [
            {'url': 'https://google.com', 'domain': 'google.com', 'estimated_traffic': 8500000000, 'domain_authority': 100},
            {'url': 'https://microsoft.com', 'domain': 'microsoft.com', 'estimated_traffic': 1200000000, 'domain_authority': 97},
            {'url': 'https://apple.com', 'domain': 'apple.com', 'estimated_traffic': 900000000, 'domain_authority': 95}
        ]
    
    def _calculate_overlap(self, target_url: str, competitor_url: str) -> float:
        """
        Calculate keyword overlap percentage (mock calculation)
        """
        # Mock overlap based on domain similarity
        target_domain = target_url.replace('https://', '').replace('http://', '').split('/')[0]
        competitor_domain = competitor_url.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Simple character-based similarity for mock data
        common_chars = set(target_domain) & set(competitor_domain)
        total_chars = set(target_domain) | set(competitor_domain)
        
        overlap = len(common_chars) / len(total_chars) if total_chars else 0
        return round(overlap * 100, 1)
    
    async def _find_keyword_gaps_from_content(self, target_content: Dict, target_keywords: List[Dict], competitors: List[Dict], region: str) -> List[Dict]:
        """
        Find keyword opportunities that competitors rank for but target doesn't
        """
        try:
            # Use already analyzed target keywords
            target_keyword_set = {kw['keyword'].lower() for kw in target_keywords}
            
            # Find gaps
            keyword_gaps = []
            
            for competitor in competitors:
                for keyword in competitor['top_keywords']:
                    if keyword['keyword'].lower() not in target_keyword_set:
                        gap = {
                            'keyword': keyword['keyword'],
                            'volume': keyword['volume'],
                            'cpc': keyword['cpc'],
                            'competition': keyword['competition'],
                            'competitor_domain': competitor['domain'],
                            'opportunity_score': self._calculate_opportunity_score(keyword)
                        }
                        keyword_gaps.append(gap)
            
            # Remove duplicates and sort by opportunity score
            seen = set()
            unique_gaps = []
            for gap in keyword_gaps:
                if gap['keyword'] not in seen:
                    seen.add(gap['keyword'])
                    unique_gaps.append(gap)
            
            unique_gaps.sort(key=lambda x: x['opportunity_score'], reverse=True)
            return unique_gaps[:15]  # Return top 15 opportunities
            
        except Exception as e:
            print(f"Error finding keyword gaps: {e}")
            return []
    
    def _calculate_opportunity_score(self, keyword: Dict) -> float:
        """
        Calculate opportunity score based on volume, CPC, and competition
        """
        volume_score = min((keyword['volume'] or 0) / 10000, 10)  # Max 10 points
        cpc_score = min((keyword['cpc'] or 0) * 2, 10)  # Max 10 points
        
        competition_score = {
            'Low': 10,
            'Medium': 6,
            'High': 3
        }.get(keyword['competition'], 5)
        
        return round((volume_score + cpc_score + competition_score) / 3, 2)