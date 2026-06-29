# Prompt Logs

JSONL interaction log. One file per day, one JSON object per line.

## File Pattern
```
logs/prompts-YYYY-MM-DD.jsonl
```

## Entry Format
```json
{"ts":"2026-06-29T13:00:00.000Z","type":"task_created","task_id":"abc123","title":"Fix auth bug","project":"MyApp","priority":"high","tags":["auth"]}
```

## Fields
| Field | Always? | Description |
|-------|---------|-------------|
| `ts` | yes | UTC timestamp (ISO 8601 milliseconds) |
| `type` | yes | Event type (see below) |
| `...` | varies | Event-specific fields |

## Event Types
| type | When | Extra fields |
|------|------|-------------|
| `task_created` | Task POST | task_id, title, project, priority, tags |
| `loop_started` | Loop POST | loop_id, task_id, goal, max_iterations |
| `brain_test` | POST /api/brains/test | brain, model, ok, error, replied_model |
| `mcp_toggle` | PATCH /api/mcp/toggle | server, action (enable/disable), source |
| `project_added` | POST /api/projects | project, folder |

## API
Read last 3 days:
```
GET http://localhost:7070/api/logs
GET http://localhost:7070/api/logs?days=7
```

## Manual Read
```bash
cat logs/prompts-$(date +%Y-%m-%d).jsonl
# pretty print
cat logs/prompts-$(date +%Y-%m-%d).jsonl | python3 -m json.tool --no-ensure-ascii | less
```

Logs are append-only. Never truncated. Rotate by day automatically.
