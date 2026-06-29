# PRD-02 — AI Features

*Status: Planned | Last updated: 2026-06-29*

## Goal
Connect multiple AI brains (Claude, OpenAI, Gemini, Grok, DeepSeek, Ollama), route tasks intelligently, stream responses, and auto-decompose goals into subtasks.

## User Stories
- As a developer, I want to validate any AI brain API key directly from the dashboard
- As a developer, I want to pick which brain handles each task
- As a developer, I want the system to automatically fall back to a secondary brain if the primary fails
- As a developer, I want to see live streaming responses in the loop log
- As a developer, I want to drop a high-level goal and get it broken into subtasks automatically

## Tasks & Subtasks

### ✅ T1 — Brain Config & Test
- [x] T1.1 Settings UI: enable/disable per brain, API key, model name
- [x] T1.2 `POST /api/brains/test` — "Hello, what is your model?" per brain
- [x] T1.3 Visual result: green ✓ model-name or red ✗ error
- [x] T1.4 Support: Claude, OpenAI, Gemini, Grok, DeepSeek, Ollama

### 🔲 T2 — Brain Router
- [ ] T2.1 Per-task brain selector in task creation modal
- [ ] T2.2 Per-project default brain in Settings
- [ ] T2.3 Fallback chain config: `claude → openai → ollama`
- [ ] T2.4 Cost estimate before dispatch (tokens × price/token)
- [ ] T2.5 Live brain status indicator (API reachable check every 60s)

### 🔲 T3 — Streaming Responses
- [ ] T3.1 Server-Sent Events (SSE) endpoint `/api/brains/stream`
- [ ] T3.2 Stream tokens directly into loop log entries in real time
- [ ] T3.3 Support streaming for: Claude (Anthropic SDK), OpenAI, Gemini
- [ ] T3.4 Abort button to cancel mid-stream

### 🔲 T4 — Task Auto-Decomposition
- [ ] T4.1 "Decompose" button on task — sends goal to selected brain
- [ ] T4.2 Brain returns structured subtask list (JSON schema enforced)
- [ ] T4.3 Subtasks created as child tasks linked to parent
- [ ] T4.4 UI: collapsible subtask tree per task
- [ ] T4.5 Cost shown before decompose (estimated tokens)

### 🔲 T5 — Multi-Model Execution
- [ ] T5.1 Run same task against multiple brains in parallel
- [ ] T5.2 Results displayed side-by-side for comparison
- [ ] T5.3 Score each response (user thumbs up/down)
- [ ] T5.4 Save winning response as task note

### 🔲 T6 — Unified MCP Context
- [ ] T6.1 All LoopEngineering tools exposed as MCP tools
- [ ] T6.2 Any brain can call: `create_task`, `log_loop`, `get_projects`
- [ ] T6.3 Context window management: auto-summarize at 80% capacity
- [ ] T6.4 Shared memory across brain calls within same task

## Acceptance Criteria
- All 6 brains have working test buttons
- Brain test returns model name in response
- Fallback chain retries on 429/500 automatically
- Streaming shows tokens in loop log with < 200ms first-token latency
- Auto-decompose creates >= 3 subtasks from a complex goal

## Dependencies
- PRD-01 (Tasks, Loops) must be complete
- Valid API keys for each brain

## Notes
- Claude uses `ANTHROPIC_BASE_URL` env (SF proxy configured)
- Ollama runs locally at `http://localhost:11434`
- DeepSeek Coder best for code-heavy loops
