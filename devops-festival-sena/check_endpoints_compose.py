import time
import urllib.request
import json

ENDPOINTS = [
    ("http://localhost:5000/health", 'json'),
    ("http://localhost:5000/api/festival", 'json'),
    ("http://localhost:5000/api/artistas", 'json'),
    ("http://localhost:8080/index.html", 'text')
]

TIMEOUT = 40
INTERVAL = 3

def fetch(url, kind='json'):
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            status = resp.getcode()
            body = resp.read()
            if status not in (200,201):
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

start = time.time()
all_ok = False
while time.time() - start < TIMEOUT:
    all_ok = True
    errors = []
    for url, kind in ENDPOINTS:
        ok, result = fetch(url, kind)
        if ok:
            print(f"OK: {url}")
        else:
            all_ok = False
            errors.append((url, result))
            print(f"WAIT: {url} -> {result}")
    if all_ok:
        break
    time.sleep(INTERVAL)

if all_ok:
    print('\nAll checks passed.')
    raise SystemExit(0)
else:
    print('\nSome checks failed or timed out:')
    for u, r in errors:
        print(f"ERROR: {u} -> {r}")
    raise SystemExit(2)
