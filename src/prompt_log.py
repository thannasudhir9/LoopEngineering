"""
Prompt / interaction logger.
Appends JSONL entries to logs/prompts-YYYY-MM-DD.jsonl.
One line per action, never truncated, daily rotation.
"""
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

_lock = asyncio.Lock()


def _today_file() -> Path:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return LOGS_DIR / f"prompts-{day}.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


async def log(event_type: str, **kwargs):
    entry = {"ts": _now(), "type": event_type, **kwargs}
    line = json.dumps(entry, default=str) + "\n"
    async with _lock:
        with _today_file().open("a") as f:
            f.write(line)


def log_sync(event_type: str, **kwargs):
    entry = {"ts": _now(), "type": event_type, **kwargs}
    line = json.dumps(entry, default=str) + "\n"
    with _today_file().open("a") as f:
        f.write(line)


def read_logs(days: int = 7) -> list[dict]:
    entries = []
    for f in sorted(LOGS_DIR.glob("prompts-*.jsonl"), reverse=True)[:days]:
        try:
            for line in f.read_text().splitlines():
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except Exception:
                        pass
        except Exception:
            pass
    return entries
