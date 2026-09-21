# YARD Omarchy Plugin — Build Plan & Architecture

This document outlines the blueprint and implementation plan for packaging the YARD control plane as a native Omarchy desktop plugin (`omarchy.yard-console`), adhering to the Omarchy Quattro shell specification.

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

## 2. Directory Structure

```
plugin/omarchy/
├── manifest.json              # Omarchy shell plugin manifest
├── BarWidget.qml              # Status bar slot button & badge icon
├── Panel.qml                  # Quickshell popout keyboard HUD
├── YardModel.js               # Parser & formatting helper for YARD status JSON
├── bin/
│   └── yard-status            # CLI status query & JSON emitter helper
└── assets/
    ├── yard.svg               # YARD brand icon
    └── yard-alert.svg         # YARD alert icon
```

---

## 3. Data Contract (`status.json`)

The plugin monitors `~/.local/state/yard/status.json`:

```json
{
  "version": 1,
  "updatedAt": "2026-09-20T21:00:00Z",
  "fleet": {
    "activeCrews": 4,
    "maxCrews": 8,
    "alarming": true,
    "alarmCount": 1
  },
  "cursor": {
    "storiesCount": 3,
    "tokenBurn": 124000,
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
    "alerts": [
      {
        "id": "SIG-901",
        "storyId": "CORE-104",
        "type": "RepeatedSignature",
        "severity": "urgent",
        "message": "pytest repeated 3 consecutive times without code edits"
      }
    ]
  }
}
```

---

## 4. Phased Implementation Roadmap

- **Phase 1 (Complete):** Core QML manifests and UI components written and validated in `plugin/omarchy/`.
- **Phase 2:** CLI helper script `yard-status` providing JSON bridge to Quickshell `Process` or `FileView`.
- **Phase 3:** User configuration hook in `~/.config/omarchy/shell.json` allowing user to place `omarchy.yard-console` into the status bar.
- **Phase 4:** Desktop notifications dispatch via `omarchy-shell` notification daemon when an urgent local watch card is raised.
