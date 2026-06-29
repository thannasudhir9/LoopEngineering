# Prompt & Interaction Logs

**Location:** `/Users/sthanna/Downloads/Cursor/LoopEngineering/logs/`  
**Updated:** 2026-06-29 11:35 UTC

All user prompts, API actions, and system events captured here. Nothing omitted.

---

## File Types

| File | Format | Content |
|------|--------|---------|
| `prompts-YYYY-MM-DD.jsonl` | JSONL (1 JSON object per line) | Machine-readable event log, auto-written by server |
| `SESSION-YYYY-MM-DD-prompts.md` | Markdown | Human-readable prompt history per session |

---

## JSONL Entry Format

```json
{"ts":"2026-06-29T11:33:00.123Z","type":"user_prompt","source":"user","text":"dont miss anything..."}
```

### Always-present fields

| Field | Type | Description |
|-------|------|-------------|
| `ts` | ISO 8601 UTC with ms | Timestamp |
| `type` | string | Event type (see below) |

---

## Event Types

| `type` | When | Extra fields |
|--------|------|-------------|
| `user_prompt` | Raw user input captured | `source` (user/claude/cursor/other), `text` |
| `task_created` | Task POST | `task_id`, `title`, `project`, `priority`, `tags` |
| `loop_started` | Loop POST | `loop_id`, `task_id`, `goal`, `max_iterations` |
| `project_added` | Project POST | `project`, `folder` |
| `brain_test` | POST /api/brains/test | `brain`, `model`, `ok`, `error`, `replied_model` |
| `mcp_toggle` | PATCH /api/mcp/toggle | `server`, `action` (enable/disable), `source` |

---

## API Endpoints

### Push a raw prompt (from dashboard, Claude hooks, Cursor, etc.)
```
POST http://localhost:7070/api/logs/prompt
Content-Type: application/json

{"text": "your prompt here", "source": "user"}
```

### Read recent logs
```
GET http://localhost:7070/api/logs          # last 3 days (default)
GET http://localhost:7070/api/logs?days=7   # last 7 days
```

---

## Manual Read (Terminal)

```bash
# Today's log
cat logs/prompts-$(date +%Y-%m-%d).jsonl

# Pretty print
cat logs/prompts-$(date +%Y-%m-%d).jsonl | python3 -m json.tool --no-ensure-ascii | less

# Only user prompts
cat logs/prompts-$(date +%Y-%m-%d).jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    e = json.loads(line)
    if e.get('type') == 'user_prompt':
        print(e['ts'], '|', e['text'])
"
```

---

## Session Logs (Human-readable)

| File | Description |
|------|-------------|
| `SESSION-2026-06-29-prompts.md` | All 21 prompts from 2026-06-29 — full LoopEngineering build session |

---

## Properties

- **Append-only** — never truncated or overwritten
- **Daily rotation** — new file per UTC day automatically
- **No secrets** — API keys stripped before write
- **Written by:** `src/prompt_log.py` → called from `server.py` on every API action

---

*Last updated: 2026-06-29 11:35 UTC*
