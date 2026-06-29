# PRD-06 — Salesforce Accessibility

*Status: Planned | Last updated: 2026-06-29*

## Goal
Ensure LoopEngineering dashboard meets WCAG 2.2 AA. Add Salesforce LWC accessibility audit tooling. Surface a11y issues as LoopEngineering tasks with automated remediation loops.

## User Stories
- As a developer, I want the LoopEngineering dashboard to be keyboard-navigable
- As a Salesforce developer, I want to run an a11y audit on my LWC components and get issues as tasks
- As a developer, I want color contrast ratios shown per component
- As a developer, I want screen reader-friendly ARIA labels on all dashboard elements

## Tasks & Subtasks

### 🔲 T1 — Dashboard WCAG 2.2 AA Compliance
- [ ] T1.1 Keyboard navigation: all interactive elements reachable via Tab
- [ ] T1.2 Focus ring visible on all focusable elements (min 3px contrast)
- [ ] T1.3 Color contrast: all text/bg pairs >= 4.5:1 (normal), >= 3:1 (large)
- [ ] T1.4 ARIA roles: `role="main"`, `role="navigation"`, `role="complementary"`
- [ ] T1.5 Skip-to-main-content link at top of page
- [ ] T1.6 Modal: trap focus, `aria-modal="true"`, `aria-labelledby`
- [ ] T1.7 Status badges: not color-only — include text label
- [ ] T1.8 Toast: `role="alert"`, `aria-live="polite"`
- [ ] T1.9 Tables: proper `<thead>`, `scope="col"`, `aria-sort` on sortable cols
- [ ] T1.10 Toggle switches: `role="switch"`, `aria-checked`
- [ ] T1.11 Form inputs: all have `<label>` or `aria-label`
- [ ] T1.12 Icon-only buttons: `aria-label` describing action
- [ ] T1.13 Reduced motion: `@media (prefers-reduced-motion)` on all animations

### 🔲 T2 — Keyboard Shortcuts
- [ ] T2.1 `n` — new task modal
- [ ] T2.2 `/` — global search
- [ ] T2.3 `g p` — go to projects
- [ ] T2.4 `Escape` — close modal
- [ ] T2.5 `?` — show keyboard shortcuts overlay
- [ ] T2.6 Arrow keys — navigate task table rows

### 🔲 T3 — Salesforce LWC A11y Audit
- [ ] T3.1 `GET /api/a11y/audit?project=` — run axe-core on LWC components
- [ ] T3.2 Parse axe-core results, create LoopEngineering tasks per violation
- [ ] T3.3 Priority mapping: critical->critical, serious->high, moderate->medium
- [ ] T3.4 Task tag: `a11y`, `wcag-{rule-id}`, `lwc`
- [ ] T3.5 Auto-create loop: "Fix {violation} in {component}"
- [ ] T3.6 Dashboard widget: a11y score per Salesforce project (0-100)

### 🔲 T4 — SLDS Accessibility Patterns
- [ ] T4.1 Audit all dashboard components against SLDS component blueprint a11y guidelines
- [ ] T4.2 Validate: `lightning-button`, `lightning-modal`, `lightning-datatable` patterns
- [ ] T4.3 Report: components using non-SLDS patterns with recommended fix
- [ ] T4.4 Auto-loop: generate fix code for each non-compliant component

### 🔲 T5 — Color & Contrast Tools
- [ ] T5.1 Settings > Theme: show contrast ratio for current theme colors
- [ ] T5.2 Warn if any theme token pair falls below 4.5:1
- [ ] T5.3 Light theme colors validated to WCAG AA already
- [ ] T5.4 High-contrast mode: `@media (prefers-contrast: high)` overrides

### 🔲 T6 — Screen Reader Testing
- [ ] T6.1 VoiceOver (macOS) smoke test: all views navigable
- [ ] T6.2 NVDA (Windows) smoke test (via VM)
- [ ] T6.3 Automated: integrate with playwright-axe for CI
- [ ] T6.4 Test checklist per view: overview, tasks, loops, MCP, settings

## Acceptance Criteria
- axe-core scan: 0 critical, 0 serious violations on dashboard
- All modals trap focus correctly
- Skip-to-content link visible on focus
- Keyboard shortcut `n` opens new task modal
- Color contrast ratio >= 4.5:1 for all text elements in both themes
- LWC audit creates tasks for each axe violation found

## Dependencies
- PRD-01 (Dashboard complete)
- `axe-core` npm package for audit runner
- Salesforce project with LWC components (PRD-05)

## References
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- SLDS Accessibility: https://www.lightningdesignsystem.com/accessibility/overview/
- axe-core: https://github.com/dequelabs/axe-core
- Salesforce Accessibility: https://developer.salesforce.com/docs/atlas.en-us.lightning.meta/lightning/accessibility_intro.htm
