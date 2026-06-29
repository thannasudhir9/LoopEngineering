# LoopEngineering — Future Scope

> Living document. Tracks planned expansion across agents, multi-brain AI, integrations, and intelligence layer.

---

## Phase 1 — Agents & Sub-Agents

### Agent Registry
- Register named agents (Claude Code, Cursor, Aider, Copilot, etc.) with roles, capabilities, and health status
- Each agent has: `name`, `type`, `model`, `status` (idle/busy/error), `capabilities[]`, `assigned_projects[]`
- Persist registry in `data/agents.json`; expose via `/api/agents`

### Sub-Agent Trees
- Spawn child agents from a parent task
- Each task can own a tree of sub-agents (e.g. "Research" → ["Web Search", "Code Analysis", "Summarizer"])
- Dashboard: collapsible agent-hierarchy tree per task
- State tracks: `parent_agent_id`, `children[]`, `depth`, `spawned_at`

### Agent Orchestrator
- Route tasks to best-fit agent based on: task type, current load, declared capabilities, priority
- Round-robin and priority-weighted routing strategies
- Retry failed agents with configurable fallback chain: `claude → openai → local-ollama`
- Deadlock detection: if child never completes, parent auto-escalates

### Inter-Agent Messaging
- Pub/sub event bus: agents publish results, other agents subscribe
- Message schema: `{ from, to, type, payload, ts, correlation_id }`
- Durable queue: messages survive agent restart (persisted to `data/messages/`)
- Dashboard: message trace view per task (timeline of agent-to-agent calls)

### Agent Loop Delegation
- Any agent can create, assign, and monitor loops on behalf of other agents
- Parent agent sets goal; child agents execute iterations
- Loop ownership transfer: if parent dies, ownership shifts to next available agent
- Loop aggregation: multiple child results merged into single parent loop log

---

## Phase 2 — Multi-Brain AI Connections

### OpenAI (GPT-4o / o3)
- Connect via OpenAI API (`openai` Python SDK)
- Route reasoning-heavy tasks to o3; fast/cheap tasks to GPT-4o-mini
- Streaming support for loop logs (tokens streamed to dashboard in real-time)
- Function/tool calling mapped to LoopEngineering task actions

### Google Gemini (2.0 Flash / 2.5 Pro)
- Gemini Flash for speed; Pro for deep reasoning
- Multimodal: pass images, PDFs, code screenshots directly to tasks
- Grounding with Google Search: research tasks auto-web-grounded
- Long context (1M tokens): entire project codebase as context

### xAI Grok 3
- Real-time X/Twitter data access for trend monitoring tasks
- Use for: market research loops, live event tracking, social signal tasks
- API via `https://api.x.ai/v1` (OpenAI-compatible)

### DeepSeek R2 / Coder
- Open-weight model; self-hostable via Ollama integration
- Best for: code generation loops, code review tasks, refactoring agents
- Run locally: zero API cost for heavy code loops

### Anthropic Claude (all tiers)
- Sonnet 4.6 (current), Opus 4.8 (deep reasoning), Haiku 4.5 (fast/cheap)
- Auto-select tier by task `priority` + estimated token budget
- Extended thinking mode for `critical` priority tasks
- Computer use capability for UI-automation loops

### Brain Selector UI
- Per-task brain picker in task creation modal
- Per-project default brain in Settings → Per-Project Controls
- Cost estimate shown before dispatch (tokens × price/token)
- Fallback chain configurable per project: e.g. `claude → gemini → ollama`
- Live brain status indicator (green = API reachable, red = down)

### Unified Context Protocol (MCP)
- MCP-compatible context passing across all brains
- Share: files, tool results, memory, conversation history across providers
- Context window management: auto-summarize when approaching limits
- Tool registry: all LoopEngineering tools (tasks, loops, notes, fs-watch) exposed as MCP tools to any brain

---

## Phase 3 — Integrations

### GitHub / GitLab
- Auto-create GitHub Issues from LoopEngineering tasks (bidirectional sync)
- Link PRs to loops: loop log entries appear as PR comments
- Sync task `status` with issue state (open/closed/in-progress label)
- Webhook ingress: GitHub events (push, PR, review) create tasks automatically
- Config: `Settings → Integrations → GitHub → token + repo`

### Jira / Linear
- Pull sprint backlog into LoopEngineering as tasks (scheduled or on-demand)
- Push loop results back as Jira comments / Linear updates
- Status mapping: `open → To Do`, `in_progress → In Progress`, `done → Done`
- Priority mapping: `critical → P1`, `high → P2`, etc.

### Slack / Discord
- Notify channels on: loop finish, critical task alerts, agent failures, daily digest
- Accept slash commands via bot: `/loop start <task_id> <goal>`, `/task create`, `/status`
- Thread replies: loop log entries posted as Slack thread updates
- Config: webhook URL per project or global fallback

### Notion / Obsidian
- Export task notes to Notion pages (auto-sync on task `done`)
- Import Notion databases as project sources (populate tasks from Notion rows)
- Obsidian: write markdown notes to vault via Obsidian-CLI MCP server
- Bidirectional: status changes in Notion reflected back in LoopEngineering

