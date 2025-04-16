import json

from pydantic import AnyUrl

with open("config.json", encoding="UTF-8") as f:
    cfg = json.load(f)


ROUNDS_QUESTIONS: dict[str, list[str]] = cfg["rounds_questions"]
ROUNDS_MAX_COUNT: int = len(ROUNDS_QUESTIONS)

QR_BACKGROUND_URL: AnyUrl = AnyUrl(cfg["qr_background_url"])
