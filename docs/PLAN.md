# LoopEngineering — Plan

*Last updated: 2026-06-29*

---

## Current State — v0.1 (2026-06-29)

### Completed ✓

- [x] FastAPI server with REST + WebSocket
- [x] Auto-seed 19 projects from `/Users/sthanna/Downloads/Cursor`
- [x] Task CRUD with priority, tags, soft-delete
- [x] Loop engine (start, log iterations, finish)
- [x] Auto-generated notes per task (index, plan, design, architecture, loop-log)
- [x] AI Process Monitor (Claude, Cursor, Ollama, Aider, Copilot, etc.) every 5s
- [x] Filesystem watcher per project (live file change events)
- [x] Dashboard: overview, tasks, loops, activity, roadmap views
- [x] Light / dark theme toggle (persists localStorage)
- [x] 3s auto-refresh poll + WebSocket real-time
- [x] Settings: global controls + per-project overrides
- [x] AI Brain config (Claude, OpenAI, Gemini, Grok, DeepSeek, Ollama)
- [x] Brain Test — validates API key with "Hello, what is your model?"
- [x] Integration config (GitHub, Slack, Jira, Linear, Notion, Discord)
- [x] MCP view — 20 servers, global + local, health status, grouped
- [x] MCP enable/disable toggle per server
- [x] Console view — browser log capture
- [x] Roadmap view — 4-phase future scope
- [x] Prompt logging to `logs/prompts-YYYY-MM-DD.jsonl`
- [x] `tmp/` scratch folder
- [x] `ARCHITECTURE.md`, `DESIGN.md`, `PLAN.md`, `FUTURE_SCOPE.md`
- [x] Claude Code config import (theme, base URL, install method)

---

## Active Sprint — v0.2

### P1 — Must Have

- [ ] **Prompt log viewer in dashboard** — view `logs/prompts-*.jsonl` in UI
- [ ] **Task due dates** — `due_date` field; overdue highlighted red
- [ ] **Project scan root configurable** — make scan root editable in Settings
- [ ] **Brain fallback chain UI** — configure `claude → openai → ollama` per project
- [ ] **Loop log search/filter** — keyword filter on loop entries

### P2 — Should Have

- [ ] **Export tasks** — download as CSV or markdown
- [ ] **Keyboard shortcuts** — `n` new task, `/` search, `g` go to project
- [ ] **Global search** — search across tasks, projects, loop logs
- [ ] **Task comments** — free-form thread per task
- [ ] **Loop templates** — save reusable loop goals

### P3 — Nice to Have

- [ ] **Task dependencies** — block task B until A is done
- [ ] **Bulk task operations** — select + batch status update
- [ ] **Activity timeline** — unified chronological event feed

---

## v0.3 — Agents (Phase 1)

- [ ] Agent registry (name, type, capabilities, health)
- [ ] Sub-agent trees (parent/child hierarchy, collapsible UI)
- [ ] Agent orchestrator (route tasks by type + load)
- [ ] Inter-agent messaging bus

*See [FUTURE_SCOPE.md](FUTURE_SCOPE.md) Phase 1 for full detail.*

---

## v0.4 — Multi-Brain (Phase 2)

- [ ] Live brain router (route by priority + cost estimate)
- [ ] Streaming responses to loop log
- [ ] Unified MCP context across brains

---

## v0.5 — Integrations (Phase 3)

- [ ] GitHub issue sync
- [ ] Slack notifications
- [ ] Jira/Linear bidirectional sync

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `data/state.json` grows large | Medium | Medium | Archive after 1000 tasks |
| API key exposure | Low | High | Future: encrypt at rest |
| MCP file write conflict | Low | Medium | Atomic write + file lock |
| WebSocket reconnect storm | Low | Medium | Fixed 3s backoff already in place |

---

## Definition of Done

- Feature has API endpoint (if backend change)
- Renders correctly in dark + light theme
- Console logs include `[Category]` prefix
- `ARCHITECTURE.md`, `DESIGN.md`, `PLAN.md` updated
- Prompt log entry emitted for user-visible actions
