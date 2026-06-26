import requests

url = "http://localhost:8000/api/chat/stream"
payload = {
    "session_id": "test_session",
    "messages": [
        {"role": "user", "content": "summarize"}
    ],
    "model": "google/gemma-4-31b-it:free",
    "search_strategy": "hybrid",
    "top_k": 4,
    "similarity_threshold": 0.5
}
response = requests.post(url, json=payload, stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
