import random
import re
from typing import List, Dict, Set
from datetime import datetime

class ProgrammaticLongTailGenerator:
    """Advanced programmatic long-tail keyword generator for strategic SEO"""
    
    def __init__(self):
        # Intent-based keyword patterns
        self.intent_patterns = {
            'commercial': {
                'patterns': [
                    'best {product} for {use_case}',
                    '{product} vs {competitor}',
                    'cheap {product} {qualifier}',
                    '{product} pricing comparison',
                    'buy {product} online',
                    '{product} discount code',
                    'affordable {product} {year}',
                    '{product} deals and offers',
                    '{product} cost analysis',
                    'where to buy {product}'
                ],
                'volume_range': (500, 5000),
                'cpc_range': (2.0, 15.0),
                'competition': ['Medium', 'High']
            },
            'informational': {
                'patterns': [
                    'how to use {product} for {use_case}',
                    'what is {product} used for',
                    '{product} tutorial for beginners',
                    '{product} step by step guide',
                    '{product} best practices {year}',
                    'learn {product} in {timeframe}',
                    '{product} tips and tricks',
                    '{product} complete guide',
                    '{product} getting started',
                    'understanding {product} features'
                ],
                'volume_range': (800, 8000),
                'cpc_range': (0.5, 3.0),
                'competition': ['Low', 'Medium']
            },
            'problem_solving': {
                'patterns': [
                    '{product} not working fix',
                    'solve {problem} with {product}',
                    '{product} troubleshooting guide',
                    'fix {product} error',
                    '{product} common problems',
                    'why {product} is slow',
                    '{product} performance issues',
                    'improve {product} speed',
                    '{product} optimization guide',
                    '{product} error codes'
                ],
                'volume_range': (300, 3000),
                'cpc_range': (1.0, 5.0),
                'competition': ['Low', 'Medium']
            },
            'feature_specific': {
                'patterns': [
                    '{product} {feature} tutorial',
                    'how to {action} in {product}',
                    '{product} {feature} vs {alternative}',
                    'best {product} {feature} practices',
                    '{product} {feature} examples',
                    'advanced {product} {feature}',
                    '{product} {feature} integration',
                    'customize {product} {feature}',
                    '{product} {feature} automation',
                    '{product} {feature} workflow'
                ],
                'volume_range': (200, 2500),
                'cpc_range': (1.5, 6.0),
                'competition': ['Low', 'Medium']
            },
            'industry_specific': {
                'patterns': [
                    '{product} for {industry}',
                    '{industry} {product} solutions',
                    'best {product} {industry} tools',
                    '{product} {industry} use cases',
                    '{industry} {product} implementation',
                    '{product} {industry} automation',
                    '{industry} professionals using {product}',
                    '{product} {industry} ROI',
                    '{industry} {product} best practices',
                    '{product} for {industry} teams'
                ],
                'volume_range': (400, 4000),
                'cpc_range': (2.0, 8.0),
                'competition': ['Medium', 'High']
            }
        }
        
        # Industry-specific contexts
        self.industry_contexts = {
            'saas': {
                'use_cases': ['small business', 'enterprise', 'startups', 'remote teams', 'scaling companies'],
                'features': ['automation', 'integration', 'api', 'dashboard', 'analytics', 'reporting', 'collaboration'],
                'actions': ['automate', 'integrate', 'customize', 'scale', 'optimize', 'migrate', 'setup'],
                'industries': ['healthcare', 'finance', 'education', 'retail', 'manufacturing', 'real estate', 'legal'],
                'problems': ['manual processes', 'data silos', 'inefficiency', 'poor communication', 'lack of visibility'],
                'timeframes': ['30 days', '3 months', '6 months', 'one year']
            },
            'ecommerce': {
                'use_cases': ['online stores', 'dropshipping', 'multi-vendor', 'B2B sales', 'subscription'],
                'features': ['checkout', 'inventory', 'shipping', 'payments', 'SEO', 'analytics', 'mobile'],
                'actions': ['optimize', 'increase sales', 'reduce cart abandonment', 'improve conversion', 'scale'],
                'industries': ['fashion', 'electronics', 'beauty', 'home decor', 'sports', 'books', 'jewelry'],
                'problems': ['low conversion', 'high cart abandonment', 'poor mobile experience', 'slow loading'],
                'timeframes': ['1 week', '1 month', '3 months', 'this year']
            },
            'ai': {
                'use_cases': ['content creation', 'customer service', 'data analysis', 'automation', 'personalization'],
                'features': ['chatbot', 'NLP', 'machine learning', 'API', 'training', 'deployment', 'monitoring'],
                'actions': ['train', 'deploy', 'fine-tune', 'integrate', 'optimize', 'scale', 'monitor'],
                'industries': ['healthcare', 'finance', 'education', 'marketing', 'sales', 'HR', 'legal'],
                'problems': ['manual tasks', 'poor accuracy', 'scalability issues', 'data quality', 'bias'],
                'timeframes': ['quickly', 'in minutes', 'efficiently', 'at scale']
            },
            'finance': {
                'use_cases': ['small business', 'freelancers', 'enterprise', 'international', 'recurring payments'],
                'features': ['security', 'compliance', 'fraud protection', 'reporting', 'integration', 'mobile'],
                'actions': ['accept payments', 'reduce fees', 'improve security', 'automate', 'scale'],
                'industries': ['retail', 'SaaS', 'marketplace', 'nonprofits', 'healthcare', 'education'],
                'problems': ['high fees', 'security concerns', 'complex setup', 'poor UX', 'compliance'],
                'timeframes': ['instantly', 'same day', 'within hours', 'quickly']
            }
        }
        
        # Trending modifiers for 2025
        self.trending_modifiers = [
            '2025', 'ai powered', 'mobile first', 'cloud based', 'remote friendly',
            'privacy focused', 'sustainable', 'automated', 'intelligent', 'next generation'
        ]
        
        # Semantic keyword clusters
        self.semantic_clusters = {
            'comparison': ['vs', 'versus', 'compared to', 'alternative to', 'instead of', 'better than'],
            'quality': ['best', 'top', 'premium', 'high quality', 'professional', 'enterprise grade'],
            'cost': ['cheap', 'affordable', 'budget', 'free', 'low cost', 'cost effective'],
            'ease': ['easy', 'simple', 'quick', 'fast', 'efficient', 'user friendly'],
            'size': ['small business', 'enterprise', 'startup', 'large scale', 'team', 'individual']
        }
    
    def generate_longtail_keywords(self, domain: str, industry: str, count: int = 50) -> List[Dict]:
        """Generate programmatic long-tail keywords for strategic SEO"""
        
        domain_name = domain.split('.')[0]
        company_name = self.extract_company_name(domain)
        
        # Get industry context
        context = self.industry_contexts.get(industry, self.industry_contexts['saas'])
        
        keywords = []
        used_keywords = set()
        
        # Generate keywords for each intent type
        for intent_type, intent_config in self.intent_patterns.items():
            intent_keywords = self.generate_intent_keywords(
                domain_name, company_name, intent_type, intent_config, context
            )
            
            for keyword_data in intent_keywords:
                if keyword_data['keyword'] not in used_keywords and len(keywords) < count:
                    keywords.append(keyword_data)
                    used_keywords.add(keyword_data['keyword'])
        
        # Add trending/seasonal keywords
        trending_keywords = self.generate_trending_keywords(domain_name, industry, context)
        for keyword_data in trending_keywords:
            if keyword_data['keyword'] not in used_keywords and len(keywords) < count:
                keywords.append(keyword_data)
                used_keywords.add(keyword_data['keyword'])
        
        # Add semantic variations
        semantic_keywords = self.generate_semantic_keywords(domain_name, context)
        for keyword_data in semantic_keywords:
            if keyword_data['keyword'] not in used_keywords and len(keywords) < count:
                keywords.append(keyword_data)
                used_keywords.add(keyword_data['keyword'])
        
        # Sort by strategic value (volume * commercial intent)
        return sorted(keywords, key=lambda x: self.calculate_strategic_value(x), reverse=True)[:count]
    
    def generate_intent_keywords(self, domain_name: str, company_name: str, 
                                intent_type: str, intent_config: Dict, context: Dict) -> List[Dict]:
        """Generate keywords for specific search intent"""
        
        keywords = []
        patterns = intent_config['patterns']
        
        for pattern in patterns[:8]:  # Limit patterns per intent
            try:
                # Fill pattern with context-appropriate terms
                filled_keywords = self.fill_pattern(pattern, domain_name, company_name, context)
                
                for keyword in filled_keywords:
                    if len(keyword.split()) >= 3:  # Ensure long-tail
                        volume = random.randint(*intent_config['volume_range'])
                        cpc = round(random.uniform(*intent_config['cpc_range']), 2)
                        competition = random.choice(intent_config['competition'])
                        
                        keywords.append({
                            'keyword': keyword,
                            'volume': volume,
                            'cpc': cpc,
                            'competition': competition,
                            'intent': intent_type,
                            'keyword_type': 'long-tail',
                            'difficulty': self.calculate_difficulty(competition, volume),
                            'commercial_value': self.calculate_commercial_value(intent_type, cpc),
                            'content_opportunity': self.suggest_content_type(intent_type, keyword)
                        })
            except:
                continue
        
        return keywords
    
    def fill_pattern(self, pattern: str, domain_name: str, company_name: str, context: Dict) -> List[str]:
        """Fill keyword patterns with contextual terms"""
        
        filled_keywords = []
        
        # Replace placeholders with actual terms
        if '{product}' in pattern:
            products = [domain_name, company_name.lower(), f"{domain_name} software", f"{domain_name} platform"]
            for product in products[:2]:  # Limit variations
                current_pattern = pattern.replace('{product}', product)
                filled_keywords.extend(self.fill_remaining_placeholders(current_pattern, context))
        else:
            filled_keywords.extend(self.fill_remaining_placeholders(pattern, context))
        
        return filled_keywords
    
    def fill_remaining_placeholders(self, pattern: str, context: Dict) -> List[str]:
        """Fill remaining placeholders in the pattern"""
        
        # Replace year placeholder
        if '{year}' in pattern:
            pattern = pattern.replace('{year}', '2025')
        
        # Replace use case placeholder
        if '{use_case}' in pattern:
            use_cases = context.get('use_cases', ['business'])
            return [pattern.replace('{use_case}', use_case) for use_case in use_cases[:3]]
        
        # Replace feature placeholder
        if '{feature}' in pattern:
            features = context.get('features', ['feature'])
            return [pattern.replace('{feature}', feature) for feature in features[:3]]
        
        # Replace action placeholder
        if '{action}' in pattern:
            actions = context.get('actions', ['use'])
            return [pattern.replace('{action}', action) for action in actions[:3]]
        
        # Replace industry placeholder
        if '{industry}' in pattern:
            industries = context.get('industries', ['business'])
            return [pattern.replace('{industry}', industry) for industry in industries[:3]]
        
        # Replace problem placeholder
        if '{problem}' in pattern:
            problems = context.get('problems', ['issues'])
            return [pattern.replace('{problem}', problem) for problem in problems[:2]]
        
        # Replace timeframe placeholder
        if '{timeframe}' in pattern:
            timeframes = context.get('timeframes', ['quickly'])
            return [pattern.replace('{timeframe}', timeframe) for timeframe in timeframes[:2]]
        
        # Replace competitor placeholder (generic)
        if '{competitor}' in pattern:
            competitors = ['alternative', 'competitor', 'solution']
            return [pattern.replace('{competitor}', comp) for comp in competitors[:2]]
        
        # Replace qualifier placeholder
        if '{qualifier}' in pattern:
            qualifiers = ['solution', 'tool', 'software', 'platform']
            return [pattern.replace('{qualifier}', qual) for qual in qualifiers[:2]]
        
        return [pattern]
    
    def generate_trending_keywords(self, domain_name: str, industry: str, context: Dict) -> List[Dict]:
        """Generate trending and seasonal keywords"""
        
        keywords = []
        current_year = datetime.now().year
        
        # AI-powered variations
        ai_patterns = [
            f"ai powered {domain_name}",
            f"{domain_name} with artificial intelligence",
            f"intelligent {domain_name} solution",
            f"{domain_name} machine learning features",
            f"smart {domain_name} automation"
        ]
        
        # 2025-specific trends
        future_patterns = [
            f"{domain_name} trends 2025",
            f"future of {domain_name}",
            f"{domain_name} predictions 2025",
            f"next generation {domain_name}",
            f"{domain_name} innovation 2025"
        ]
        
        # Remote work trends
        remote_patterns = [
            f"{domain_name} for remote teams",
            f"remote {domain_name} solution",
            f"{domain_name} work from home",
            f"distributed teams {domain_name}",
            f"hybrid work {domain_name}"
        ]
        
        all_patterns = ai_patterns + future_patterns + remote_patterns
        
        for pattern in all_patterns[:10]:
            volume = random.randint(300, 2000)
            cpc = round(random.uniform(1.5, 6.0), 2)
            
            keywords.append({
                'keyword': pattern,
                'volume': volume,
                'cpc': cpc,
                'competition': 'Medium',
                'intent': 'trending',
                'keyword_type': 'long-tail',
                'difficulty': '40/100',
                'commercial_value': 'Medium',
                'content_opportunity': 'Thought leadership content'
            })
        
        return keywords
    
    def generate_semantic_keywords(self, domain_name: str, context: Dict) -> List[Dict]:
        """Generate semantically related keywords"""
        
        keywords = []
        
        # Generate comparison keywords
        for comparison in self.semantic_clusters['comparison']:
            for quality in self.semantic_clusters['quality']:
                keyword = f"{quality} {domain_name} {comparison} competitors"
                keywords.append({
                    'keyword': keyword,
                    'volume': random.randint(200, 1500),
                    'cpc': round(random.uniform(2.0, 8.0), 2),
                    'competition': 'High',
                    'intent': 'commercial',
                    'keyword_type': 'long-tail',
                    'difficulty': '65/100',
                    'commercial_value': 'High',
                    'content_opportunity': 'Comparison pages'
                })
        
        # Generate cost-focused keywords
        for cost_term in self.semantic_clusters['cost']:
            for size in self.semantic_clusters['size']:
                keyword = f"{cost_term} {domain_name} for {size}"
                keywords.append({
                    'keyword': keyword,
                    'volume': random.randint(300, 2000),
                    'cpc': round(random.uniform(1.5, 5.0), 2),
                    'competition': 'Medium',
                    'intent': 'commercial',
                    'keyword_type': 'long-tail',
                    'difficulty': '45/100',
                    'commercial_value': 'High',
                    'content_opportunity': 'Pricing pages'
                })
        
        return keywords[:15]  # Limit semantic keywords
    
    def extract_company_name(self, domain: str) -> str:
        """Extract company name from domain"""
        name = domain.replace('.com', '').replace('.org', '').replace('.net', '').replace('.io', '')
        
        special_names = {
            'github': 'GitHub',
            'openai': 'OpenAI',
            'anthropic': 'Anthropic',
            'youtube': 'YouTube'
        }
        
        return special_names.get(name.lower(), name.title())
    
    def calculate_difficulty(self, competition: str, volume: int) -> str:
        """Calculate keyword difficulty score"""
        base_difficulty = {'Low': 25, 'Medium': 50, 'High': 75}
        
        # Adjust based on volume
        volume_adjustment = min(volume // 1000, 20)
        
        final_difficulty = base_difficulty[competition] + volume_adjustment
        return f"{min(final_difficulty, 95)}/100"
    
    def calculate_commercial_value(self, intent_type: str, cpc: float) -> str:
        """Calculate commercial value of keyword"""
        if intent_type == 'commercial' and cpc > 5.0:
            return 'High'
        elif intent_type in ['commercial', 'industry_specific'] and cpc > 2.0:
            return 'Medium'
        else:
            return 'Low'
    
    def suggest_content_type(self, intent_type: str, keyword: str) -> str:
        """Suggest content type for the keyword"""
        content_mapping = {
            'commercial': 'Product/pricing pages',
            'informational': 'Blog posts/tutorials',
            'problem_solving': 'Support/troubleshooting guides',
            'feature_specific': 'Feature documentation',
            'industry_specific': 'Industry landing pages',
            'trending': 'Thought leadership content'
        }
        
        return content_mapping.get(intent_type, 'Blog content')
    
    def calculate_strategic_value(self, keyword_data: Dict) -> int:
        """Calculate strategic value for sorting"""
        volume = keyword_data.get('volume', 0)
        cpc = keyword_data.get('cpc', 0)
        
        # Weight by commercial intent
        intent_multiplier = {
            'commercial': 3,
            'industry_specific': 2.5,
            'feature_specific': 2,
            'problem_solving': 1.5,
            'informational': 1,
            'trending': 1.2
        }
        
        intent = keyword_data.get('intent', 'informational')
        multiplier = intent_multiplier.get(intent, 1)
        
        return int((volume * 0.7 + cpc * 100) * multiplier)