#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

def test_enhanced_analyzer_methods():
    print("🧪 Testing Enhanced Analyzer Methods\n")
    
    # Import the handler class
    from enhanced_analyze import handler
    
    # Create a mock handler instance with minimal setup
    class TestHandler:
        def detect_industry_from_domain(self, domain_name: str) -> str:
            domain_lower = domain_name.lower()
            
            if any(word in domain_lower for word in ['recovery', 'rehab', 'treatment', 'detox', 'addiction', 'sober']):
                return 'healthcare_rehab'
            elif any(word in domain_lower for word in ['medical', 'health', 'clinic', 'hospital', 'doctor']):
                return 'healthcare_medical'
            else:
                return 'general'
        
        def generate_healthcare_rehab_keywords(self, domain_name: str):
            # Import from the enhanced_analyze module
            import enhanced_analyze
            temp_handler = type('TempHandler', (), {})()
            # Copy the method
            temp_handler.generate_healthcare_rehab_keywords = enhanced_analyze.handler.generate_healthcare_rehab_keywords.__get__(temp_handler, type(temp_handler))
            return temp_handler.generate_healthcare_rehab_keywords(domain_name)
    
    test_handler = TestHandler()
    
    # Test industry detection
    print("🏢 Testing Industry Detection:")
    test_domains = ["desertrecoverycenters", "medicalcenter", "lawfirm", "autorepair"]
    for domain in test_domains:
        industry = test_handler.detect_industry_from_domain(domain)
        print(f"   {domain} → {industry}")
    
    # Test healthcare keyword generation for desert recovery centers
    print(f"\n🏥 Testing Healthcare Keyword Generation:")
    try:
        keywords = test_handler.generate_healthcare_rehab_keywords("desertrecoverycenters")
        print(f"✅ Generated {len(keywords)} healthcare keywords")
        
        print(f"\n🎯 Top Healthcare Keywords:")
        for i, kw in enumerate(keywords[:10], 1):
            print(f"   {i}. {kw['keyword']}")
            print(f"      📈 Volume: {kw['volume']:,}")
            print(f"      💰 CPC: ${kw['cpc']}")
            print(f"      🎯 Intent: {kw['intent']}")
            print(f"      🏷️  Type: {kw['keyword_type']}")
            print()
        
        # Check for Arizona-specific keywords
        arizona_keywords = [kw for kw in keywords if 'arizona' in kw['keyword'].lower()]
        phoenix_keywords = [kw for kw in keywords if 'phoenix' in kw['keyword'].lower()]
        
        print(f"📍 Arizona-specific keywords: {len(arizona_keywords)}")
        print(f"📍 Phoenix-specific keywords: {len(phoenix_keywords)}")
        
        # Show sample Arizona keywords
        if arizona_keywords:
            print(f"\n🌵 Sample Arizona Keywords:")
            for kw in arizona_keywords[:5]:
                print(f"   • {kw['keyword']} (Vol: {kw['volume']:,}, CPC: ${kw['cpc']})")
        
    except Exception as e:
        print(f"❌ Error generating healthcare keywords: {str(e)}")

if __name__ == "__main__":
    test_enhanced_analyzer_methods()