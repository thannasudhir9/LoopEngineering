# Loop Engineering — Research & Reference

## Core Definition

Loop Engineering = designing systems that prompt AI agents on your behalf instead of prompting manually.
Replace yourself as the person who prompts. Build the system that does it instead.

**Shift:** Human writes prompt → reads → writes next prompt  
→ System discovers work → dispatches agents → verifies results → determines next steps autonomously

---

## Primary Sources

| Source | URL | Key Insight |
|--------|-----|-------------|
| Addy Osmani — Loop Engineering | https://addyosmani.com/blog/loop-engineering/ | Full methodology: 5 components, maker/checker separation, skills prevent intent debt |
| MindStudio — What Is Loop Engineering | https://www.mindstudio.ai/blog/what-is-loop-engineering-ai-coding-agents | ReAct pattern, loop types, termination logic |
| Oracle Developers — AI Agent Loop | https://blogs.oracle.com/developers/what-is-the-ai-agent-loop-the-core-architecture-behind-autonomous-ai-systems | Core architecture of autonomous AI agent loops |
| Reddit r/clawdbot — Loop Engineering | https://www.reddit.com/r/clawdbot/comments/1u0zpbn/loop_engineering_the_missing_layer_between/ | "The missing layer between prompts and outcomes" |
| Cursor Forum | https://forum.cursor.com/t/loop-engineering-more-autonomous-development/163082 | Multi-agent coding, parallel tasks in Cursor |
| YouTube — Loop Engineering in 9 Minutes | https://www.youtube.com/watch?v=nKlF15Ic78w | Stop prompting, start building loops |
| YouTube — Why Everyone is Talking About Agentic Loops | https://www.youtube.com/watch?v=7BrxIBkX3mg | Agentic loops overview |
| YouTube — Build Autonomous Loops | https://www.youtube.com/watch?v=q3YvFYtuhec | Practical autonomous loop construction |
| Instagram Post | https://www.instagram.com/p/DZeHlriCTt9/?igsh=b2dweWh1dmRueHR5 | Visual intro to Loop Engineering concept |

---

## Core Components (from Addy Osmani)

| Component | Purpose |
|-----------|---------|
| **Automations** | Scheduled discovery/triage — the heartbeat of the loop |
| **Worktrees** | Git-isolated dirs — parallel agents don't overwrite each other |
| **Skills** | Codified project knowledge (SKILL.md) — context survives across runs |
| **Connectors** | MCP-based integrations — connects agents to real tools |
| **Sub-agents** | Maker vs Checker separation — writer != reviewer |
| **Memory/State** | External persistent storage — markdown files, issue boards |

---

## Key Principles

1. **Automation as Heartbeat** — scheduled runs surface work continuously
2. **Isolation via Worktrees** — parallel agents need isolated dirs
3. **Skills prevent Intent Debt** — every session without skills starts cold
4. **Maker/Checker Separation** — agent that wrote code can't reliably grade it
5. **Connectors enable real-world action** — filesystem-only loops have narrow impact
6. **Goal-based stopping** — a separate model decides "done", not the one that did the work

## Loop Types (ReAct Pattern)

- **Retry Loop** — simple pass/fail, atomic tasks
- **Plan-Execute-Verify** — multi-step, order-dependent
- **Explore-Narrow** — debugging unknown errors, tests multiple paths
- **Human-in-the-Loop** — pauses for ambiguous requirements

## What Loops Don't Solve

- Verification responsibility stays human
- Comprehension debt accelerates with faster loops
- Cognitive surrender — loops replace thinking instead of amplifying it

---

## This Project: LoopEngineering App

**Goal:** Monitor all AI tasks (Claude, Claude Code, Cursor) running on system.
Loop until issues fixed. Auto-generate notes (plan, design, architecture) per task.
Interactive web dashboard for all projects/tasks/issues/priorities.

**Architecture:** Local Python server (FastAPI/http.server) + HTML/JS frontend
- Real-time filesystem watching via watchdog
- Process monitoring via psutil (macOS ps/lsof)
- WebSocket push to browser
- Zero cloud, runs fully local

---

*Last updated: 2026-06-29*
