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
| `b` | openspec baseball card |
| `[` `]` | prev / next bead |
| `/` | filter |
| `j` `k` | move card |
| `return` | open detail |
| `esc` | close / dismiss |

## OpenSpec & Beads Baseball Card Interface

The console integrates directly with **OpenSpec** capability definitions and **Beads** (`.beads/issues.jsonl`) linear progress pipelines:

![OpenSpec & Beads Baseball Card](docs/images/07_baseball_card_openspec.png)

- **Persistent Current Bead Ribbon:** Shows the project selector and the active 3-step bead pipeline: `[Last Completed]` ➜ `[In Work (Pulse)]` ➜ `[Next Queued]`.
- **Baseball Card Modal (`b`):**
  - **Player & Engine Stats:** Assigned agent, model (`gemini-3.8-flash`, `gpt-5.6-sol`, `sonnet-5`), token burn percentage, and heartbeat telemetry.
  - **OpenSpec Definition:** Linked spec document, capability purpose statement, and formal `SHALL` requirement clause.
  - **Executable Gherkin:** Syntax-highlighted `GIVEN` / `WHEN` / `THEN` scenario verifying the bead's acceptance criteria.
  - **Connected Trio Stepper:** Click any pill or press `[` / `]` to step between the last completed, current in-work, and next bead.

## Agent Crews Across Projects

The **Crews View (`3`)** manages autonomous agile crews working concurrently across distinct repositories, each assigned a dedicated scrum-master agent and runtime budget:

![Agent Crews Working Distributed Projects](docs/images/04_crews_wip.png)

## Views

1. **overview:** Fleet summary, agent roster, pipeline flow, and anomaly alerts.
2. **the yard:** 5-column Kanban board (Spec & Brief, Cursor Build, Golden Eval, Grok Ship, Watch & Accept).
3. **crews:** Multi-project domain teams (`yard-console`, `bookish-train`, `schwerpunkt`, `fuzzy-reconciler`, `omarchy-quattro`), POs, scrum-master agents, and per-crew WIP caps.
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
| **Crews Matrix (View 3)** | `agent-scrum-core`, `agent-scrum-backup`, `agent-scrum-ooda`, `agent-scrum-reconcile`, `agent-scrum-release`, `agent-scrum-watch`, `agent-scrum-omarchy` | Scrum-master agents capping WIP across 7 distributed repositories. |
| **Cursor Build Table (View 4)** | `Cursor Cloud (bc-709a / gpt-5.6-sol)`, `Cursor Local (Sonnet 5)`, `gemini-3.8-flash`, `composer-2.5` | Granular builder model attribution per branch, repo & PR. |
| **Local Watch Table (View 6)** | `Ollama / Qwen 2.5 Coder 14B`, `llama.cpp / DeepSeek R1 14B`, `Mistral NeMo` | Zero-egress local observer models watching heartbeats across repos. |
| **Beads Active Ribbon (Header)** | Current in-work bead ID (`schwerpunkt-i0i.3.1`, `yard-042`), assigned agent, live pulse | Continuous task attribution across multiple project repositories. |
| **OpenSpec Baseball Card (`b`)** | Assigned agent (`Cursor Cloud bc-709a`), engine model (`gemini-3.8-flash`), token burn | Glanceable athlete-card stats, formal `SHALL` spec requirement, and Gherkin BDD scenario. |
| **Persistent Footer Status Bar** | `Cursor Cloud Agent: Active`, `Grok Release Agent: Canary 10%`, `Local Watcher: 1 Alert` | Always-visible agent health LEDs across all views. |

## Live Operation & Repository Management

The console is fully functional and monitors real repository state:
1. **Local State Daemon (`yard-sync`):** Continuously scans `.beads/issues.jsonl` and `openspec/specs/` across all configured repositories, formatting unified status JSON into `~/.local/state/yard/status.json` and `data/status.json`.
2. **Web Live Polling:** The console polls `data/status.json` and updates the active bead ribbon, project selector, and baseball cards in real time without refreshing.
3. **Omarchy Quickshell Plugin:** The status script (`plugin/omarchy/bin/yard-status`) reads this same state, updating the Linux desktop bar and HUD.

### Starting the Live Console

Run the bundled launcher:
```bash
./scripts/yard-start.sh
```
This runs the background `yard-sync` daemon and serves `http://localhost:8000`.

### Adding an Existing Repository

To link an existing workspace repository to the YARD console:
```bash
./scripts/yard-add-repo.py /path/to/my-repo \
  --crew "Backend Core" \
  --agent "Cursor Cloud Agent (bc-709a)" \
  --model "gemini-3.8-flash"
```
The script will:
- Auto-detect git origin remote slug or directory name.
- Verify or initialize `.beads/` and `openspec/`.
- Register the repo in `config/repos.json`.
- Trigger an immediate sync so it appears in the console project selector.

### Adding a New Repository from Scratch

To create and scaffold a brand new repository with Beads issue tracking and OpenSpec living specs:
```bash
./scripts/yard-add-repo.py /home/tprettol/repo/new-service \
  --new \
  --slug "mowgli42/new-service" \
  --crew "Telemetry Stream" \
  --init-beads \
  --init-openspec
```
This creates:
- Initialized Git repository (`git init`).
- `.beads/config.yaml` and starter issue in `.beads/issues.jsonl`.
- `openspec/project.md` and initial capability contract in `openspec/specs/core-capability/spec.md`.
- Immediate registration in YARD fleet config.

---

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
