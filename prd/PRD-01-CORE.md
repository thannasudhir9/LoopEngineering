# PRD-01 — Core Platform

*Status: v0.1 Done | Last updated: 2026-06-29*

## Goal
Single local dashboard to monitor all AI processes, track tasks across projects, run loops, auto-generate notes, and watch filesystem changes in real time.

## User Stories
- As a developer, I want to see all running AI tools (Claude, Cursor, Ollama) so I know what's active
- As a developer, I want to create tasks per project and track status
- As a developer, I want to attach a loop to a task and log each iteration
- As a developer, I want auto-generated notes for every task I create
- As a developer, I want to see live file changes in my watched projects

## Tasks & Subtasks

### ✅ T1 — FastAPI Server
- [x] T1.1 REST endpoints: projects, tasks, loops, processes, snapshot
- [x] T1.2 WebSocket `/ws` with pub/sub queue per client
- [x] T1.3 `lifespan()` startup: seed projects, start monitor + watcher
- [x] T1.4 Static file serving for dashboard

### ✅ T2 — State Store
- [x] T2.1 In-memory `_state` dict with `projects`, `tasks`, `loops`
- [x] T2.2 Persist to `data/state.json` on every mutation
- [x] T2.3 `_broadcast()` to all connected WebSocket queues
- [x] T2.4 Settings: global + per-project with deep merge

### ✅ T3 — AI Process Monitor
- [x] T3.1 `psutil.process_iter()` every 5s
- [x] T3.2 Classify: Claude, Claude Code, Cursor, Copilot, Ollama, Aider, Cody, Continue, LM Studio
- [x] T3.3 Deduplicate by label (highest-memory wins)
- [x] T3.4 Push `processes_updated` event

### ✅ T4 — Filesystem Watcher
- [x] T4.1 `watchdog` Observer per registered project
- [x] T4.2 Emit `fs_event` on modified/created/deleted/moved
- [x] T4.3 Thread-safe via `asyncio.run_coroutine_threadsafe`

### ✅ T5 — Notes Generator
- [x] T5.1 Create `notes/<project>/<date>-<task>/` on task creation
- [x] T5.2 Generate `index.md`, `plan.md`, `design.md`, `architecture.md`, `loop-log.md`
- [x] T5.3 `append_loop_entry()` for iteration rows
- [x] T5.4 `update_task_status_in_notes()` on status change

### ✅ T6 — Dashboard
- [x] T6.1 Views: overview, processes, tasks, loops, activity
- [x] T6.2 WebSocket real-time + 3s HTTP poll fallback
- [x] T6.3 Dark/light theme toggle (localStorage)
- [x] T6.4 Modals: add project, add task, start loop
- [x] T6.5 Toast notifications

### ✅ T7 — Project Auto-Seed
- [x] T7.1 Scan `/Users/sthanna/Downloads/Cursor` on startup
- [x] T7.2 `POST /api/projects/scan` for manual rescan
- [x] T7.3 19 projects loaded on first run

### ✅ T8 — Prompt Logging
- [x] T8.1 `src/prompt_log.py` JSONL logger
- [x] T8.2 Daily rotation: `logs/prompts-YYYY-MM-DD.jsonl`
- [x] T8.3 Log: task_created, loop_started, brain_test, mcp_toggle, project_added
- [x] T8.4 `GET /api/logs` endpoint

## Open Items
- [ ] T9 — Prompt log viewer in dashboard UI
- [ ] T10 — Task due dates
- [ ] T11 — Loop log search/filter
- [ ] T12 — Export tasks to CSV/markdown

## Acceptance Criteria
- Server starts cleanly with `uvicorn server:app --port 7070`
- Dashboard loads at `http://localhost:7070`
- Projects auto-populated from Cursor folder
- Creating a task generates notes folder
- Loop iterations visible in real time
