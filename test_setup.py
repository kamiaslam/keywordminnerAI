#!/usr/bin/env python3

import subprocess
import sys
import time

def check_installation():
    print("🔍 Checking KeywordMiner setup...\n")
    
    # Check Python version
    print(f"✓ Python version: {sys.version}")
    
    # Check required packages
    packages = ['fastapi', 'uvicorn', 'playwright', 'bs4', 'nltk']
    missing = []
    
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip3 install -r requirements.txt")
        return False
    
    # Test NLTK data
    try:
        import nltk
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        print("✓ NLTK data downloaded")
    except LookupError:
        print("✗ NLTK data not downloaded")
        print("Run: python3 -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords')\"")
        return False
    
    # Test backend import
    try:
        sys.path.append('backend')
        from main import app
        print("✓ Backend imports correctly")
    except Exception as e:
        print(f"✗ Backend import error: {e}")
        return False
    
    print("\n✅ All checks passed! You can now run ./start.sh")
    return True

if __name__ == "__main__":
    check_installation()