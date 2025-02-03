import json
from typing import Dict, List

with open("rounds_data.json") as f:
    ROUNDS_DATA: Dict[str, List[str]] = json.load(f)
