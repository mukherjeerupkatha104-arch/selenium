"""Robot variable file: configuration is read once, with safe CLI overrides."""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_dotenv() -> None:
    dotenv = ROOT / ".env"
    if not dotenv.exists():
        return
    for line in dotenv.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def get_variables() -> dict[str, object]:
    _load_dotenv()
    settings = json.loads((ROOT / "config" / "environments.json").read_text(encoding="utf-8"))
    environment = os.getenv("ENVIRONMENT", "qa").lower()
    if environment not in settings:
        raise ValueError(f"Unknown ENVIRONMENT '{environment}'. Choose one of: {', '.join(settings)}")
    active = settings[environment]
    return {
        "ENVIRONMENT": environment,
        "BASE_URL": os.getenv("BASE_URL", active["base_url"]),
        "BROWSER": os.getenv("BROWSER", "chrome"),
        "HEADLESS": os.getenv("HEADLESS", active["headless"]),
        "TIMEOUT": os.getenv("TIMEOUT", active["timeout"]),
        "SCREENSHOT_ON_FAILURE": os.getenv("SCREENSHOT_ON_FAILURE", active["screenshot_on_failure"]),
        "TEST_EMAIL": os.getenv("AE_EMAIL", ""),
        "TEST_PASSWORD": os.getenv("AE_PASSWORD", ""),
        "BUILD_ID": os.getenv("BUILD_ID", "local"),
    }
