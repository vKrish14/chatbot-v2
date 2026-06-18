import requests
import json

payload = {
    "messages": [{"role": "user", "content": "hi"}],
    "model": "google/gemma-4-31b-it:free"
}

print("Testing /api/chat...")
response = requests.post("http://localhost:8000/api/chat", json=payload, timeout=60)
print(f"Status Code: {response.status_code}")
try:
    print(json.dumps(response.json(), indent=2))
except:
    print(response.text)
