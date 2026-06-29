# LoopEngineering — Future Scope

*Last updated: 2026-06-29 (session 2)*

---

## Phase 1 — Agents & Sub-Agents (v0.3)

Build a registry of named AI agents (Claude Code, Cursor, Aider, etc.) with roles and capabilities. Spawn sub-agent trees from tasks. Orchestrate routing, delegation, and messaging.

| Feature | Detail |
|---------|--------|
| Agent Registry | Register agents with name, type, model, capabilities, health |
| Sub-Agent Trees | Spawn child agents; visualize hierarchy; depth limit 5 |
| Orchestrator | Route tasks by type + load; fallback chain on failure |
| Messaging Bus | Pub/sub between agents; durable queue; trace timeline |
| Loop Delegation | Agents create/monitor loops for other agents |

---

## Phase 2 — Multi-Brain AI (v0.4)

Connect Claude, OpenAI, Gemini, Grok, DeepSeek, Ollama. Route tasks by cost + quality. Stream responses. Auto-decompose goals into subtasks.

| Feature | Detail |
|---------|--------|
| Brain Router | Per-task selector; fallback chain; cost estimate before dispatch |
| Streaming SSE | Token-by-token stream into loop log; abort button |
| Task Decomposition | Brain breaks goal into subtasks; subtask tree in UI |
| Multi-Model Compare | Same task to N brains; side-by-side; thumbs up/down scoring |
| Unified MCP Context | All LoopEngineering tools exposed as MCP; shared memory |

---

## Phase 3 — Integrations (v0.5)

GitHub, Slack, Jira, Linear, Notion, Webhooks, Calendar, Email.

| Integration | Key Capability |
|-------------|---------------|
| GitHub | Task → Issue; loop log → PR comment; status sync |
| Slack/Discord | Notify on loop finish/fail; slash commands |
| Jira/Linear | Pull sprint backlog in; push loop results as comments |
| Notion/Obsidian | Export notes to pages; import DB rows as tasks |
| Webhooks | HMAC-signed ingress; 5-min replay window; dead-letter queue |
| Calendar | Task due date → calendar event; loops as time-blocks |

---

## Phase 4 — Salesforce Deep Integration (v0.3+)

Full Salesforce ecosystem tooling built directly into LoopEngineering.

| Feature | Cloud | Detail |
|---------|-------|--------|
| Agentforce Agent List | Agentforce | List agents via MCP; create tasks from agent spec |
| Agent Test Runs | Agentforce | Trigger test suite; log results as loop iterations |
| Quote-to-Cash Loops | Revenue Cloud | Track pricing → order → billing as loop steps |
| Billing Monitor | Revenue Cloud | Alert on failed invoice runs → critical task |
| Apex Log Analysis | All | Fetch debug logs; run RCA; surface findings as tasks |
| Org Readiness | Agentforce | Scheduled daily check; deployment via tracked loop |
| Data Cloud Monitor | Data Cloud | Ingestion job status; profile completeness metrics |
| Multi-Cloud Widget | All | Overview panel: org health per cloud |

---

## Phase 5 — Intelligence Layer (v0.5+)

Cross-brain memory, cost tracking, loop replay, self-healing, eval harness.

| Feature | Detail |
|---------|--------|
| Vector Memory | ChromaDB/Qdrant; embed all logs + tasks; similarity search |
| Cost Dashboard | Per-brain token spend; budget caps; alert at 80% |
| Loop Replay | Snapshot per iteration; side-by-side diff; regression flag |
| Agent Eval Harness | Benchmark tasks; multi-brain scoring; nightly evals |
| Self-Healing Loops | Detect stuck loops; auto-restart; circuit breaker after 3 fails |
| Advanced Orchestration | Tournament brackets; staged escalation; completeness critic |

---

## Phase 6 — Web Intelligence Expansion

Beyond GitHub/Reddit/HN/Dev.to — richer signal sources.

| Source | Method | Use Case |
|--------|--------|----------|
| YouTube | Data API v3 (key needed) | Salesforce tutorial trends, conference talks |
| LinkedIn | No public API — use MCP browser tool | Job posts, announcements |
| X / Twitter | API v2 (bearer token) | Real-time SF community signals |
| Instagram | Graph API (token needed) | Salesforce event coverage |
| Salesforce Blog | RSS feed parse | Official release notes |
| Trailhead | Web scrape via MCP browser | New trails, modules by topic |
| AppExchange | Scrape listings | Popular apps by category |
| GitHub Trending | Daily trending page | Hottest SF repos this week |

---

## Accessibility Roadmap (v0.2+)

WCAG 2.2 AA for dashboard + LWC audit tooling for Salesforce projects.

- Keyboard navigation for all interactive elements
- ARIA roles + live regions on all dynamic content
- axe-core audit → auto-create tasks per violation
- High-contrast mode (`prefers-contrast: high`)
- Screen reader smoke tests (VoiceOver + NVDA)

See [prd/PRD-06-ACCESSIBILITY.md](../prd/PRD-06-ACCESSIBILITY.md)

---

## Priority Table

| Feature | Impact | Effort | Priority |
|---------|--------|--------|----------|
| SF Ecosystem view in dashboard | High | Low | P0 |
| Web Intel view in dashboard | High | Low | P0 |
| Analytics + perf tracking | Medium | Low | P0 |
| Agentforce agent list | High | Medium | P1 |
| Apex log → task auto-create | High | Medium | P1 |
| Brain streaming SSE | High | Medium | P1 |
| Vector memory (ChromaDB) | High | High | P2 |
| GitHub sync | Medium | Medium | P2 |
| Eval harness | Medium | High | P3 |
| YouTube/Twitter ingestion | Medium | High | P3 |
