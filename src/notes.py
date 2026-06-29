"""
Notes Generator — creates structured markdown docs (plan, design, architecture) per task.
Saves to notes/<project-slug>/<date-task-slug>/
"""
import re
from datetime import datetime
from pathlib import Path

NOTES_DIR = Path(__file__).parent.parent / "notes"
NOTES_DIR.mkdir(exist_ok=True)


def _slug(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text[:60].strip("-")


def _date() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def create_task_notes(project_name: str, task_id: str, task_title: str,
                      description: str = "", tags: list[str] | None = None) -> str:
    project_slug = _slug(project_name)
    task_slug = _slug(task_title)
    task_dir = NOTES_DIR / project_slug / f"{_date()}-{task_slug}"
    task_dir.mkdir(parents=True, exist_ok=True)

    tags_str = ", ".join(tags) if tags else "none"
    date_str = _date()

    (task_dir / "index.md").write_text(f"""# {task_title}

| Field | Value |
|-------|-------|
| Task ID | `{task_id}` |
| Project | {project_name} |
| Date | {date_str} |
| Tags | {tags_str} |
| Status | open |

## Description

{description or "_No description provided._"}

## Quick Links

- [Plan](plan.md)
- [Design](design.md)
- [Architecture](architecture.md)
- [Loop Log](loop-log.md)
""")

    (task_dir / "plan.md").write_text(f"""# Plan — {task_title}

**Date:** {date_str}  **Task:** `{task_id}`

## Goal

> What does "done" look like?

## Scope

### In Scope
- [ ] Item 1

### Out of Scope
- Item 1

## Steps

| # | Step | Owner | Status |
|---|------|-------|--------|
| 1 | Define requirements | human | pending |
| 2 | Implement | AI loop | pending |
| 3 | Verify | checker agent | pending |
| 4 | Close | human | pending |

## Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Scope creep | medium | Hard gate on out-of-scope |
""")

    (task_dir / "design.md").write_text(f"""# Design — {task_title}

**Date:** {date_str}

## Problem Statement

_What problem does this solve and for whom?_

## Proposed Solution

_High-level description of the approach._

## Interface / API Contract

```
# inputs, outputs, side effects
```

## Data Model

_Entities, fields, relationships._

## Error Handling

| Error | Strategy |
|-------|---------|
| Example | Retry with backoff |

## Testing Strategy

- Unit: _what to unit test_
- Integration: _what to integration test_
- Manual: _what to verify by hand_

## Alternatives Considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Option A | | | chosen |
| Option B | | | rejected |
""")

    (task_dir / "architecture.md").write_text(f"""# Architecture — {task_title}

**Date:** {date_str}

## System Context

_How does this fit in the larger system?_

## Component Diagram

```
+-------------+     +-------------+
| Component A |---->| Component B |
+-------------+     +-------------+
```

## Components

### Component A
- **Purpose:**
- **Interface:**
- **Dependencies:**

## Data Flow

1. Step 1
2. Step 2
3. Step 3

## Key Decisions

| Decision | Rationale |
|----------|-----------|

## Non-Functional Requirements

| NFR | Target |
|-----|--------|
| Performance | < 200ms p99 |
| Reliability | No data loss |
""")

    (task_dir / "loop-log.md").write_text(f"""# Loop Log — {task_title}

**Task:** `{task_id}`  **Started:** {date_str}

---

""")

    return str(task_dir)


def append_loop_entry(notes_path: str, iteration: int, status: str,
                      action: str, result: str, next_step: str = ""):
    log_file = Path(notes_path) / "loop-log.md"
    if not log_file.exists():
        return
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""## Iteration {iteration} — {ts}

**Status:** {status}  **Action:** {action}
**Result:** {result}
**Next:** {next_step or "_TBD_"}

---

"""
    with open(log_file, "a") as f:
        f.write(entry)


def update_task_status_in_notes(notes_path: str, status: str):
    index_file = Path(notes_path) / "index.md"
    if not index_file.exists():
        return
    content = index_file.read_text()
    content = re.sub(r"\| Status \| .+ \|", f"| Status | {status} |", content)
    index_file.write_text(content)
