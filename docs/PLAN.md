# LoopEngineering — Plan

*Last updated: 2026-06-29 (session 2)*

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
- [x] MCP view — 20+ servers, global + local, health status, grouped
- [x] MCP enable/disable toggle per server
- [x] Console view — browser log capture
- [x] Roadmap view — 4-phase future scope
- [x] Prompt logging to `logs/prompts-YYYY-MM-DD.jsonl`
- [x] `POST /api/logs/prompt` — raw user prompt capture endpoint
- [x] `tmp/` scratch folder
- [x] `docs/` folder — ARCHITECTURE, DESIGN, PLAN, FUTURE_SCOPE, RESEARCH
- [x] `prd/` folder — 8 PRD files (core, AI, agents, integrations, SF, a11y, future)
- [x] Claude Code config import (theme, base URL, install method)
- [x] Git repo initialized, pushed to github.com/thannasudhir9/LoopEngineering
- [x] Session prompt log: `logs/SESSION-2026-06-29-prompts.md` (21 prompts)

### Added in Session 2 (2026-06-29)

- [x] `src/sf_ecosystem.py` — 12 Salesforce cloud registry + brain mapping
- [x] `src/web_intel.py` — GitHub, Reddit, HN, Dev.to parallel search
- [x] `GET /api/sf/ecosystem` — Salesforce ecosystem endpoint
- [x] `POST /api/web-intel/search` — multi-source web intelligence search
- [x] `salesforce-ecosystem/` folder — 12 SF cloud project directories inside LoopEngineering
- [x] PRD files: PRD-00 through PRD-07 (8 files)

---

## Active Sprint — v0.2

### P1 — Must Have

- [ ] Dashboard UI redesign — shadcn-inspired CSS, better typography, card layouts
- [ ] Analytics view — task creation rate, loop success %, brain usage, process uptime
- [ ] Performance tracking — API latency per endpoint, render time
- [ ] Show/hide projects sidebar button
- [ ] Salesforce ecosystem view — 12-cloud grid with brain mapping, task counts
- [ ] Web Intel view — search GitHub/Reddit/HN/Dev.to from dashboard
- [ ] Prompt log viewer in UI
- [ ] Task due dates

### P2 — Should Have

- [ ] Brain fallback chain UI
- [ ] Loop log search/filter
- [ ] Export tasks as CSV or markdown
- [ ] Keyboard shortcuts (n, /, ?)
- [ ] Global search across tasks + logs

### P3 — Nice to Have

- [ ] Task dependencies
- [ ] Bulk task operations
- [ ] Activity timeline
- [ ] Loop templates

---

## v0.3 — Salesforce Deep Integration

- [ ] Agentforce agents list from MCP tool
- [ ] Create task from Agentforce agent spec
- [ ] Revenue Cloud quote-to-cash loop tracking
- [ ] Apex log analysis auto-tasks
- [ ] Org health check dashboard widget

See prd/PRD-05-SALESFORCE.md

---

## v0.4 — Agents & Multi-Brain

- [ ] Agent registry + sub-agent trees
- [ ] Agent orchestrator
- [ ] Live brain router with streaming

See prd/PRD-02-AI-FEATURES.md, prd/PRD-03-AGENTS.md

---

## v0.5 — Integrations

- [ ] GitHub issue sync
- [ ] Slack notifications
- [ ] Jira/Linear bidirectional sync

See prd/PRD-04-INTEGRATIONS.md

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `data/state.json` grows large | Medium | Medium | Archive after 1000 tasks |
| API key exposure | Low | High | Future: encrypt at rest |
| MCP file write conflict | Low | Medium | Atomic write already in place |
| WebSocket reconnect storm | Low | Medium | Fixed 3s backoff in place |
| GitHub API rate limit (60/hr anon) | Medium | Low | Cache responses, add token in settings |
| Reddit API changes | Medium | Low | Fallback to HN + Dev.to |

---

## Definition of Done

- Feature has API endpoint (if backend change)
- Renders correctly in dark + light theme
- Console logs include [Category] prefix
- ARCHITECTURE.md, DESIGN.md, PLAN.md updated
- Prompt log entry emitted for user-visible actions
- PRD task checkbox ticked
