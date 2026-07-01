import sys
import urllib.request
import json

ENDPOINTS = [
    ("http://localhost:5000/health", 'json'),
    ("http://localhost:5000/api/festival", 'json'),
    ("http://localhost:5000/api/artistas", 'json'),
    ("http://localhost:8000/index.html", 'text')
]

def fetch(url, kind='json'):
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            status = resp.getcode()
            body = resp.read()
            if status != 200 and status != 201:
                return False, f"{url} returned status {status}"
            if kind == 'json':
                try:
                    data = json.loads(body.decode('utf-8'))
                    return True, data
                except Exception as e:
                    return False, f"{url} returned invalid JSON: {e}"
            else:
                text = body.decode('utf-8', errors='ignore')
                return True, text
    except Exception as e:
        return False, str(e)

all_ok = True
for url, kind in ENDPOINTS:
    ok, result = fetch(url, kind)
    if ok:
        print(f"OK: {url}")
    else:
        print(f"ERROR: {url} -> {result}")
        all_ok = False

if not all_ok:
    print('\nOne or more checks failed.')
    sys.exit(2)
else:
    print('\nAll checks passed.')
    sys.exit(0)
