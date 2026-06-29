# PRD-03 — Agents & Sub-Agents

*Status: Planned | Last updated: 2026-06-29*

## Goal
Registry of named AI agents with roles and capabilities. Spawn sub-agent trees from tasks. Orchestrate routing, delegation, and inter-agent messaging.

## User Stories
- As a developer, I want to register Claude Code, Cursor, and Aider as agents
- As a developer, I want to assign a task to an agent and track its progress
- As a developer, I want to spawn sub-agents from a parent task
- As a developer, I want agents to pass results to each other without manual copy-paste
- As a developer, I want the orchestrator to auto-route tasks to the best agent

## Tasks & Subtasks

### 🔲 T1 — Agent Registry
- [ ] T1.1 Data model: `{id, name, type, model, capabilities[], status, assigned_projects[]}`
- [ ] T1.2 `POST /api/agents` — register agent
- [ ] T1.3 `GET /api/agents` — list with live status
- [ ] T1.4 `PATCH /api/agents/:id` — update status/capabilities
- [ ] T1.5 Persist to `data/agents.json`
- [ ] T1.6 Dashboard view: Agents list with health dots

### 🔲 T2 — Sub-Agent Trees
- [ ] T2.1 Add `parent_agent_id`, `children[]`, `depth` to agent model
- [ ] T2.2 `POST /api/agents/:id/spawn` — create child agent
- [ ] T2.3 Dashboard: collapsible tree view per task
- [ ] T2.4 Tree depth limit: 5 levels
- [ ] T2.5 Orphan handling: re-parent to root if parent dies

### 🔲 T3 — Agent Orchestrator
- [ ] T3.1 Routing strategies: round-robin, priority-weighted, capability-match
- [ ] T3.2 `POST /api/orchestrator/assign` — assign task to best agent
- [ ] T3.3 Load balancing: track active task count per agent
- [ ] T3.4 Fallback chain: if agent fails, retry next in configured chain
- [ ] T3.5 Deadlock detection: escalate if child never completes (timeout configurable)

### 🔲 T4 — Inter-Agent Messaging Bus
- [ ] T4.1 Message schema: `{id, from, to, type, payload, ts, correlation_id}`
- [ ] T4.2 `POST /api/messages` — send message between agents
- [ ] T4.3 `GET /api/messages?agent_id=` — inbox for agent
- [ ] T4.4 Durable queue: persist to `data/messages/`
- [ ] T4.5 Dashboard: message trace timeline per task

### 🔲 T5 — Loop Delegation
- [ ] T5.1 Any agent can create/assign/monitor loops for other agents
- [ ] T5.2 Loop ownership transfer on parent failure
- [ ] T5.3 Result aggregation: merge multiple child loop outputs

## Acceptance Criteria
- Register Claude Code as agent, assign task, see status update
- Spawn 2 sub-agents from parent, see tree in UI
- Orchestrator routes "code review" task to Aider, "research" to Claude
- Message sent from agent A received by agent B via inbox

## Dependencies
- PRD-01 (Tasks, Loops)
- PRD-02 (Brain Router) for agent-to-brain assignment
