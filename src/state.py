"""
Central in-memory state store. Single source of truth for all projects, tasks, loops.
Persists to data/state.json on every mutation.
"""
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any
import uuid

DATA_FILE = Path(__file__).parent.parent / "data" / "state.json"
DATA_FILE.parent.mkdir(exist_ok=True)

DEFAULT_GLOBAL_SETTINGS = {
    "auto_refresh_interval": 3,
    "process_scan_interval": 5,
    "watch_filesystem": True,
    "notifications_enabled": True,
    "theme": "dark",
    "default_priority": "medium",
    "max_loop_iterations": 10,
    "ai_brains": {
        "claude": {"enabled": True, "model": "claude-sonnet-4-6", "api_key": ""},
        "openai": {"enabled": False, "model": "gpt-4o", "api_key": ""},
        "gemini": {"enabled": False, "model": "gemini-2.0-flash", "api_key": ""},
        "grok": {"enabled": False, "model": "grok-3", "api_key": ""},
        "deepseek": {"enabled": False, "model": "deepseek-coder", "api_key": ""},
        "ollama": {"enabled": False, "model": "llama3.2", "base_url": "http://localhost:11434"},
    },
    "integrations": {
        "github": {"enabled": False, "token": "", "repo": ""},
        "slack": {"enabled": False, "webhook_url": ""},
        "jira": {"enabled": False, "base_url": "", "token": "", "project_key": ""},
        "linear": {"enabled": False, "api_key": "", "team_id": ""},
        "notion": {"enabled": False, "token": "", "database_id": ""},
        "discord": {"enabled": False, "webhook_url": ""},
    },
}

DEFAULT_PROJECT_SETTINGS = {
    "watch_filesystem": True,
    "notifications_enabled": True,
    "default_priority": "medium",
    "default_brain": "claude",
    "auto_create_notes": True,
    "allowed_brains": ["claude"],
    "integrations": {
        "github": {"enabled": False, "repo": ""},
        "jira": {"enabled": False, "project_key": ""},
        "linear": {"enabled": False, "team_id": ""},
    },
}

_state: dict[str, Any] = {
    "projects": {},
    "tasks": {},
    "loops": {},
    "processes": [],
    "settings": {"global": dict(DEFAULT_GLOBAL_SETTINGS), "projects": {}},
    "updated_at": None,
}
_subscribers: list[asyncio.Queue] = []


def now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _load():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text())
            _state.update({k: v for k, v in data.items() if k != "processes"})
            # Merge any new default keys added since last save
            if "settings" not in _state:
                _state["settings"] = {"global": dict(DEFAULT_GLOBAL_SETTINGS), "projects": {}}
            for k, v in DEFAULT_GLOBAL_SETTINGS.items():
                if k not in _state["settings"].get("global", {}):
                    _state["settings"]["global"][k] = v
        except Exception:
            pass


def _save():
    to_save = {k: v for k, v in _state.items() if k != "processes"}
    to_save["updated_at"] = now()
    DATA_FILE.write_text(json.dumps(to_save, indent=2))


async def _broadcast(event: dict):
    dead = []
    for q in _subscribers:
        try:
            q.put_nowait(event)
        except asyncio.QueueFull:
            dead.append(q)
    for q in dead:
        _subscribers.remove(q)


def subscribe() -> asyncio.Queue:
    q: asyncio.Queue = asyncio.Queue(maxsize=100)
    _subscribers.append(q)
    return q


def unsubscribe(q: asyncio.Queue):
    if q in _subscribers:
        _subscribers.remove(q)


# ── Projects ──────────────────────────────────────────────────────────────────

def get_projects() -> dict:
    return _state["projects"]


def upsert_project(folder: str, name: str | None = None) -> dict:
    pid = str(Path(folder).resolve())
    if pid not in _state["projects"]:
        _state["projects"][pid] = {
            "id": pid,
            "name": name or Path(folder).name,
            "folder": pid,
            "created_at": now(),
            "task_count": 0,
            "open_issues": 0,
        }
    elif name:
        _state["projects"][pid]["name"] = name
    _save()
    asyncio.create_task(_broadcast({"type": "project_updated", "data": _state["projects"][pid]}))
    return _state["projects"][pid]


# ── Tasks ─────────────────────────────────────────────────────────────────────

def get_tasks(project_id: str | None = None) -> list[dict]:
    tasks = list(_state["tasks"].values())
    if project_id:
        tasks = [t for t in tasks if t.get("project_id") == project_id]
    return sorted(tasks, key=lambda t: t.get("created_at", ""), reverse=True)


