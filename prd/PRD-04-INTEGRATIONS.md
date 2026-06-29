# PRD-04 — Integrations

*Status: Planned | Last updated: 2026-06-29*

## Goal
Connect LoopEngineering to external tools: GitHub, Slack, Jira, Linear, Notion, Discord, Calendar, Email.

## User Stories
- As a developer, I want tasks auto-synced to GitHub Issues
- As a developer, I want Slack notifications when loops finish
- As a developer, I want to pull my Jira sprint backlog into LoopEngineering
- As a developer, I want loop notes exported to Notion automatically

## Tasks & Subtasks

### 🔲 T1 — GitHub / GitLab
- [ ] T1.1 Config: token + repo in Settings > Integrations
- [ ] T1.2 `POST /api/integrations/github/push-task` — create GH Issue from task
- [ ] T1.3 Webhook ingress `/api/webhooks/github` — GH events create tasks
- [ ] T1.4 Status sync: LoopEngineering status <-> GH Issue state
- [ ] T1.5 Loop log -> PR comment on linked PR
- [ ] T1.6 Dashboard: GitHub badge per task showing issue #

### 🔲 T2 — Slack / Discord
- [ ] T2.1 Config: webhook URL per project or global
- [ ] T2.2 `POST /api/integrations/slack/notify` — send message
- [ ] T2.3 Events that trigger: loop_finished, loop_failed, task critical created
- [ ] T2.4 Bot slash commands: `/loop status`, `/task create`
- [ ] T2.5 Thread: loop iterations posted as Slack thread replies

### 🔲 T3 — Jira / Linear
- [ ] T3.1 Config: Jira base URL + token + project key
- [ ] T3.2 `GET /api/integrations/jira/sync` — pull sprint tasks in
- [ ] T3.3 Status mapping: open->To Do, in_progress->In Progress, done->Done
- [ ] T3.4 Push loop results as Jira comments
- [ ] T3.5 Priority mapping: critical->P1, high->P2

### 🔲 T4 — Notion / Obsidian
- [ ] T4.1 Config: Notion token + database ID
- [ ] T4.2 Export task notes to Notion page on task `done`
- [ ] T4.3 Import Notion database rows as LoopEngineering tasks
- [ ] T4.4 Obsidian: write notes to vault via Obsidian-CLI MCP

### 🔲 T5 — Webhooks (Ingress)
- [ ] T5.1 `/api/webhooks/ingest` — accept signed payloads from any system
- [ ] T5.2 HMAC-SHA256 signature verification
- [ ] T5.3 5-minute replay window
- [ ] T5.4 Dead-letter queue: retry x3 on failure

### 🔲 T6 — Calendar & Email
- [ ] T6.1 Google Calendar: create event from task due_date
- [ ] T6.2 Schedule loops as calendar time-blocks
- [ ] T6.3 Daily digest email: loop outcomes + blocked tasks

## Acceptance Criteria
- GitHub: task created -> GH Issue created within 5s
- Slack: loop finish -> Slack message within 10s
- Jira: pull sprint -> tasks appear in LoopEngineering within 30s
- Webhooks: external POST -> task created within 2s

## Dependencies
- PRD-01 (Tasks, Loops)
- Valid tokens for each integration
