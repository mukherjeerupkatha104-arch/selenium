"""Robot variable file that isolates test cases from the JSON data format."""
from __future__ import annotations

import json
from pathlib import Path


def get_variables() -> dict[str, object]:
    path = Path(__file__).resolve().parents[1] / "data" / "product_matrix.json"
    return {"PRODUCT_CASES": json.loads(path.read_text(encoding="utf-8"))}