def create_task(project_id: str, title: str, description: str = "",
                priority: str = "medium", tags: list[str] | None = None) -> dict:
    tid = str(uuid.uuid4())
    task = {
        "id": tid,
        "project_id": project_id,
        "title": title,
        "description": description,
        "status": "open",
        "priority": priority,
        "tags": tags or [],
        "loop_count": 0,
        "notes_path": None,
        "created_at": now(),
        "updated_at": now(),
    }
    _state["tasks"][tid] = task
    if project_id in _state["projects"]:
        _state["projects"][project_id]["task_count"] += 1
    _save()
    asyncio.create_task(_broadcast({"type": "task_created", "data": task}))
    return task


def update_task(task_id: str, **kwargs) -> dict | None:
    if task_id not in _state["tasks"]:
        return None
    _state["tasks"][task_id].update(kwargs)
    _state["tasks"][task_id]["updated_at"] = now()
    _save()
    asyncio.create_task(_broadcast({"type": "task_updated", "data": _state["tasks"][task_id]}))
    return _state["tasks"][task_id]


# ── Loops ─────────────────────────────────────────────────────────────────────

def get_loops() -> list[dict]:
    return list(_state["loops"].values())


def create_loop(task_id: str, goal: str, max_iterations: int = 10) -> dict:
    lid = str(uuid.uuid4())
    loop = {
        "id": lid,
        "task_id": task_id,
        "goal": goal,
        "status": "running",
        "iteration": 0,
        "max_iterations": max_iterations,
        "log": [],
        "started_at": now(),
        "updated_at": now(),
    }
    _state["loops"][lid] = loop
    _save()
    asyncio.create_task(_broadcast({"type": "loop_created", "data": loop}))
    return loop


def append_loop_log(loop_id: str, message: str, level: str = "info"):
    if loop_id not in _state["loops"]:
        return
    entry = {"ts": now(), "level": level, "msg": message}
    _state["loops"][loop_id]["log"].append(entry)
    _state["loops"][loop_id]["iteration"] += 1
    _state["loops"][loop_id]["updated_at"] = now()
    _save()
    asyncio.create_task(_broadcast({"type": "loop_log", "loop_id": loop_id, "entry": entry}))


def finish_loop(loop_id: str, status: str = "done"):
    if loop_id not in _state["loops"]:
        return
    _state["loops"][loop_id]["status"] = status
    _state["loops"][loop_id]["updated_at"] = now()
    _save()
    asyncio.create_task(_broadcast({"type": "loop_finished", "loop_id": loop_id, "status": status}))


# ── Processes (ephemeral) ─────────────────────────────────────────────────────

def set_processes(procs: list[dict]):
    _state["processes"] = procs
    asyncio.create_task(_broadcast({"type": "processes_updated", "data": procs}))


def get_processes() -> list[dict]:
    return _state["processes"]


def get_snapshot() -> dict:
    return {
        "projects": list(_state["projects"].values()),
        "tasks": get_tasks(),
        "loops": get_loops(),
        "processes": _state["processes"],
        "settings": _state.get("settings", {}),
        "updated_at": _state.get("updated_at"),
    }


# ── Settings ──────────────────────────────────────────────────────────────────

def get_global_settings() -> dict:
    return _state["settings"].get("global", dict(DEFAULT_GLOBAL_SETTINGS))


def update_global_settings(updates: dict) -> dict:
    current = _state["settings"].setdefault("global", dict(DEFAULT_GLOBAL_SETTINGS))
    _deep_merge(current, updates)
    _save()
    asyncio.create_task(_broadcast({"type": "settings_updated", "data": _state["settings"]}))
    return current


def get_project_settings(project_id: str) -> dict:
    import copy
    base = copy.deepcopy(DEFAULT_PROJECT_SETTINGS)
    saved = _state["settings"].get("projects", {}).get(project_id, {})
    _deep_merge(base, saved)
    return base


def update_project_settings(project_id: str, updates: dict) -> dict:
    proj_settings = _state["settings"].setdefault("projects", {})
    if project_id not in proj_settings:
        import copy
        proj_settings[project_id] = copy.deepcopy(DEFAULT_PROJECT_SETTINGS)
    _deep_merge(proj_settings[project_id], updates)
    _save()
    asyncio.create_task(_broadcast({"type": "settings_updated", "data": _state["settings"]}))
    return proj_settings[project_id]


def _deep_merge(base: dict, updates: dict):
    for k, v in updates.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


_load()
