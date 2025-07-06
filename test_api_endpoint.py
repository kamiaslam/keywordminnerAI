#!/usr/bin/env python3

import requests
import json

def test_keyword_analysis_api():
    print("🚀 Testing Enhanced Keyword Analysis API\n")
    
    # Local test URL (assuming you're running the API locally)
    api_url = "https://keywordminer-ai-mindmetas-projects.vercel.app/api/simple_analyze"
    
    # Test with the desert recovery centers website
    test_data = {
        "url": "https://desertrecoverycenters.com/",
        "region": "US"
    }
    
    print(f"📊 Testing API with: {test_data['url']}")
    
    try:
        response = requests.post(api_url, json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ API call successful!")
            print(f"📋 URL analyzed: {result.get('url')}")
            print(f"🔍 Keywords found: {result.get('keywords_found')}")
            print(f"📊 Total volume: {result.get('total_volume'):,}")
            print(f"💰 Average CPC: ${result.get('avg_cpc')}")
            
            # Show website analysis data
            website_analysis = result.get('website_analysis', {})
            print(f"\n🌐 Website Analysis:")
            print(f"   📋 Title: {website_analysis.get('title')}")
            print(f"   🏢 Industry: {website_analysis.get('detected_industry')}")
            print(f"   📍 Locations: {website_analysis.get('locations_found')}")
            print(f"   🔍 Method: {website_analysis.get('content_analysis_method')}")
            
            # Show top keywords
            keywords = result.get('keywords', [])
            print(f"\n🎯 Top Keywords from API:")
            for i, keyword in enumerate(keywords[:10], 1):
                print(f"   {i}. {keyword['keyword']}")
                print(f"      📈 Volume: {keyword['volume']:,}")
                print(f"      💰 CPC: ${keyword['cpc']}")
                print(f"      🎯 Intent: {keyword['intent']}")
                if 'keyword_type' in keyword:
                    print(f"      🏷️  Source: {keyword['keyword_type']}")
                print()
            
            # Check for healthcare-specific keywords
            healthcare_keywords = [kw for kw in keywords if any(term in kw['keyword'].lower() for term in ['rehab', 'addiction', 'treatment', 'recovery', 'detox'])]
            if healthcare_keywords:
                print(f"🏥 Healthcare keywords found: {len(healthcare_keywords)}")
                for kw in healthcare_keywords[:5]:
                    print(f"   • {kw['keyword']} (Volume: {kw['volume']:,})")
            
            print(f"\n📊 Data source: {result.get('data_source')}")
            print(f"🔍 Extraction method: {result.get('extraction_method')}")
            
        else:
            print(f"❌ API call failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_keyword_analysis_api()