"""
LoopEngineering Server — FastAPI backend.
Serves REST API + WebSocket for the dashboard.
Run: uvicorn server:app --reload --port 7070
"""
import asyncio
import json
import os
from pathlib import Path
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src import state, monitor, watcher, notes, prompt_log, web_intel, sf_ecosystem

DASHBOARD_DIR = Path(__file__).parent / "dashboard"


CURSOR_ROOT = Path("/Users/sthanna/Downloads/Cursor")


def _seed_projects():
    if not CURSOR_ROOT.exists():
        return
    for child in sorted(CURSOR_ROOT.iterdir()):
        if child.is_dir() and not child.name.startswith("."):
            state.upsert_project(str(child))


@asynccontextmanager
async def lifespan(app: FastAPI):
    _seed_projects()
    loop = asyncio.get_event_loop()
    watcher.start_watcher(loop)
    asyncio.create_task(monitor.monitor_loop(interval=5.0))
    for proj in state.get_projects().values():
        try:
            watcher.watch_project(proj["id"], proj["folder"], loop)
        except Exception:
            pass
    yield
    watcher.stop_watcher()


app = FastAPI(title="LoopEngineering", lifespan=lifespan)

if DASHBOARD_DIR.exists():
    assets = DASHBOARD_DIR / "assets"
    if assets.exists():
        app.mount("/assets", StaticFiles(directory=str(assets)), name="assets")


@app.get("/", response_class=FileResponse)
async def serve_dashboard():
    return FileResponse(str(DASHBOARD_DIR / "index.html"))


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    q = state.subscribe()
    try:
        await ws.send_text(json.dumps({"type": "snapshot", "data": state.get_snapshot()}))
    except Exception:
        state.unsubscribe(q)
        return
    try:
        while True:
            try:
                event = q.get_nowait()
            except asyncio.QueueEmpty:
                await asyncio.sleep(0.1)
                continue
            await ws.send_text(json.dumps(event))
    except (WebSocketDisconnect, Exception):
        state.unsubscribe(q)


# ── Projects ──────────────────────────────────────────────────────────────────

class ProjectIn(BaseModel):
    folder: str
    name: str | None = None


@app.get("/api/projects")
async def list_projects():
    return list(state.get_projects().values())


@app.post("/api/projects")
async def add_project(body: ProjectIn):
    folder = Path(body.folder).expanduser().resolve()
    if not folder.exists():
        raise HTTPException(400, f"Folder not found: {folder}")
    proj = state.upsert_project(str(folder), body.name)
    loop = asyncio.get_event_loop()
    watcher.watch_project(proj["id"], proj["folder"], loop)
    asyncio.create_task(prompt_log.log("project_added", project=proj["name"], folder=str(folder)))
    return proj


# ── Tasks ─────────────────────────────────────────────────────────────────────

class TaskIn(BaseModel):
    project_id: str
    title: str
    description: str = ""
    priority: str = "medium"
    tags: list[str] = []


class TaskUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None
    title: str | None = None
    description: str | None = None


@app.get("/api/tasks")
async def list_tasks(project_id: str | None = None):
    return state.get_tasks(project_id)


@app.post("/api/tasks")
async def create_task_endpoint(body: TaskIn):
    projects = state.get_projects()
    if body.project_id not in projects:
        raise HTTPException(400, "Unknown project_id")
    task = state.create_task(
        project_id=body.project_id,
        title=body.title,
        description=body.description,
        priority=body.priority,
        tags=body.tags,
    )
    proj_name = projects[body.project_id]["name"]
    notes_path = notes.create_task_notes(
        project_name=proj_name,
        task_id=task["id"],
        task_title=task["title"],
        description=body.description,
        tags=body.tags,
    )
    state.update_task(task["id"], notes_path=notes_path)
    asyncio.create_task(prompt_log.log("task_created", task_id=task["id"],
        title=body.title, project=proj_name, priority=body.priority, tags=body.tags))
    tasks = state.get_tasks()
    return next((t for t in tasks if t["id"] == task["id"]), task)


@app.patch("/api/tasks/{task_id}")
async def update_task_endpoint(task_id: str, body: TaskUpdate):
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    task = state.update_task(task_id, **updates)
    if not task:
        raise HTTPException(404, "Task not found")
    if task.get("notes_path") and "status" in updates:
        notes.update_task_status_in_notes(task["notes_path"], updates["status"])
    return task


@app.delete("/api/tasks/{task_id}")
async def delete_task_endpoint(task_id: str):
    tasks = {t["id"]: t for t in state.get_tasks()}
    if task_id not in tasks:
        raise HTTPException(404, "Task not found")
    state.update_task(task_id, status="deleted")
    return {"ok": True}


# ── Loops ─────────────────────────────────────────────────────────────────────

