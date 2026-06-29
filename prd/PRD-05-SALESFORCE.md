# PRD-05 — Salesforce Integration

*Status: Planned | Last updated: 2026-06-29*

## Goal
Deep integration with Salesforce platform: Agentforce agents, Revenue Cloud (RLM), MCP servers, Apex log analysis, org health monitoring, and deployment pipelines.

## Context
User has: Agentforce MCP server, salesforce-clouds-python MCP, mcp-adaptor, revenue-cloud-python, experience-cloud, omnistudio-python, datacloud-python, servicecloud-fieldservice-python, marketingcloud-python, commerce-python, industry-clouds-python, loyalty-python — all configured.

## User Stories
- As a Salesforce developer, I want to monitor all my SF org deployments as LoopEngineering tasks
- As a Salesforce developer, I want Apex log analysis results surfaced in the dashboard
- As a Salesforce developer, I want to trigger Agentforce agents from a LoopEngineering task
- As a Salesforce developer, I want Revenue Cloud quote-to-cash flows tracked as loops
- As a Salesforce developer, I want org readiness checks scheduled as recurring tasks

## Tasks & Subtasks

### 🔲 T1 — Salesforce MCP Bridge
- [ ] T1.1 Dashboard: show all 12 SF MCP servers with status and tool count
- [ ] T1.2 Enable/disable individual SF MCP servers from dashboard
- [ ] T1.3 Health ping: test each SF MCP server on demand
- [ ] T1.4 Group SF MCPs: Agentforce | Revenue Cloud | Experience | Industry Clouds

### 🔲 T2 — Agentforce Integration
- [ ] T2.1 `GET /api/sf/agents` — list all Agentforce agents via `agentforce_list_agents`
- [ ] T2.2 Create LoopEngineering task from Agentforce agent
- [ ] T2.3 Send preview messages to agent, stream response into loop log
- [ ] T2.4 Activate/deactivate Agentforce agents from dashboard
- [ ] T2.5 Link Agentforce runs to LoopEngineering loops
- [ ] T2.6 `agentforce_run_tests` — trigger test suite, log results as loop iterations
- [ ] T2.7 `agentforce_generate_agent_spec` — auto-generate task descriptions

### 🔲 T3 — Revenue Cloud / RLM Monitoring
- [ ] T3.1 Track quote-to-cash flows as LoopEngineering loops
- [ ] T3.2 `rlm_calculate_quote_price` — trigger pricing, log result
- [ ] T3.3 `rlm_create_orders_from_quote` — order creation as task
- [ ] T3.4 Monitor active billing schedules (`rlm_get_billing_schedules`)
- [ ] T3.5 Alert on failed invoice runs -> create critical task
- [ ] T3.6 Revenue metrics dashboard widget (ARR, churn, renewals)

### 🔲 T4 — Apex Log Analysis
- [ ] T4.1 `GET /api/sf/apex-logs` — fetch recent debug logs via `rlm_get_debug_logs`
- [ ] T4.2 Trigger sfrc-apex-log-analysis skill on log file
- [ ] T4.3 Surface RCA findings as LoopEngineering tasks with priority
- [ ] T4.4 Link log entry -> source Apex class:line in notes
- [ ] T4.5 Recurring scan: check for new error logs every 15min

### 🔲 T5 — Org Health & Deployment
- [ ] T5.1 `agentforce_org_readiness_check` — scheduled daily task
- [ ] T5.2 `agentforce_deploy_bundle` — deployment as tracked loop
- [ ] T5.3 `agentforce_run_tests` — test run -> loop log entries
- [ ] T5.4 Deployment status timeline in dashboard
- [ ] T5.5 Alert on test failures -> create high-priority task

### 🔲 T6 — Salesforce Data Cloud
- [ ] T6.1 Monitor Data Cloud ingestion jobs as tasks
- [ ] T6.2 Alert on ingestion failures
- [ ] T6.3 Profile completeness metrics surfaced in overview

### 🔲 T7 — Multi-Cloud Dashboard Widget
- [ ] T7.1 Overview panel: show active SF orgs + cloud health
- [ ] T7.2 Per-cloud status: Revenue, Agentforce, Experience, Commerce, Service
- [ ] T7.3 Click-through to cloud-specific task list

## Acceptance Criteria
- All 12 SF MCP servers shown in MCP view with enable/disable
- Agentforce agents list loads and shows status
- Create task from Agentforce agent spec
- Apex log analysis result appears as task within 60s of log availability
- Org readiness check runs on demand, result visible in dashboard

## Dependencies
- PRD-01 (Tasks, Loops)
- Active Salesforce org with MCP servers running
- `salesforce-clouds-python`, `agentforce-python` MCPs healthy
- PRD-04 (Webhooks) for SF Platform Events ingress
