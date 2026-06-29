# PRD-07 — Future Scope / Intelligence Layer

*Status: Future | Last updated: 2026-06-29*

## Goal
Long-range intelligence features: cross-brain vector memory, cost dashboards, loop replay, self-healing loops, and agent eval harnesses. See [docs/FUTURE_SCOPE.md](../docs/FUTURE_SCOPE.md) for full narrative.

## Tasks & Subtasks

### 🔲 T1 — Cross-Brain Vector Memory
- [ ] T1.1 ChromaDB or Qdrant local instance (Docker Compose)
- [ ] T1.2 Embed all loop logs, task descriptions on creation
- [ ] T1.3 Similarity search: "Find tasks similar to this goal"
- [ ] T1.4 Memory browser in dashboard: search + source tasks
- [ ] T1.5 Shared across all brains via MCP tool `search_memory`

### 🔲 T2 — Cost & Token Dashboard
- [ ] T2.1 Track tokens in/out per brain per API call
- [ ] T2.2 Store in `data/cost_log.jsonl`
- [ ] T2.3 Dashboard widget: spend by brain, by project, by day
- [ ] T2.4 Budget caps: per-project daily limit (settings)
- [ ] T2.5 Alert at 80% cap: toast + critical task auto-created

### 🔲 T3 — Loop Replay & Diff
- [ ] T3.1 Snapshot loop state at each iteration: `data/loop_snapshots/<id>-<iter>.json`
- [ ] T3.2 `GET /api/loops/:id/snapshot` — fetch snapshot
- [ ] T3.3 Side-by-side diff view: compare two loop runs
- [ ] T3.4 Auto-flag regression: if quality score drops vs previous run
- [ ] T3.5 Export diff as markdown to task notes

### 🔲 T4 — Agent Eval Harness
- [ ] T4.1 Define benchmark task set (JSON fixtures)
- [ ] T4.2 Run same task against all enabled brains in parallel
- [ ] T4.3 Score: accuracy (human/LLM judge), speed (ms), cost (tokens), completeness
- [ ] T4.4 Ranking table in dashboard
- [ ] T4.5 Scheduled nightly evals, trend chart over time

### 🔲 T5 — Self-Healing Loops
- [ ] T5.1 Detect stuck loop: no log entry for N seconds (configurable, default 120s)
- [ ] T5.2 Auto-restart: increase max_iterations, switch to fallback brain
- [ ] T5.3 Failure analysis: send error context to brain, get suggested fix
- [ ] T5.4 Circuit breaker: if loop fails 3x -> pause + alert + create task
- [ ] T5.5 Healing log: record all auto-interventions

### 🔲 T6 — Advanced Orchestration
- [ ] T6.1 Tournament brackets: N agent approaches -> judge panel -> winner
- [ ] T6.2 Staged escalation: cheap model first, escalate to expensive on failure
- [ ] T6.3 Completeness critic: "What's missing?" agent after every loop
- [ ] T6.4 Loop-until-dry: keep running until K consecutive rounds find nothing new

## Dependencies
- PRD-02 (Multi-Brain)
- PRD-03 (Agents)
- ChromaDB or Qdrant running locally
