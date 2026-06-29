# LoopEngineering — Architecture

*Last updated: 2026-06-29*

---

## System Overview

LoopEngineering is a local-first AI task and loop monitoring platform. FastAPI backend with REST + WebSocket APIs, vanilla-JS dashboard. All state persisted to `data/state.json`.

```
Browser (index.html)
    │   WebSocket ws://localhost:7070/ws     (real-time push)
    │   REST  http://localhost:7070/api/*    (read/write)
    ▼
FastAPI (server.py)  :7070
    ├── State Store     (src/state.py)          ← in-memory + data/state.json
    ├── Process Monitor (src/monitor.py)         ← psutil scan every 5s
    ├── FS Watcher      (src/watcher.py)         ← watchdog per project
    ├── Notes Generator (src/notes.py)           ← markdown per task
    ├── Prompt Logger   (src/prompt_log.py)      ← JSONL audit trail
    └── MCP Scanner     (server.py)              ← reads ~/.claude* + local settings
```

---

## Component Map

### `server.py` — FastAPI Entrypoint
- All REST routes registered here
- `lifespan()`: seeds projects, starts watcher + monitor loop on startup
- `_seed_projects()`: auto-imports `/Users/sthanna/Downloads/Cursor/*`
- WebSocket `/ws`: broadcasts state events to all connected clients
- Brain testers: `_test_claude`, `_test_openai`, `_test_gemini`, `_test_grok`, `_test_deepseek`, `_test_ollama`
- MCP scanner: reads `~/.claude.json`, `~/.claude/settings.json`, local `.claude/settings.json`
- MCP toggle: writes `disabled: true` flag into source config file (atomic)

### `src/state.py` — Central State Store
- Single `_state` dict: `{projects, tasks, loops, processes, settings}`
- Written to `data/state.json` on every mutation (excludes ephemeral `processes`)
- Pub/sub via `asyncio.Queue` per connected WebSocket client
- Settings: `DEFAULT_GLOBAL_SETTINGS` + `DEFAULT_PROJECT_SETTINGS`, deep-merged per project
- `_deep_merge()` for nested patch updates

### `src/monitor.py` — AI Process Scanner
- `psutil.process_iter()` every 5s in background task
- Classifies by name/cmdline: Claude, Claude Code, Cursor, Copilot, Continue, Ollama, LM Studio, Aider, Cody
- Deduplicates by label (keeps highest-memory instance)
- Pushes `processes_updated` event via `state.set_processes()`

### `src/watcher.py` — Filesystem Watcher
- `watchdog` Observer per registered project folder
- Emits `fs_event` (modified/created/deleted/moved) to dashboard
- Thread-safe via `asyncio.run_coroutine_threadsafe`

### `src/notes.py` — Notes Generator
- Creates `notes/<project-slug>/<date>-<task-slug>/` on task creation
- Files: `index.md`, `plan.md`, `design.md`, `architecture.md`, `loop-log.md`
- `append_loop_entry()`: appends iteration rows to `loop-log.md`
- `update_task_status_in_notes()`: updates status header in `index.md`

### `src/prompt_log.py` — Prompt / Interaction Logger
- Appends JSONL entries to `logs/prompts-YYYY-MM-DD.jsonl`
- Logs: task_created, loop_started, loop_log, loop_finished, brain_test, mcp_toggle, settings_updated
- Thread-safe: uses `asyncio.Lock` for file writes
- Daily rotation: new file per day, never truncated

### `dashboard/index.html` — Single-File Frontend
- Vanilla JS, zero framework, zero build step — open in any browser
- State `S`: projects, tasks, loops, processes, settings, mcpServers, fsEvents
- WebSocket for real-time push + 3s HTTP poll (`pollSnapshot`) as fallback
- Views: overview, processes, tasks, loops, activity, roadmap, settings, mcp, console
- Theme: dark/light toggle, persists `localStorage`
- Console log capture: wraps `console.log/warn/error/info`

---

## Data Flow

```
User action (UI click / form submit)
    │
    ▼
api() fetch → POST /api/tasks
    │
    ▼
server.py handler
    ├── state.create_task()
    │       ├── write data/state.json
    │       └── _broadcast({type: "task_created"})
    │                   └── asyncio.Queue → ws.send_text()
    ├── notes.create_task_notes()   → notes/<slug>/
    └── prompt_log.log()            → logs/prompts-<date>.jsonl
    │
    ▼
HTTP 200 response JSON
    │
    ▼
upsert(S.tasks, t) → render()
```

---

## Storage Layout

```
data/
  state.json              — projects, tasks, loops, settings (no secrets logged)

notes/
  <project-slug>/
    <date>-<task-slug>/
      index.md            — task metadata + status
      plan.md             — task plan
      design.md           — design decisions
      architecture.md     — technical approach
      loop-log.md         — iteration history

logs/
  prompts-YYYY-MM-DD.jsonl — all interactions, JSONL, append-only, daily rotation

tmp/                       — scratch: experiments, test scripts, one-off work
```

---

## API Surface

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/projects` | List all projects |
| POST | `/api/projects` | Add project by folder path |
| POST | `/api/projects/scan` | Scan Cursor root, import all subdirs |
| GET | `/api/tasks` | List tasks (`?project_id=` optional) |
| POST | `/api/tasks` | Create task + notes |
| PATCH | `/api/tasks/:id` | Update task fields |
| DELETE | `/api/tasks/:id` | Soft-delete task |
| GET | `/api/loops` | List loops |
| POST | `/api/loops` | Start loop |
| POST | `/api/loops/:id/log` | Append iteration |
| POST | `/api/loops/:id/finish` | Finish loop |
| GET | `/api/processes` | Live AI processes |
| GET | `/api/snapshot` | Full state snapshot |
| GET | `/api/settings/global` | Global settings |
| PATCH | `/api/settings/global` | Update global settings |
| GET | `/api/settings/projects/:id` | Per-project settings |
| PATCH | `/api/settings/projects/:id` | Update per-project settings |
| GET | `/api/mcp/servers` | All MCP servers (global + local) |
| PATCH | `/api/mcp/toggle` | Enable/disable MCP server in config |
| POST | `/api/brains/test` | Test AI brain connectivity |
| GET | `/api/brains/claude-config` | Import Claude Code local config |
| WS | `/ws` | Real-time event stream |

---

## WebSocket Events

| Event | Trigger |
|-------|---------|
| `snapshot` | WS connect |
| `project_updated` | Project added/edited |
| `task_created` | Task created |
| `task_updated` | Task updated |
| `loop_created` | Loop started |
| `loop_log` | Iteration logged |
| `loop_finished` | Loop done/failed |
| `processes_updated` | Every 5s scan |
| `fs_event` | File change in watched folder |
| `settings_updated` | Settings changed |

---

## Security Notes

- Binds `127.0.0.1:7070` only — not network-exposed
- `GET /api/brains/claude-config` returns only safe (non-secret) fields
- `GET /api/mcp/servers` strips `env` blocks (may contain tokens)
- `data/state.json` is local only — no remote sync
- No authentication — single-user local tool
