import json

with open("config.json") as f:
    cfg = json.load(f)

API_URL: str = cfg["api_url"]
