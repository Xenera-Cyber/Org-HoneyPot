import urllib.request
import json

def test_endpoint(url):
    print(f"Testing {url}...")
    try:
        response = urllib.request.urlopen(url, timeout=3)
        status = response.getcode()
        content = json.loads(response.read().decode('utf-8'))
        print(f"[{status}] Success!")
        print(f"Keys returned: {list(content.keys())}")
        if 'honeypotOnline' in content:
            print(f"  Honeypot Online: {content['honeypotOnline']}")
        if 'activeSessions' in content:
            print(f"  Active Sessions: {content['activeSessions']}")
        if 'reachable' in content:
            print(f"  AI Reachable: {content['reachable']}")
    except Exception as e:
        print(f"[-] Failed: {e}")
    print("-" * 50)

if __name__ == "__main__":
    test_endpoint("http://localhost:8000/api/monitoring")
    test_endpoint("http://localhost:8000/api/sessions")
    test_endpoint("http://localhost:8000/api/threats")
    test_endpoint("http://localhost:8000/api/ai")
    test_endpoint("http://localhost:8000/api/ai/config")
    test_endpoint("http://localhost:8000/api/honeypot/config")