class LoopIn(BaseModel):
    task_id: str
    goal: str
    max_iterations: int = 10


class LoopLogIn(BaseModel):
    message: str
    level: str = "info"
    action: str = ""
    result: str = ""
    next_step: str = ""


@app.get("/api/loops")
async def list_loops():
    return state.get_loops()


@app.post("/api/loops")
async def start_loop(body: LoopIn):
    loop = state.create_loop(body.task_id, body.goal, body.max_iterations)
    state.update_task(body.task_id, status="in_progress")
    asyncio.create_task(prompt_log.log("loop_started", loop_id=loop["id"],
        task_id=body.task_id, goal=body.goal, max_iterations=body.max_iterations))
    return loop


@app.post("/api/loops/{loop_id}/log")
async def add_loop_log(loop_id: str, body: LoopLogIn):
    loops = {l["id"]: l for l in state.get_loops()}
    if loop_id not in loops:
        raise HTTPException(404, "Loop not found")
    state.append_loop_log(loop_id, body.message, body.level)
    lp = loops[loop_id]
    tasks = {t["id"]: t for t in state.get_tasks()}
    task = tasks.get(lp["task_id"])
    if task and task.get("notes_path"):
        notes.append_loop_entry(
            notes_path=task["notes_path"],
            iteration=lp["iteration"] + 1,
            status=body.level,
            action=body.action or body.message,
            result=body.result,
            next_step=body.next_step,
        )
    return {"ok": True}


@app.post("/api/loops/{loop_id}/finish")
async def finish_loop_endpoint(loop_id: str, status: str = "done"):
    loops = {l["id"]: l for l in state.get_loops()}
    if loop_id not in loops:
        raise HTTPException(404, "Loop not found")
    state.finish_loop(loop_id, status)
    task_id = loops[loop_id]["task_id"]
    final = "done" if status == "done" else "failed"
    state.update_task(task_id, status=final)
    tasks = {t["id"]: t for t in state.get_tasks()}
    task = tasks.get(task_id)
    if task and task.get("notes_path"):
        notes.update_task_status_in_notes(task["notes_path"], final)
    return {"ok": True}


# ── Processes ─────────────────────────────────────────────────────────────────

@app.get("/api/processes")
async def list_processes():
    return state.get_processes()


@app.get("/api/snapshot")
async def snapshot():
    return state.get_snapshot()


# ── Settings ──────────────────────────────────────────────────────────────────

@app.get("/api/settings/global")
async def get_global_settings():
    return state.get_global_settings()


@app.patch("/api/settings/global")
async def patch_global_settings(body: dict):
    return state.update_global_settings(body)


@app.get("/api/settings/projects/{project_id:path}")
async def get_project_settings(project_id: str):
    return state.get_project_settings(project_id)


@app.patch("/api/settings/projects/{project_id:path}")
async def patch_project_settings(project_id: str, body: dict):
    if project_id not in state.get_projects():
        raise HTTPException(404, "Project not found")
    return state.update_project_settings(project_id, body)


# ── Brain Test / Validation ────────────────────────────────────────────────────

class BrainTestIn(BaseModel):
    brain: str          # claude | openai | gemini | grok | deepseek | ollama
    api_key: str = ""
    model: str = ""
    base_url: str = ""  # for ollama or custom endpoints


