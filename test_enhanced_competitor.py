#!/usr/bin/env python3

from api.real_competitor_intel import RealCompetitorIntelligence
from api.longtail_generator import ProgrammaticLongTailGenerator

def test_real_competitor_intelligence():
    print("🚀 Testing Real Competitor Intelligence\n")
    
    intel = RealCompetitorIntelligence()
    
    # Test with different types of companies
    test_domains = ['shopify.com', 'openai.com', 'stripe.com', 'github.com']
    
    for domain in test_domains:
        print(f"📊 Analyzing competitors for {domain}:")
        
        # Detect industry
        domain_name = domain.split('.')[0]
        industry = intel.detect_industry(domain_name)
        print(f"   🏢 Industry: {industry}")
        
        # Get competitors
        competitors = intel.analyze_competitors(domain)
        print(f"   🏆 Found {len(competitors)} competitors:")
        
        for i, comp in enumerate(competitors[:3], 1):
            print(f"   {i}. {comp['company_name']} ({comp['domain']})")
            print(f"      📈 Traffic: {comp['monthly_traffic']:,}/month")
            print(f"      🎯 Authority: {comp['domain_authority']}")
            print(f"      🌍 Global Rank: #{comp['global_rank']:,}")
            print(f"      💰 Est. Revenue: {comp['estimated_revenue']}")
            print(f"      🔧 Tech: {', '.join(comp['technology_stack'][:3])}")
            
        print()

def test_programmatic_longtail():
    print("🎯 Testing Programmatic Long-Tail Generator\n")
    
    generator = ProgrammaticLongTailGenerator()
    
    # Test with different industries
    test_cases = [
        ('shopify', 'ecommerce'),
        ('openai', 'ai'),
        ('stripe', 'finance'),
        ('salesforce', 'saas')
    ]
    
    for domain_name, industry in test_cases:
        print(f"🔍 Generating long-tail keywords for {domain_name} ({industry}):")
        
        keywords = generator.generate_longtail_keywords(domain_name, industry, 15)
        
        # Categorize by intent
        intents = {}
        for kw in keywords:
            intent = kw.get('intent', 'unknown')
            if intent not in intents:
                intents[intent] = []
            intents[intent].append(kw)
        
        print(f"   📊 Generated {len(keywords)} strategic keywords")
        print(f"   🎯 Intent breakdown: {', '.join(f'{k}: {len(v)}' for k, v in intents.items())}")
        
        # Show top commercial keywords
        commercial_kw = [kw for kw in keywords if kw.get('commercial_value') == 'High']
        if commercial_kw:
            print(f"   💰 Top commercial keywords:")
            for kw in commercial_kw[:3]:
                print(f"      • {kw['keyword']} (Vol: {kw['volume']:,}, CPC: ${kw['cpc']})")
        
        # Show top informational keywords
        info_kw = [kw for kw in keywords if kw.get('intent') == 'informational']
        if info_kw:
            print(f"   📚 Top informational keywords:")
            for kw in info_kw[:2]:
                print(f"      • {kw['keyword']} (Vol: {kw['volume']:,})")
        
        print()

if __name__ == "__main__":
    print("🧪 Testing Enhanced Competitor Intelligence & Long-Tail Generation\n")
    test_real_competitor_intelligence()
    test_programmatic_longtail()
    print("✅ All tests completed successfully!")