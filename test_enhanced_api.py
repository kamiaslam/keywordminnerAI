#!/usr/bin/env python3

from api.google_trends_api import GoogleTrendsAPI

def test_enhanced_api():
    print("🚀 Testing Enhanced Google Trends Style API\n")
    
    api = GoogleTrendsAPI()
    
    # Test Google Trends data
    print("1. Testing Google Trends Data for 'shopify':")
    trends_data = api.get_google_trends_data('shopify', 'US')
    
    print(f"   📊 Monthly Search Volume: {trends_data['search_volume']['monthly_searches']:,}")
    print(f"   💰 Suggested Bid: ${trends_data['suggested_bid']['suggested_bid']}")
    print(f"   🎯 Competition: {trends_data['competition_level']['level']} ({trends_data['competition_level']['score']})")
    print(f"   🔍 Search Intent: {trends_data['search_intent']['primary_intent']}")
    print(f"   📈 Trend Status: {trends_data['seasonal_patterns']['volatility']}")
    print(f"   🌍 Top Region: {trends_data['interest_by_region'][0]['region']} ({trends_data['interest_by_region'][0]['interest']}%)")
    
    print(f"\n   📅 12-Month Trend Data (last 3 months):")
    for data_point in trends_data['trend_data'][-3:]:
        print(f"      {data_point['date']}: {data_point['interest']}% interest")
    
    print(f"\n   🔗 Related Queries (top 3):")
    for i, query in enumerate(trends_data['related_queries'][:3], 1):
        print(f"      {i}. {query['query']} - Vol: {query['volume']:,} - CPC: ${query['cpc']}")
    
    print(f"\n   📈 Rising Queries (top 3):")
    for i, query in enumerate(trends_data['rising_queries'][:3], 1):
        print(f"      {i}. {query['query']} - Growth: {query['growth_percentage']}")
    
    # Test keyword ideas generator
    print(f"\n2. Testing Keyword Ideas Generator for 'shopify':")
    keyword_ideas = api.get_keyword_ideas('shopify', 'US')
    
    print(f"   💡 Generated {len(keyword_ideas)} keyword ideas:")
    for i, idea in enumerate(keyword_ideas[:5], 1):
        print(f"      {i}. {idea['keyword']}")
        print(f"         Volume: {idea['search_volume']:,} | CPC: ${idea['cpc']} | Competition: {idea['competition']}")
        print(f"         Intent: {idea['intent']} | Difficulty: {idea['difficulty']}")
    
    print(f"\n✅ Enhanced API testing completed successfully!")

if __name__ == "__main__":
    test_enhanced_api()