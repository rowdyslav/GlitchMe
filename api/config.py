import json

from pydantic import AnyUrl

with open("config.json") as f:
    cfg = json.load(f)

MIN_PLAYERS_COUNT: int = cfg["min_players_count"]

QR_BACKGROUND_URL: AnyUrl = AnyUrl(cfg["qr_background_url"])
QR_BACKGROUND_KIND: str = cfg["qr_background_kind"]

ROUNDS_QUESTIONS: dict[str, list[str]] = cfg["rounds_questions"]
MAX_ROUNDS_COUNT: int = len(ROUNDS_QUESTIONS)
