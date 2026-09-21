# YARD — Project Context & Specification Index

## Purpose

YARD is a mixed-fleet control plane designed to orchestrate agentic software engineering and delivery workflows across strictly segregated runtimes:
- **Cursor:** Builds applications, implements stories, writes tests, opens GitHub Pull Requests.
- **Grok:** Manages deployment lifecycle, tags releases, conducts canary rolls, executes promote or rollback operations.
- **Local LLM:** Observes journald and CI logs, tracks token trajectories, monitors agent heartbeats with zero external egress.
- **Humans:** Remain Product Owners, define domain packs, set WIP caps, and give final acceptance.

## System Interfaces

1. **Standalone Web Console (`index.html`):**
   - Palette: Tokyo Night (`#1a1b26`, `#24283b`, `#7aa2f7`, `#bb9af7`, `#7dcfff`, `#f7768e`, `#9ece6a`, `#e0af68`).
   - Keyboard-first interaction model:
     - `1` through `7` for view switching.
     - `/` for instant filtering.
     - `j` and `k` for card/item navigation.
     - `return` to open details.
     - `esc` to dismiss dialogs/close views.
2. **Omarchy Desktop Shell Plugin (`omarchy.yard-console`):**
   - Bar widget with alert badges and fleet state.
   - Quickshell popup panel showing crew WIP, active canaries, and local watch detector warnings.
   - IPC integration via `omarchy-shell` and desktop notifications.

## Specifications Index

| Capability | Spec Path | Description |
|---|---|---|
| Runtime Boundary & Contracts | `openspec/specs/runtime-boundaries/spec.md` | Strict rules separating Cursor, Grok, and Local LLM runtimes. |
| Crew & WIP Cap Management | `openspec/specs/crew-management/spec.md` | Scrum-master agent rules, per-crew WIP caps, cycle time metrics. |
| Local Anomaly Detectors | `openspec/specs/local-detectors/spec.md` | Passive anomaly detection (token overrun, goal drift, tool loops). |
| Web Console UI & Navigation | `openspec/specs/web-console/spec.md` | Keyboard-first Tokyo Night interface requirements and hotkeys. |
| Omarchy Shell Plugin | `openspec/specs/omarchy-plugin/spec.md` | Native Quickshell bar widget, popup HUD, IPC targets. |
| AI Tools Integration Matrix | `openspec/specs/ai-integrations/spec.md` | Protocols, MCP bridges, and telemetry pipelines for external agent tools. |
| Beads & OpenSpec Interface | `openspec/specs/beads-openspec-interface/spec.md` | Beads issue tracking, active bead ticker, and OpenSpec Baseball Card modal. |

## Verification Framework

- OpenSpec specs define formal **SHALL** requirements.
- Gherkin feature files mirror specifications in `openspec/features/*.feature` for automated testing via `pytest-bdd` or Cucumber.
- Active integration test systems configured in YARD fleet:
  - `mowgli42/appliance-keeper`: Local-first household appliance & filter schedule tracker.
  - `mowgli42/fluffy-spoon`: XML catalog and recipe-box static generation engine.
  - `mowgli42/OnePage-PM`: One-page project management (OPPM) matrix with FastAPI backend and Svelte frontend.
