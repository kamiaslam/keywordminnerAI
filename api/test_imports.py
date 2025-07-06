from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        try:
            # Test imports
            import requests
            import_status = {"requests": "✅ Available"}
            
            try:
                from bs4 import BeautifulSoup
                import_status["beautifulsoup4"] = "✅ Available"
            except ImportError as e:
                import_status["beautifulsoup4"] = f"❌ Failed: {str(e)}"
            
            try:
                from website_content_analyzer import WebsiteContentAnalyzer
                import_status["WebsiteContentAnalyzer"] = "✅ Available"
                
                # Test basic functionality
                analyzer = WebsiteContentAnalyzer()
                import_status["analyzer_init"] = "✅ Initialized successfully"
            except ImportError as e:
                import_status["WebsiteContentAnalyzer"] = f"❌ Failed: {str(e)}"
            except Exception as e:
                import_status["analyzer_init"] = f"❌ Init failed: {str(e)}"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "Import test results",
                "imports": import_status,
                "python_version": sys.version,
                "current_directory": os.getcwd(),
                "files_in_api": [f for f in os.listdir('.') if f.endswith('.py')]
            }
            
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"error": f"Test failed: {str(e)}"}
            self.wfile.write(json.dumps(response).encode())