import json
import os
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
CONTENT_FILE = BASE_DIR / "content" / "site.json"


def load_site() -> dict[str, Any]:
    with CONTENT_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def public_site_url(request_url: str) -> str:
    configured_url = os.getenv("PUBLIC_SITE_URL", "").strip().rstrip("/")
    if configured_url:
        return configured_url
    return request_url.split("/", 3)[0] + "//" + request_url.split("/", 3)[2]
