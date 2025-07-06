#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from api.enhanced_analyze import handler
from io import StringIO
import json

class MockRequest:
    def __init__(self, data):
        self.data = data
        
class MockHeaders:
    def __init__(self):
        self.headers = {'Content-Length': str(len(json.dumps({"url": "https://desertrecoverycenters.com/", "region": "US"}).encode()))}
    
    def __getitem__(self, key):
        return self.headers[key]

def test_enhanced_analyzer():
    print("🧪 Testing Enhanced Analyzer Locally\n")
    
    # Create mock handler
    test_handler = handler()
    test_handler.headers = MockHeaders()
    
    # Mock the rfile.read method
    test_data = {"url": "https://desertrecoverycenters.com/", "region": "US"}
    test_handler.rfile = type('MockRFile', (), {
        'read': lambda self, length: json.dumps(test_data).encode()
    })()
    
    # Mock the response methods
    responses = []
    headers = []
    
    def mock_send_response(code):
        responses.append(f"Response: {code}")
    
    def mock_send_header(name, value):
        headers.append(f"{name}: {value}")
    
    def mock_end_headers():
        headers.append("END_HEADERS")
    
    output_data = []
    def mock_write(data):
        output_data.append(data.decode() if isinstance(data, bytes) else data)
    
    test_handler.send_response = mock_send_response
    test_handler.send_header = mock_send_header
    test_handler.end_headers = mock_end_headers
    test_handler.wfile = type('MockWFile', (), {'write': mock_write})()
    
    # Test the POST method
    try:
        test_handler.do_POST()
        
        print("✅ Enhanced analyzer executed successfully!")
        print(f"📊 Responses: {responses}")
        
        if output_data:
            result = json.loads(output_data[0])
            print(f"📋 URL analyzed: {result.get('url')}")
            print(f"🔍 Keywords found: {result.get('keywords_found')}")
            print(f"🏢 Industry: {result.get('website_analysis', {}).get('detected_industry')}")
            print(f"📍 Locations: {result.get('website_analysis', {}).get('locations_found')}")
            print(f"📊 Version: {result.get('website_analysis', {}).get('version')}")
            
            # Show healthcare keywords
            keywords = result.get('keywords', [])
            healthcare_keywords = [kw for kw in keywords if any(term in kw['keyword'].lower() for term in ['rehab', 'addiction', 'treatment', 'recovery', 'arizona'])]
            
            print(f"\n🏥 Healthcare keywords found: {len(healthcare_keywords)}")
            for i, kw in enumerate(healthcare_keywords[:10], 1):
                print(f"   {i}. {kw['keyword']}")
                print(f"      📈 Volume: {kw['volume']:,}")
                print(f"      💰 CPC: ${kw['cpc']}")
                print(f"      🎯 Intent: {kw['intent']}")
                
            print(f"\n📊 Data source: {result.get('data_source')}")
            print(f"🔍 Method: {result.get('extraction_method')}")
            
    except Exception as e:
        print(f"❌ Error testing enhanced analyzer: {str(e)}")

if __name__ == "__main__":
    test_enhanced_analyzer()