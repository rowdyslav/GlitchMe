import json

with open("rounds_data.json") as f:
    ROUNDS_DATA: dict[str, list[str]] = json.load(f)