### VS Code / Cursor Extension
- Sidebar panel showing live tasks and loops for the open workspace
- Click loop log entry → jump to file:line in editor
- Quick-create task from selected code (right-click context menu)
- Status bar: shows active loop count and current AI brain

### Webhook Ingress
- Any external system can POST task/loop updates to `/api/webhooks/ingest`
- HMAC-SHA256 signed payloads with 5-minute replay window
- Schema: `{ event_type, project_id, payload, signature, ts }`
- Dead-letter queue for failed deliveries (retry × 3 with backoff)

### Calendar (Google / Outlook)
- Schedule tasks as time-blocked calendar events
- Deadline tracking: task `due_date` → calendar event; overdue tasks flagged red
- Loop schedules: run loops at scheduled calendar times (cron-like)

### Email Digest
- Daily/weekly summary email: loop outcomes, blocked tasks, AI usage stats
- Configurable: per-project or global digest
- Template: markdown rendered to HTML via Python `mistune`

---

## Phase 4 — Intelligence Layer

### Cross-Brain Memory
- Shared vector store (ChromaDB or Qdrant, self-hosted) across all AI brains
- Embeddings generated by any provider; queried by all agents
- Memory types: `episodic` (loop logs), `semantic` (task descriptions), `procedural` (loop patterns)
- Dashboard: memory browser — search embeddings, see source tasks

### Task Auto-Decomposition
- Drop a high-level goal; system breaks it into subtasks
- Uses configured brain (default Claude) to generate task tree
- Assigns agents to subtasks based on type and brain capabilities
- Cost estimate shown before decomposition commits

### Cost & Token Dashboard
- Per-brain spend tracking (tokens in/out × price)
- Budget caps: per-project daily/monthly limits
- Alert when approaching 80% of budget cap
- Charts: spend over time, cost per task, cost per loop, brain comparison

### Loop Replay & Diff
- Store full loop execution snapshots in `data/loop_snapshots/`
- Compare two loop runs side-by-side: diff inputs, outputs, tool calls
- Detect regressions: if loop outcome quality drops, auto-flag
- Export diff as markdown report

### Agent Eval Harness
- Run benchmark tasks against multiple brains simultaneously
- Score each brain on: accuracy, speed (ms), cost (tokens), completeness
- Ranking table in dashboard
- Scheduled evals: run nightly, track brain quality over time

### Self-Healing Loops
- Detect stuck loops: no log entry for N seconds → considered stuck
- Auto-restart with: increased max_iterations, switched brain, or reduced scope
- Failure analysis: use brain to diagnose why loop failed, suggest fix
- Circuit breaker: if loop fails 3× in a row, pause and alert

---

## Architecture Vision (End State)

```
┌─────────────────────────────────────────────────────┐
│                  LoopEngineering                     │
│  Dashboard (Vanilla JS)        ←→  FastAPI Backend  │
│                                         │            │
│  ┌──────────────────────────────────────┼──────┐    │
│  │           Agent Orchestrator                │    │
│  │  ┌────────┐ ┌────────┐ ┌────────┐          │    │
│  │  │ Agent1 │ │ Agent2 │ │ AgentN │          │    │
│  │  │Claude  │ │Cursor  │ │ Aider  │          │    │
│  │  └────┬───┘ └────┬───┘ └────┬───┘          │    │
│  │       └──────────┴──────────┘               │    │
│  │              Inter-Agent Bus                │    │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │           Brain Router                       │   │
│  │  Claude | GPT-4o | Gemini | Grok | DeepSeek  │   │
│  │         └─── Unified MCP Context ───┘        │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Integrations                                │   │
│  │  GitHub | Jira | Slack | Notion | Calendar   │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Intelligence Layer                          │   │
│  │  Vector Memory | Auto-Decompose | Eval | Heal│   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Priority Order

| # | Feature | Effort | Value | Phase |
|---|---------|--------|-------|-------|
| 1 | Agent Registry + basic orchestrator | M | High | 1 |
| 2 | Claude multi-tier brain selector | S | High | 2 |
| 3 | OpenAI + Gemini brain connections | M | High | 2 |
| 4 | GitHub integration | M | High | 3 |
| 5 | Slack notifications | S | Medium | 3 |
| 6 | Sub-agent trees (UI + backend) | L | High | 1 |
| 7 | Cross-brain vector memory | L | High | 4 |
| 8 | Task auto-decomposition | M | High | 4 |
| 9 | Jira/Linear sync | M | Medium | 3 |
| 10 | Cost & token dashboard | M | Medium | 4 |
| 11 | Self-healing loops | L | Medium | 4 |
| 12 | VS Code extension | L | Medium | 3 |
| 13 | Grok + DeepSeek brains | S | Low | 2 |
| 14 | Loop replay & diff | M | Medium | 4 |
| 15 | Agent eval harness | L | Medium | 4 |

*Effort: S=days, M=1-2 weeks, L=3-4 weeks*

---

*Last updated: 2026-06-29*
