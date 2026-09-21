# YARD

Internal preview. Not for distribution.

![YARD Mixed-Fleet Control Plane Console](docs/images/01_overview_main.png)

YARD is a mixed-fleet control plane for work that already happens in the building:

- **Cursor** builds the app and opens the PR.
- **Grok** ships the tagged build (canary, promote, rollback).
- **A local LLM** reads logs and heartbeats. No egress. No code. No deploy.

Humans remain product owners. Scrum-master agents cap WIP. Each domain is an agile crew with an assigned runtime.

## Surface

Open `index.html`. Tokyo Night. Keyboard first.

![The Yard - Kanban Multi-Fleet Board](docs/images/02_the_yard_board.png)

| key | action |
|---|---|
| `1–7` | views |
| `/` | filter |
| `j` `k` | move card |
| `return` | open detail |
| `esc` | close / dismiss |

## Views

1. **overview:** Fleet summary, agent roster, pipeline flow, and anomaly alerts.
2. **the yard:** 5-column Kanban board (Spec & Brief, Cursor Build, Golden Eval, Grok Ship, Watch & Accept).
3. **crews:** Domain teams, human POs, scrum-master agents, and per-crew WIP caps.
4. **cursor build:** Builder fleet tracking, branch references, PR status, token spend, and golden evals.
5. **grok ship:** Image tags, commit SHAs, canary traffic allocation, and rollback targets.
6. **local watch:** On-premise zero-egress telemetry, heartbeat intervals, tool loop detection, and goal drift.
7. **signals:** Real-time stream of detector warnings, budget overrun alarms, and soak notifications.

## Where Agents Are Identified in the Console

| Display Location | Identified Agents & Models | Context & Purpose |
|---|---|---|
| **Top Fleet Roster Bar** | `Cursor Cloud (bc-709a / gpt-5.6-sol)`, `xAI Grok (grok-4.6)`, `Local Watcher (Ollama / Qwen 2.5 Coder 14B)` | High-level fleet capabilities and active agent roster. |
| **Hero Metric Cards (View 1)** | `Cursor Cloud & Sonnet 5`, `xAI Grok Release Agent`, `Local LLM (Qwen 2.5 Coder 14B)` | Real-time ownership of in-flight stories, canaries, and alerts. |
| **Kanban Card Badges (View 2)** | `Cursor` (Blue), `Grok` (Purple), `Local` (Green) | At-a-glance runtime delegation on the board. |
| **Card Detail Drawer (`return`)** | Full Model Spec & Agent ID (e.g. `Cursor Cloud Agent bc-709a / gpt-5.6-sol`) | Forensic execution telemetry, tool signature loops, token overruns. |
| **Crews Matrix (View 3)** | `agent-scrum-core`, `agent-scrum-release`, `agent-scrum-watch`, `agent-scrum-omarchy` | Scrum-master agents capping WIP per functional domain. |
| **Cursor Build Table (View 4)** | `Cursor Cloud (bc-709a / gpt-5.6-sol)`, `Cursor Local (Sonnet 5)`, `gemini-3.8-flash` | Granular builder model attribution per branch & PR. |
| **Local Watch Table (View 6)** | `Ollama / Qwen 2.5 Coder 14B`, `llama.cpp / DeepSeek R1 14B`, `Mistral NeMo` | Zero-egress local observer models watching heartbeats. |
| **Persistent Footer Status Bar** | `Cursor Cloud Agent: Active`, `Grok Release Agent: Canary 10%`, `Local Watcher: 1 Alert` | Always-visible agent health LEDs across all views. |

## What this is not

Not a waitlist. Not a model vendor. Not a replacement for Cursor, Grok, or the box that runs the local model. It is the board those three report to.

## Status

Stealth preview. Contracts and detector rules are documented in `docs/ARCHITECTURE.md`.

## Documentation & Architecture

- **C4 Architecture & Pipeline Flow:** [`docs/C4-ARCHITECTURE.md`](docs/C4-ARCHITECTURE.md) (Context, Containers, Components, Pipeline Flow)
- **AI Tools Integration Matrix:** [`docs/AI-INTEGRATIONS.md`](docs/AI-INTEGRATIONS.md) (Cursor, Grok, Local LLMs, Claude Code, MCP servers)
- **Omarchy Shell Plugin Plan:** [`docs/OMARCHY-PLUGIN-PLAN.md`](docs/OMARCHY-PLUGIN-PLAN.md) (Quattro bar widget & Quickshell HUD)
- **OpenSpec & Gherkin Specs:** [`openspec/project.md`](openspec/project.md) and [`openspec/features/`](openspec/features/)
- **Native Omarchy Plugin:** [`plugin/omarchy/`](plugin/omarchy/) (`manifest.json`, `BarWidget.qml`, `Panel.qml`, `bin/yard-status`)
