import json
import urllib.request

req = urllib.request.Request("https://openrouter.ai/api/v1/models")
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())

free_models = [m["id"] for m in data["data"] if ":free" in m["id"]]
for m in free_models[:20]:
    print(m)
