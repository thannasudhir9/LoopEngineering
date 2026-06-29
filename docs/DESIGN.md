# LoopEngineering — Design

*Last updated: 2026-06-29 (session 2)*

---

## Design Principles

1. **Local-first** — all data stays on machine; no cloud dependency
2. **Zero-framework frontend** — vanilla JS, single HTML file, no build step
3. **Real-time by default** — WebSocket push + 3s HTTP poll fallback
4. **Additive state** — tasks/projects never hard-deleted (soft status)
5. **Progressive enhancement** — works without API keys; features unlock as keys added
6. **Audit trail** — every meaningful action logged to JSONL with timestamp
7. **Salesforce-native** — SF clouds are first-class entities, not just projects
8. **Web-aware** — fetch signals from GitHub, Reddit, HN, Dev.to to inform tasks

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
│  Salesforce  │                                              │
│  Web Intel   │                                              │
│  Analytics   │                                              │
│  Roadmap     │                                              │
│  Settings    │                                              │
│  MCP    [20] │                                              │
│  Console     │                                              │
│  ─ Projects ─│                                              │
│  [show/hide] │                                              │
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
| SF Cloud colors | per-cloud hex | same | Cloud identity badges |

---

## Component Patterns

### Stat Card
```
┌─────────────────┐
│ LABEL           │
│ 42              │ ← large font-weight:700
│ subtitle text   │ ← text3, 11px
└─────────────────┘
```

### Panel
- `background: var(--bg2)`, border, border-radius 12px
- Header: flex row, title left, action right
- Body: padding 16–18px or padding:0 for full-width tables

### Toggle Switch
- `role="switch"`, `aria-checked`
- 36×20px pill, 14px circle handle
- Checked: `--blue` background

### MCP Row
- Health dot (green/red/gray) + name + command (monospace truncated)
- Right: type badge + status text + toggle
- Duplicate servers shown with `override` badge at 0.7 opacity

### SF Cloud Card
- Color-accented left border (cloud brand color)
- Icon + name + desc + feature chips
- Brain badge: primary + secondary AI recommendation
- Task count badge
- Search button → triggers Web Intel query

### Web Intel Result Card
- Source badge: GitHub (black) / Reddit (orange) / HN (red) / Dev.to (purple)
- Title + desc + URL link
- Score/stars metric + comment count
- Author + date

### Analytics Card
- Sparkline mini-chart (SVG inline)
- Delta badge: +N% vs previous period
- Time-series stored in `S.analytics`

---

## State Management

```javascript
const S = {
  // Core
  projects: [],
  tasks: [],
  loops: [],
  processes: [],
  fsEvents: [],
  settings: {},

  // Navigation
  activeView: 'overview',
  activeProject: null,
  projectsVisible: true,   // show/hide projects sidebar

  // MCP
  mcpServers: [],

  // Salesforce
  sfEcosystem: {},         // {cloud_id: {name, icon, color, brain, task_count, ...}}
  activeCloud: null,

  // Web Intelligence
  webIntel: {
    query: '',
    results: {},           // {github:[], reddit:[], hackernews:[], devto:[]}
    loading: false,
    lastSearch: null,
  },

  // Analytics
  analytics: {
    tasksByDay: [],        // [{date, count}]
    loopSuccessRate: 0,
    brainUsage: {},        // {claude: N, openai: N, ...}
    processUptime: {},     // {label: minutes}
  },

  // Performance
  perf: {
    apiLatency: {},        // {endpoint: [ms, ms, ...]}
    renderTime: [],        // [ms]
    pollCount: 0,
    wsEvents: 0,
  },
};
```

---

## Settings Architecture

```
DEFAULT_GLOBAL_SETTINGS
  ├── auto_refresh_interval: 3
  ├── process_scan_interval: 5
  ├── watch_filesystem: true
  ├── notifications_enabled: true
  ├── theme: "dark"
  ├── ai_brains: {claude, openai, gemini, grok, deepseek, ollama}
  └── integrations: {github, slack, jira, linear, notion, discord}

DEFAULT_PROJECT_SETTINGS (per project, deep-merged over global)
  ├── watch_filesystem: true
  ├── default_brain: "claude"
  ├── auto_create_notes: true
  ├── allowed_brains: ["claude"]
  └── integrations: {github, jira, linear}
```

---

## MCP Design

- Scan order: `~/.claude.json` → `~/.claude/settings.json` → per-project `.claude/settings.json`
- Later entries override earlier (per-project wins over global)
- Duplicate tracking: first occurrence is canonical, later marked `duplicate: true`
- Toggle: atomic write via `.tmp` + `.replace()` — never partial file state
- Health cache: `~/.claude/mcp-health-cache.json` read-only from dashboard

---

## Salesforce Ecosystem Design

- 12 clouds defined in `src/sf_ecosystem.py` — single source of truth
- Each cloud has: icon, brand color, MCP server name, search keywords, folder path
- Brain mapping: recommended primary + secondary AI per cloud task type
- Cloud folders live at `salesforce-ecosystem/<cloud>/src/`
- Web Intel integration: each cloud card has "Search" button pre-filled with cloud keywords
- Tasks tagged with cloud folder name auto-linked to that cloud's task count

---

## Web Intelligence Design

- Public APIs only — no auth tokens, no rate limit abuse
- GitHub: `/search/repositories?sort=stars` — highest star repos first
- Reddit: `r/salesforce+mulesoft+apexcode+devops` — relevant SF subreddits
- HN: Algolia search API — top stories by relevance
- Dev.to: `/articles?tag=` — community articles by tag
- All sources run in parallel (`asyncio.gather`) — total latency = slowest single source
- Results cached in `S.webIntel.results` until next search
- Logged to `prompt_log` as `web_intel_search` event

---

## Prompt Logging Design

- Every user-visible action emits a `prompt_log.log()` call
- JSONL format: one object per line, never truncated
- Fields always present: `ts` (ISO 8601 UTC ms), `type`
- Session markdown log: `logs/SESSION-YYYY-MM-DD-prompts.md` — human-readable
- Raw prompt capture: `POST /api/logs/prompt` accepts `{text, source}` from UI, hooks, or external tools

---

## Performance Design

- API calls wrapped: `const t0 = performance.now(); ... S.perf.apiLatency[path].push(ms)`
- Render time: `performance.now()` before/after `render()`
- Analytics view shows: p50/p95 latency per endpoint, render histogram
- `S.perf.pollCount` increments each successful poll — uptime proxy
- `S.perf.wsEvents` increments each WS message received

---

## Decisions Log

| Date | Decision | Reason |
|------|----------|--------|
| 2026-06-29 | Vanilla JS, no framework | Zero build complexity; single HTML file |
| 2026-06-29 | JSONL for prompt logs | Append-only, grep-friendly, no schema migrations |
| 2026-06-29 | Atomic MCP toggle | Prevent partial config file corruption |
| 2026-06-29 | SF ecosystem as in-memory constants | Clouds don't change; avoids DB overhead |
| 2026-06-29 | Web Intel via asyncio.gather | All sources ~same latency; parallel is free |
| 2026-06-29 | salesforce-ecosystem/ inside LoopEngineering | Single repo, single git history |
| 2026-06-29 | GitHub API unauthenticated | 60 req/hr sufficient for manual searches; no token needed |
