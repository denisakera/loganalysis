#!/usr/bin/env python3
"""
Simple local HTTP server for viewing interactive visualizations.
Run this script, then open http://localhost:8000/interactive_visualizations.html in your browser.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow local file access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def log_message(self, format, *args):
        # Suppress default logging
        pass

def main():
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    Handler = MyHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Starting local server at http://localhost:{PORT}")
        print(f"\nAvailable files:")
        print(f"  - http://localhost:{PORT}/interactive_visualizations.html")
        print(f"  - http://localhost:{PORT}/relational_interaction_visualizations.html")
        print(f"  - http://localhost:{PORT}/topic_emergence_visualizations.html")
        print(f"\nPress Ctrl+C to stop the server")
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}/interactive_visualizations.html')
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == "__main__":
    main()
