# LoopEngineering

Monitor all AI tasks (Claude, Claude Code, Cursor, Ollama, etc.) running on your machine.
Loop until issues are fixed. Auto-generate structured notes per task. One dashboard for all projects.

## What It Does

| Feature | Detail |
|---------|--------|
| AI Process Monitor | Scans for Claude, Claude Code, Cursor, Ollama, Aider, Copilot every 5s |
| Task Tracker | Create tasks for any project/folder with priority, tags, status |
| Loop Engine | Attach a loop to any task — track iterations, log progress, mark done/failed |
| Notes Generator | Auto-creates plan.md, design.md, architecture.md, loop-log.md per task |
| Filesystem Watcher | Watches registered project folders for live file changes |
| Live Dashboard | WebSocket-powered web UI — updates without refresh |

## Setup

```bash
cd /Users/sthanna/Downloads/Cursor/LoopEngineering

pip install -r requirements.txt

uvicorn server:app --reload --port 7070

open http://localhost:7070
```

## File Structure

```
LoopEngineering/
├── server.py              # FastAPI server — REST + WebSocket
├── requirements.txt
├── RESEARCH.md            # Loop Engineering research & reference links
├── src/
│   ├── state.py           # Central in-memory store + persistence
│   ├── monitor.py         # AI process scanner (psutil)
│   ├── watcher.py         # Filesystem watcher (watchdog)
│   └── notes.py           # Notes generator
├── dashboard/
│   └── index.html         # Full dashboard (vanilla JS, zero framework)
├── data/
│   └── state.json         # Persisted projects/tasks/loops
└── notes/
    └── <project>/<date>-<task>/
        ├── index.md
        ├── plan.md
        ├── design.md
        ├── architecture.md
        └── loop-log.md
```

## API

### Projects
- `GET  /api/projects`
- `POST /api/projects` — `{folder, name?}`

### Tasks
- `GET  /api/tasks?project_id=`
- `POST /api/tasks` — `{project_id, title, description, priority, tags}` — creates task + notes
- `PATCH /api/tasks/:id` — `{status?, priority?, title?, description?}`
- `DELETE /api/tasks/:id`

### Loops
- `GET  /api/loops`
- `POST /api/loops` — `{task_id, goal, max_iterations}`
- `POST /api/loops/:id/log` — `{message, level, action, result, next_step}`
- `POST /api/loops/:id/finish?status=done|failed`

### Processes
- `GET /api/processes`

### WebSocket: `ws://localhost:7070/ws`

Events: `snapshot`, `task_created`, `task_updated`, `loop_created`, `loop_log`, `loop_finished`, `processes_updated`, `fs_event`

## Posting Loop Updates from Claude Code / Cursor

```bash
# Start loop
curl -X POST http://localhost:7070/api/loops \
  -H 'Content-Type: application/json' \
  -d '{"task_id":"<id>","goal":"All tests pass","max_iterations":10}'

# Log iteration
curl -X POST http://localhost:7070/api/loops/<id>/log \
  -H 'Content-Type: application/json' \
  -d '{"message":"Ran tests","action":"pytest","result":"3 failures","next_step":"fix auth middleware"}'

# Finish
curl -X POST "http://localhost:7070/api/loops/<id>/finish?status=done"
```

## References

See [RESEARCH.md](RESEARCH.md) for all Loop Engineering research, sources, and concepts.
