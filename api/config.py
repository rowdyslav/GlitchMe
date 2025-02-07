import json

with open("config.json") as f:
    cfg = json.load(f)

ROUNDS_QUESTIONS: dict[str, list[str]] = cfg["rounds_questions"]
MAX_ROUNDS_COUNT: int = len(ROUNDS_QUESTIONS)

MIN_PLAYERS_COUNT: int = cfg["min_players_count"]
