#!/usr/bin/env python3

from api.seo_apis import SEODataProvider

def test_seo_data():
    provider = SEODataProvider()
    result = provider.extract_keywords_from_content('https://google.com')
    
    print('Real SEO data extraction test:')
    print(f'Keywords found: {len(result.get("extracted_keywords", []))}')
    print(f'Suggestions: {len(result.get("suggestions", []))}')
    print()
    
    print('First 3 keywords:')
    for i, kw in enumerate(result.get('extracted_keywords', [])[:3]):
        print(f'{i+1}. {kw.get("keyword", "N/A")} - Volume: {kw.get("volume", 0)} - CPC: ${kw.get("cpc", 0)}')
    print()
    
    print('First 3 suggestions:')
    for i, suggestion in enumerate(result.get('suggestions', [])[:3]):
        print(f'{i+1}. {suggestion}')
    print()
    
    # Test competitor analysis
    print('Testing competitor analysis:')
    competitors = provider.get_competitors_from_serp('google.com')
    print(f'Competitors found: {len(competitors)}')
    for i, comp in enumerate(competitors[:2]):
        print(f'{i+1}. {comp.get("name", "N/A")} ({comp.get("domain", "N/A")})')

if __name__ == "__main__":
    test_seo_data()