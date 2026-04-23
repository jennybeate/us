import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent / "data" / "responses.json"


def load() -> dict:
    try:
        if DATA_FILE.exists():
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        pass
    return {}


def save(data: dict) -> None:
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def reset() -> None:
    if DATA_FILE.exists():
        DATA_FILE.unlink()


def slot_for(name: str, data: dict) -> str | None:
    for slot in ("partner1", "partner2"):
        if data.get(slot, {}).get("name") == name:
            return slot
    return None


def next_free_slot(data: dict) -> str | None:
    for slot in ("partner1", "partner2"):
        if slot not in data:
            return slot
    return None


def add_context(slot: str, name: str, context: dict) -> None:
    data = load()
    if slot not in data:
        data[slot] = {"name": name}
    data[slot]["context"] = context
    data[slot]["context_submitted_at"] = datetime.now().isoformat()
    save(data)


def add_answers(slot: str, name: str, answers: dict) -> None:
    data = load()
    if slot not in data:
        data[slot] = {"name": name}
    data[slot]["answers"] = answers
    data[slot]["answers_submitted_at"] = datetime.now().isoformat()
    save(data)


def add_pillars(slot: str, pillars: list) -> None:
    data = load()
    data[slot]["pillars"] = pillars
    data[slot]["submitted_at"] = datetime.now().isoformat()
    save(data)


def update_scores(slot: str, scores: dict) -> None:
    data = load()
    if "scores" not in data[slot]:
        data[slot]["scores"] = {}
    for pid, value in scores.items():
        data[slot]["scores"][pid] = {
            "value": value,
            "updated_at": datetime.now().isoformat(),
        }
    save(data)


def partner_stage(slot: str, data: dict) -> str:
    """Returns: 'empty', 'context', 'answers', 'pillars' (fully done)"""
    p = data.get(slot, {})
    if not p:
        return "empty"
    if "pillars" in p:
        return "pillars"
    if "answers" in p:
        return "answers"
    if "context" in p:
        return "context"
    return "empty"
