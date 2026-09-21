# YARD Omarchy Plugin — Build Plan & Architecture

This document outlines the blueprint and implementation plan for packaging the YARD control plane as a native Omarchy desktop plugin (`org.yard.console`), adhering to the Omarchy Quattro shell specification.

---

## 1. Plugin Goals & System Integration

1. **At-a-Glance Fleet Awareness:**
   - Display active fleet status (Cursor build in-flight, Grok canary percentage, and Local Watch detector alarms) directly on the Hyprland status bar.
   - Dynamic glyphs and alarm states:
     - `󱚣` (Base glyph)
     - Normal state: Clean foreground color.
     - Warning state (Canary running or 2x token pace): Yellow accent (`#e0af68`).
     - Urgent alarm state (4x token overrun or tool loop detected): Pulsing red accent (`#f7768e`).

2. **Native Quickshell Keyboard Panel:**
   - Single-click or keybind popout panel running natively inside `omarchy-shell`.
   - Real-time status cards:
     - Active Domain Crews and current WIP vs Cap.
     - Cursor PR in-flight with token burn percentage meters.
     - Grok Canary health and rollback status.
     - Local Watch detector warnings with quick "Acknowledge" and "Inspect" actions.
   - Quick launch button: Launches the full Tokyo Night web console (`index.html`) in the default browser (`omarchy launch browser`).

3. **Zero-Overhead Local Daemon & State Watcher:**
   - Reads state from `~/.local/state/yard/status.json`.
   - Updated periodically by local agent collectors (`yard-status-sync` CLI / cron / file watcher).
   - Zero external cloud polling inside the UI rendering thread.

---

## 2. Directory Structure (Self-Contained Hybrid Architecture)

```
yard-console/
├── manifest.json              # Omarchy shell plugin manifest (schemaVersion 1, id: org.yard.console)
├── BarWidget.qml              # Status bar slot button & badge icon
├── Panel.qml                  # Quickshell popout keyboard HUD
├── YardModel.js               # Parser & formatting helper for YARD status JSON
├── bin/
│   └── yard-status            # CLI status query & JSON emitter helper
├── tests/
│   └── test_plugin.py         # Automated verification test suite
├── index.html                 # Full Tokyo Night web console & Baseball Card interface
├── scripts/
│   ├── yard-sync.py           # Background Beads/OpenSpec/Git telemetry collector
│   ├── yard-add-repo.py       # New/existing repository onboarding tool
│   ├── yard-start.sh          # Live environment launcher
│   └── generate-screenshots.py # Headless browser screenshot generator
├── openspec/                  # Living capability specifications & Gherkin scenarios
└── docs/                      # Architectural blueprints, C4 models & diagrams
```

---

## 3. Data Contract (`status.json`)

The plugin monitors `~/.local/state/yard/status.json`:

```json
{
  "version": 1,
  "updatedAt": "2026-09-21T15:30:11Z",
  "fleet": {
    "activeCrews": 7,
    "maxCrews": 12,
    "alarming": false,
    "alarmCount": 0
  },
  "cursor": {
    "storiesCount": 3,
    "tokenBurn": 142000,
    "activePr": "#42 Tokyo Night sync",
    "status": "nominal"
  },
  "grok": {
    "canaryTag": "v1.4.2-rc1",
    "canaryPercent": 10,
    "healthScore": 99.8,
    "status": "staging"
  },
  "localWatch": {
    "zeroEgress": true,
    "alerts": []
  },
  "beads": {
    "activeProject": "mowgli42/appliance-keeper",
    "completed": {
      "id": "appliance-keeper-rnc",
      "title": "Apply AGENTS.md schema",
      "status": "closed"
    },
    "inWork": {
      "id": "appliance-keeper-o4o",
      "title": "Phase 1: filter mark-changed UX polish",
      "status": "in_progress",
      "agent": "Claude Sonnet (Claude-3.7)",
      "model": "claude-sonnet-5-thinking-high",
      "agentStatus": "active",
      "specPath": "openspec/specs/filter-schedule/spec.md"
    },
    "next": {
      "id": "appliance-keeper-5e0",
      "title": "Phase 1: add warranty/service forms",
      "status": "open"
    }
  },
  "beadsSystem": {
    "installed": false,
    "binaryPath": "",
    "version": "not installed",
    "doltInstalled": false,
    "adoptedRepos": 6,
    "totalRepos": 7,
    "adoptionPercent": 85,
    "totalBeads": 119,
    "closedBeads": 64,
    "pendingBeads": 54
  },
  "allProjects": {
    "mowgli42/appliance-keeper": {
      "beadsAdoption": { "adopted": true, "adoptionScore": 100, "backend": "dolt" },
      "gitActivity": { "branch": "main", "isClean": true },
      "githubPrs": { "openPrs": [{ "number": 6, "title": "Add appliance: filter info" }] }
    }
  }
}
```

---

## 4. Phased Implementation Roadmap

- **Phase 1 (Complete):** Core QML manifests and UI components validated at the repository root for direct `omarchy plugin add` compatibility.
- **Phase 2 (Complete):** CLI helper script `yard-status` providing JSON bridge to Quickshell `Process` or `FileView`, with Beads ecosystem, Git activity, and agent state metrics.
- **Phase 3 (Complete):** Beads adoption & GitHub activity HUD integration inside `Panel.qml` with dynamic tooltip status in `BarWidget.qml`.
- **Phase 4:** Desktop notifications dispatch via `omarchy-shell` notification daemon when an urgent local watch card is raised.
