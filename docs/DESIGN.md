# LoopEngineering — Design

*Last updated: 2026-06-29*

---

## Design Principles

1. **Local-first** — all data stays on machine; no cloud dependency
2. **Zero-framework frontend** — vanilla JS, single HTML file, no build step
3. **Real-time by default** — WebSocket push + 3s HTTP poll fallback
4. **Additive state** — tasks/projects never hard-deleted (soft status)
5. **Progressive enhancement** — works without API keys; features unlock as keys added
6. **Audit trail** — every meaningful action logged to JSONL with timestamp

---

## UI Design

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│ TOPBAR: logo · ws-status · ☀theme · +Project · +Task       │
├──────────────┬──────────────────────────────────────────────┤
│  SIDEBAR     │  CONTENT (scrollable)                        │
│  Overview    │                                              │
│  AI Procs    │  Active view renders here.                   │
│  All Tasks   │  Full DOM replace on every state change.     │
│  Loops       │                                              │
│  Activity    │                                              │
│  Roadmap     │                                              │
│  Settings    │                                              │
│  MCP    [20] │                                              │
│  Console     │                                              │
│  ─ Projects ─│                                              │
│  (dynamic)   │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

### Color System

| Token | Dark | Light | Usage |
|-------|------|-------|-------|
| `--bg` | `#0d0f14` | `#f0f2f7` | Page background |
| `--bg2` | `#151820` | `#ffffff` | Panel / sidebar |
| `--bg3` | `#1c2030` | `#e8eaf0` | Hover / group headers |
| `--bg4` | `#222638` | `#dde0ea` | Badges / inputs |
| `--text` | `#e2e6f3` | `#1a1d2e` | Primary text |
| `--text2` | `#9aa0b8` | `#4a5068` | Secondary / labels |
| `--text3` | `#5d6480` | `#8890a8` | Muted / metadata |
| `--blue` | `#4f8ef7` | same | Active / links |
| `--green` | `#3ecf8e` | same | Success / healthy |
| `--orange` | `#f5a623` | same | Warning / in-progress |
| `--red` | `#e85d5d` | same | Error / critical |
| `--purple` | `#a78bfa` | same | Loops / local MCP scope |
| `--cyan` | `#22d3ee` | same | Integrations / phase 3 |

### Component Patterns

- **Panels**: `bg2` background, `1px solid --border`, `border-radius: 12px`
- **Tables**: full-width, row hover `bg3`, no border-collapse
- **Status badges**: `<span>` with 15% opacity tint background
- **Toggle switches**: CSS-only checkbox (no JS for appearance)
- **Modals**: full-screen overlay, click-outside dismisses
- **Toasts**: fixed bottom-right, auto-dismiss 3.5s, success=green/error=red

---

## State Management

### Client State (`S` object)

```js
S = {
  projects:     [],    // from /api/projects
  tasks:        [],    // from /api/tasks
  loops:        [],    // from /api/loops
  processes:    [],    // from /api/processes (ephemeral, not persisted)
  settings:     {},    // global + per-project config
  mcpServers:   [],    // from /api/mcp/servers
  fsEvents:     [],    // ring buffer, max 200
  activeView:   'overview',
  activeProject: null,
}
```

### Update Strategy

| Source | Frequency | Action |
|--------|-----------|--------|
| WebSocket events | Instant | Targeted `upsert()` by id |
| HTTP poll (`pollSnapshot`) | Every 3s | Full sync of all collections |
| MCP scan | On first poll / manual Rescan | Full replace of `mcpServers` |

Full `render()` called after every update — acceptable for data sizes under ~1000 items. No virtual DOM needed.

### Server Persistence

- `data/state.json` written on every mutation via `_save()`
- Excludes: `processes` (ephemeral, always re-scanned)
- `_load()` called once at module import — merges saved data + new defaults

---

## Settings Architecture

### Two-Level Hierarchy

```
Global Settings  (DEFAULT_GLOBAL_SETTINGS in state.py)
    ↓ applies to all projects

Per-Project Settings  (DEFAULT_PROJECT_SETTINGS)
    ↓ overrides global per project
    ↓ stored under settings.projects[project_id]
    ↓ deep-merged: only set keys override, rest inherit global
```

### Brain Config Schema

```json
{
  "enabled": false,
  "model": "gpt-4o",
  "api_key": "",
  "base_url": ""
}
```

`api_key` stored in `data/state.json` local only. Not echoed back in plain text to browser.

### Integration Config Schema

```json
{
  "enabled": false,
  "token": "",
  "repo": "",
  "webhook_url": "",
  "project_key": ""
}
```

---

## MCP Design

### Discovery Priority

1. `~/.claude.json` — global user config (highest priority)
2. `~/.claude/settings.json` — global Claude Code settings
3. `<project>/.claude/settings.json` — per-project overrides

Health from `~/.claude/mcp-health-cache.json` (written by Claude Code).

### Toggle Mechanism

`PATCH /api/mcp/toggle` → reads source file → sets/unsets `"disabled": true` on the server block → writes file atomically. Claude Code re-reads on next session start.

### Display Grouping

| Badge | Color | Meaning |
|-------|-------|---------|
| GLOBAL | Blue | From `~/.claude*` |
| LOCAL | Purple | From project `.claude/settings.json` |
| override | Orange | Same name in multiple files |

### Health Dot

| Color | Status |
|-------|--------|
| Green | `healthy` |
| Grey | `unknown` (not yet checked or cache expired) |
| Red | `error` or `failed` |

---

## Prompt Logging Design

### Log Format (JSONL)

One JSON object per line, appended to `logs/prompts-YYYY-MM-DD.jsonl`:

```jsonl
{"ts":"2026-06-29T13:00:00.000Z","type":"task_created","project":"LoopEngineering","task_id":"abc","title":"Fix auth bug","priority":"high"}
{"ts":"2026-06-29T13:01:00.000Z","type":"loop_started","task_id":"abc","goal":"All tests pass","max_iterations":10}
{"ts":"2026-06-29T13:02:00.000Z","type":"brain_test","brain":"claude","ok":true,"model":"claude-sonnet-4-6"}
{"ts":"2026-06-29T13:03:00.000Z","type":"mcp_toggle","server":"github","action":"enable","source":"~/.claude/settings.json"}
```

### Logged Event Types

| Type | When |
|------|------|
| `task_created` | Task POST |
| `task_updated` | Task PATCH |
| `loop_started` | Loop POST |
| `loop_log` | Loop iteration logged |
| `loop_finished` | Loop finish |
| `brain_test` | Brain test attempted |
| `mcp_toggle` | MCP enable/disable |
| `settings_updated` | Settings PATCH |
| `project_added` | Project POST |

---

## Decisions Log

| Date | Decision | Reason |
|------|----------|--------|
| 2026-06-29 | Vanilla JS, no framework | Zero build tooling; single-file deployable |
| 2026-06-29 | FastAPI + uvicorn | Async native; WebSocket built-in |
| 2026-06-29 | JSONL for prompt logs | Append-only, streamable, grep-friendly, daily rotation |
| 2026-06-29 | Soft-delete tasks | Preserve history; loops reference task ids |
| 2026-06-29 | 3s poll + WebSocket | WS handles real-time; poll catches missed events |
| 2026-06-29 | data/state.json (not SQLite) | Simple, human-readable, no migration at this scale |
| 2026-06-29 | MCP toggle via file edit | Claude Code reads config files directly |
| 2026-06-29 | tmp/ scratch folder | Fast one-off testing without polluting src/ |
