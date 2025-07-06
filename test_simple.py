#!/usr/bin/env python3

from api.seo_apis import SEODataProvider

def test_simple_site():
    provider = SEODataProvider()
    
    # Test with a simpler website
    print('Testing with a simple website:')
    result = provider.extract_keywords_from_content('https://example.com')
    
    print(f'Keywords found: {len(result.get("extracted_keywords", []))}')
    print(f'Suggestions: {len(result.get("suggestions", []))}')
    
    if result.get('extracted_keywords'):
        print('\nFirst 5 keywords:')
        for i, kw in enumerate(result.get('extracted_keywords', [])[:5]):
            print(f'{i+1}. {kw.get("keyword", "N/A")} - Volume: {kw.get("volume", 0)} - CPC: ${kw.get("cpc", 0)} - Type: {kw.get("type", "N/A")}')
    
    if result.get('suggestions'):
        print('\nFirst 5 suggestions:')
        for i, suggestion in enumerate(result.get('suggestions', [])[:5]):
            print(f'{i+1}. {suggestion}')
    
    # Test the fallback keywords function directly
    print('\n--- Testing fallback keywords for "shopify" ---')
    fallback = provider.get_fallback_keywords('shopify.com')
    print(f'Fallback keywords: {len(fallback.get("extracted_keywords", []))}')
    for i, kw in enumerate(fallback.get('extracted_keywords', [])[:3]):
        print(f'{i+1}. {kw.get("keyword", "N/A")} - Volume: {kw.get("volume", 0)} - Type: {kw.get("type", "N/A")}')

if __name__ == "__main__":
    test_simple_site()