async def _test_claude(api_key: str, model: str, base_url: str) -> dict:
    key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    url = (base_url or os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")).rstrip("/")
    mdl = model or "claude-sonnet-4-6"
    if not key:
        return {"ok": False, "error": "No API key"}
    payload = {
        "model": mdl,
        "max_tokens": 64,
        "messages": [{"role": "user", "content": "Say: 'Hello from LoopEngineering! I am model: " + mdl + "'. Nothing else."}],
    }
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            f"{url}/v1/messages",
            headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json=payload,
        )
    if r.status_code != 200:
        return {"ok": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
    data = r.json()
    reply = data.get("content", [{}])[0].get("text", "")
    used_model = data.get("model", mdl)
    return {"ok": True, "reply": reply, "model": used_model}


async def _test_openai(api_key: str, model: str, base_url: str) -> dict:
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    url = (base_url or "https://api.openai.com").rstrip("/")
    mdl = model or "gpt-4o-mini"
    if not key:
        return {"ok": False, "error": "No API key"}
    payload = {
        "model": mdl,
        "max_tokens": 64,
        "messages": [{"role": "user", "content": f"Say exactly: 'Hello from LoopEngineering! I am model: {mdl}'. Nothing else."}],
    }
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            f"{url}/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=payload,
        )
    if r.status_code != 200:
        return {"ok": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
    data = r.json()
    reply = data["choices"][0]["message"]["content"]
    used_model = data.get("model", mdl)
    return {"ok": True, "reply": reply, "model": used_model}


async def _test_gemini(api_key: str, model: str, base_url: str) -> dict:
    key = api_key or os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))
    mdl = model or "gemini-2.0-flash"
    if not key:
        return {"ok": False, "error": "No API key"}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{mdl}:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": f"Say exactly: 'Hello from LoopEngineering! I am model: {mdl}'. Nothing else."}]}]}
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(url, headers={"Content-Type": "application/json"}, json=payload)
    if r.status_code != 200:
        return {"ok": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
    data = r.json()
    reply = data["candidates"][0]["content"]["parts"][0]["text"]
    return {"ok": True, "reply": reply, "model": mdl}


async def _test_grok(api_key: str, model: str, base_url: str) -> dict:
    key = api_key or os.environ.get("XAI_API_KEY", os.environ.get("GROK_API_KEY", ""))
    url = (base_url or "https://api.x.ai").rstrip("/")
    mdl = model or "grok-3"
    if not key:
        return {"ok": False, "error": "No API key"}
    payload = {
        "model": mdl,
        "max_tokens": 64,
        "messages": [{"role": "user", "content": f"Say exactly: 'Hello from LoopEngineering! I am model: {mdl}'. Nothing else."}],
    }
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            f"{url}/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=payload,
        )
    if r.status_code != 200:
        return {"ok": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
    data = r.json()
    reply = data["choices"][0]["message"]["content"]
    used_model = data.get("model", mdl)
    return {"ok": True, "reply": reply, "model": used_model}


async def _test_deepseek(api_key: str, model: str, base_url: str) -> dict:
    key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
    url = (base_url or "https://api.deepseek.com").rstrip("/")
    mdl = model or "deepseek-chat"
    if not key:
        return {"ok": False, "error": "No API key"}
    payload = {
        "model": mdl,
        "max_tokens": 64,
        "messages": [{"role": "user", "content": f"Say exactly: 'Hello from LoopEngineering! I am model: {mdl}'. Nothing else."}],
    }
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            f"{url}/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=payload,
        )
    if r.status_code != 200:
        return {"ok": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
    data = r.json()
    reply = data["choices"][0]["message"]["content"]
    used_model = data.get("model", mdl)
    return {"ok": True, "reply": reply, "model": used_model}


async def _test_ollama(api_key: str, model: str, base_url: str) -> dict:
    url = (base_url or "http://localhost:11434").rstrip("/")
    mdl = model or "llama3.2"
    payload = {
        "model": mdl,
        "messages": [{"role": "user", "content": f"Say exactly: 'Hello from LoopEngineering! I am model: {mdl}'. Nothing else."}],
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{url}/api/chat", json=payload)
    if r.status_code != 200:
        return {"ok": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
    data = r.json()
    reply = data.get("message", {}).get("content", "")
    return {"ok": True, "reply": reply, "model": mdl}


_BRAIN_TESTERS = {
    "claude": _test_claude,
    "openai": _test_openai,
    "gemini": _test_gemini,
    "grok": _test_grok,
    "deepseek": _test_deepseek,
    "ollama": _test_ollama,
}


@app.post("/api/brains/test")
async def test_brain(body: BrainTestIn):
    tester = _BRAIN_TESTERS.get(body.brain)
    if not tester:
        raise HTTPException(400, f"Unknown brain: {body.brain}")
    try:
        result = await tester(body.api_key, body.model, body.base_url)
    except httpx.ConnectError as e:
        result = {"ok": False, "error": f"Connection failed: {str(e)[:150]}"}
    except httpx.TimeoutException:
        result = {"ok": False, "error": "Request timed out (15s)"}
    except Exception as e:
        result = {"ok": False, "error": str(e)[:200]}
    asyncio.create_task(prompt_log.log("brain_test", brain=body.brain,
        model=body.model or "(default)", ok=result.get("ok"), error=result.get("error"),
        replied_model=result.get("model")))
    return result


@app.get("/api/mcp/servers")
async def list_mcp_servers():
    """Scan all Claude config files and return MCP servers grouped by source."""
    home = Path.home()
    cursor_root = Path("/Users/sthanna/Downloads/Cursor")

    sources = [
        ("global: ~/.claude.json",        home / ".claude.json"),
        ("global: ~/.claude/settings.json", home / ".claude" / "settings.json"),
    ]
    # Add local project settings
    for child in sorted(cursor_root.iterdir()):
        sf = child / ".claude" / "settings.json"
        if sf.exists():
            sources.append((f"local: {child.name}", sf))

    health_cache: dict = {}
    hf = home / ".claude" / "mcp-health-cache.json"
    if hf.exists():
        try:
            health_cache = json.loads(hf.read_text()).get("servers", {})
        except Exception:
            pass

    result = []
    seen: set[str] = set()

    for source_label, path in sources:
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text())
        except Exception:
            continue
        mcps = data.get("mcpServers", {})
        for name, cfg in mcps.items():
            h = health_cache.get(name, {})
            entry = {
                "name": name,
                "source": source_label,
                "source_file": str(path),
                "type": cfg.get("type", "stdio"),
                "command": cfg.get("command", cfg.get("url", "")),
                "args": cfg.get("args", []),
                "status": h.get("status", "unknown"),
                "checked_at": h.get("checkedAt"),
                "failure_count": h.get("failureCount", 0),
                "last_error": h.get("lastError"),
                "duplicate": name in seen,
            }
            seen.add(name)
            result.append(entry)

    return result


class MCPToggleIn(BaseModel):
    name: str
    source_file: str
    enabled: bool


@app.patch("/api/mcp/toggle")
async def toggle_mcp_server(body: MCPToggleIn):
    src = Path(body.source_file)
    if not src.exists():
        raise HTTPException(404, f"Config file not found: {src}")
    try:
        data = json.loads(src.read_text())
    except Exception as e:
        raise HTTPException(500, f"Failed to read config: {e}")
    mcps = data.get("mcpServers", {})
    if body.name not in mcps:
        raise HTTPException(404, f"MCP server '{body.name}' not in {src}")
    if body.enabled:
        mcps[body.name].pop("disabled", None)
        action = "enable"
    else:
        mcps[body.name]["disabled"] = True
        action = "disable"
    # Atomic write via temp file
    tmp = src.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(src)
    asyncio.create_task(prompt_log.log("mcp_toggle", server=body.name,
        action=action, source=str(src)))
    return {"ok": True, "name": body.name, "enabled": body.enabled}


@app.get("/api/logs")
async def get_prompt_logs(days: int = 3):
    from src.prompt_log import read_logs
    return read_logs(days=days)


@app.get("/api/brains/claude-config")
async def get_claude_config():
    """Return safe (non-secret) Claude Code config from ~/.claude.json"""
    home = Path.home()
    cfg_file = home / ".claude.json"
    if not cfg_file.exists():
        return {}
    try:
        raw = json.loads(cfg_file.read_text())
    except Exception:
        return {}
    # Strip secrets, return only safe fields
    SAFE = {"theme", "numStartups", "installMethod", "autoUpdates",
            "hasCompletedOnboarding", "defaultPermissionMode", "claudeCodeVersion"}
    safe = {k: v for k, v in raw.items() if k in SAFE}
    # Add env-based config (no secrets)
    safe["anthropic_base_url"] = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    safe["has_anthropic_key_in_env"] = bool(os.environ.get("ANTHROPIC_API_KEY", ""))
    return safe


# ── Logs / Prompt Capture ─────────────────────────────────────────────────────

class PromptIn(BaseModel):
    text: str
    source: str = "user"   # user | claude | cursor | other


@app.post("/api/logs/prompt")
async def log_prompt(body: PromptIn):
    await prompt_log.log("user_prompt", source=body.source, text=body.text)
    return {"ok": True}


@app.get("/api/logs")
async def get_logs(days: int = 3):
    return prompt_log.read_logs(days)


@app.post("/api/projects/scan")
async def scan_projects(root: str = str(CURSOR_ROOT)):
    root_path = Path(root).expanduser().resolve()
    if not root_path.exists():
        raise HTTPException(400, f"Path not found: {root_path}")
    added = []
    for child in sorted(root_path.iterdir()):
        if child.is_dir() and not child.name.startswith("."):
            proj = state.upsert_project(str(child))
            added.append(proj)
    return {"added": len(added), "projects": added}


# ── Salesforce Ecosystem ───────────────────────────────────────────────────────

@app.get("/api/sf/ecosystem")
async def get_sf_ecosystem():
    clouds = sf_ecosystem.get_all_clouds()
    result = {}
    for cloud_id, cloud in clouds.items():
        result[cloud_id] = {
            **cloud,
            "brain": sf_ecosystem.get_brain_for_cloud(cloud_id),
            "task_count": len([t for t in state.get_tasks()
                               if cloud["folder"] in (t.get("tags") or [])]),
        }
    return result


# ── Web Intelligence ───────────────────────────────────────────────────────────

class WebIntelSearchIn(BaseModel):
    query: str
    sources: list[str] = ["github", "reddit", "hackernews", "devto"]
    limit: int = 8


@app.post("/api/web-intel/search")
async def web_intel_search(body: WebIntelSearchIn):
    if not body.query.strip():
        raise HTTPException(400, "query required")
    results = await web_intel.multi_search(body.query, body.sources, body.limit)
    await prompt_log.log("web_intel_search", query=body.query, sources=body.sources,
                         counts={k: len(v) for k, v in results.items()})
    return results
