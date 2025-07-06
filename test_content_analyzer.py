#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from api.website_content_analyzer import WebsiteContentAnalyzer

def test_content_analyzer():
    print("🔍 Testing Website Content Analyzer\n")
    
    analyzer = WebsiteContentAnalyzer()
    
    # Test with the desert recovery centers website
    test_url = "https://desertrecoverycenters.com/"
    
    print(f"📊 Analyzing: {test_url}")
    
    try:
        result = analyzer.analyze_website_content(test_url)
        
        print(f"✅ Analysis completed successfully!")
        print(f"📋 Title: {result['title']}")
        print(f"🏢 Industry: {result['industry']}")
        print(f"📍 Locations: {result['locations']}")
        print(f"🔍 Keywords found: {len(result['keywords'])}")
        
        print(f"\n🎯 Top Keywords:")
        for i, keyword in enumerate(result['keywords'][:10], 1):
            print(f"   {i}. {keyword['keyword']}")
            print(f"      📈 Volume: {keyword['volume']:,}")
            print(f"      💰 CPC: ${keyword['cpc']}")
            print(f"      🎯 Intent: {keyword['intent']}")
            print(f"      🏷️  Type: {keyword['keyword_type']}")
            print()
        
        # Show industry-specific keywords
        healthcare_keywords = [kw for kw in result['keywords'] if 'rehab' in kw['keyword'].lower() or 'treatment' in kw['keyword'].lower() or 'recovery' in kw['keyword'].lower()]
        if healthcare_keywords:
            print(f"🏥 Healthcare-specific keywords found:")
            for kw in healthcare_keywords[:5]:
                print(f"   • {kw['keyword']} (Volume: {kw['volume']:,})")
        
        # Show location-based keywords
        location_keywords = [kw for kw in result['keywords'] if any(loc.split(',')[0].lower() in kw['keyword'].lower() for loc in result['locations'])]
        if location_keywords:
            print(f"📍 Location-based keywords found:")
            for kw in location_keywords[:5]:
                print(f"   • {kw['keyword']} (Volume: {kw['volume']:,})")
        
    except Exception as e:
        print(f"❌ Error analyzing website: {str(e)}")
        
        # Test fallback functionality
        print(f"\n🔄 Testing fallback analysis...")
        try:
            fallback_result = analyzer.fallback_analysis(test_url, str(e))
            print(f"✅ Fallback analysis completed")
            print(f"🏢 Industry (from domain): {fallback_result['industry']}")
            print(f"🔍 Fallback keywords: {len(fallback_result['keywords'])}")
            
            print(f"\n🎯 Fallback Keywords:")
            for i, keyword in enumerate(fallback_result['keywords'][:5], 1):
                print(f"   {i}. {keyword['keyword']} (Volume: {keyword['volume']:,})")
        except Exception as fallback_error:
            print(f"❌ Fallback also failed: {str(fallback_error)}")

def test_industry_detection():
    print("\n🏢 Testing Industry Detection\n")
    
    analyzer = WebsiteContentAnalyzer()
    
    test_domains = [
        "desertrecoverycenters.com",
        "lawfirm.com", 
        "realestate.com",
        "autorepair.com",
        "medicalcenter.com"
    ]
    
    for domain in test_domains:
        domain_name = domain.split('.')[0]
        industry = analyzer.detect_industry_from_domain(domain_name)
        print(f"   {domain} → {industry}")

if __name__ == "__main__":
    print("🧪 Testing Enhanced Website Content Analysis\n")
    test_content_analyzer()
    test_industry_detection()
    print("\n✅ All tests completed!")