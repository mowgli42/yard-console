# YARD C4 Architecture Documentation

YARD is a mixed-fleet control plane for multi-agent software engineering and continuous delivery. It enforces strict separation of concerns across runtime boundaries (Cursor for build/PR creation, Grok for ship/tag/canary/promote/rollback, Local LLMs for log/heartbeat watch, and Humans for Product Ownership and Sprint Governance).

---

## C4 Model — Level 1: System Context Diagram

The System Context diagram illustrates the actors (Human Product Owners, Platform Engineers) and the external AI systems/runtimes that interact with YARD.

```mermaid
C4Context
    title System Context Diagram for YARD Mixed-Fleet Control Plane

    Person(po, "Product Owner / Human Engineer", "Defines sprint goals, accepts PRs, authorizes promotions or overrides.")
    Person(operator, "Platform Operator", "Monitors fleet health, reviews anomalies, manages runtime budgets.")

    System(yard, "YARD Control Plane", "Central mixed-fleet board & coordination layer. Tracks crews, enforces WIP caps, manages story lifecycle across runtimes, and processes watch telemetry.")

    System_Ext(cursor_agent, "Cursor Cloud/Local Agent", "Authoring runtime. Implements stories, runs lint/unit tests, opens GitHub PRs, updates domain packs.")
    System_Ext(grok_agent, "xAI Grok Agent", "Release runtime. Ships tagged builds, executes canary deployments, monitors release metrics, drives promote or rollback.")
    System_Ext(local_llm, "Local LLM Watcher (Ollama / vLLM / llama.cpp)", "Telemetry runtime. Classifies journald, CI logs, token consumption curves, and heartbeats on-premise without egress.")
    System_Ext(vcs_ci, "GitHub & CI Infrastructure", "Stores git repositories, PRs, actions workflows, and container artifacts.")
    System_Ext(omarchy, "Omarchy Desktop Environment", "Host Arch Linux + Hyprland desktop displaying status bar widgets and native Quickshell HUD panels.")

    Rel(po, yard, "Views board, defines domain scope, accepts deliverables", "HTTPS / Web / Quickshell HUD")
    Rel(operator, yard, "Configures detector thresholds & WIP limits", "CLI / Web HUD")
    Rel(cursor_agent, yard, "Reports build state, story progress, token burn, PR metadata", "REST API / Webhook / Agent CLI")
    Rel(grok_agent, yard, "Reports deployment state, canary health, promote/rollback decisions", "REST API / Webhook")
    Rel(local_llm, yard, "Submits anomaly alerts, detector cards, heartbeat states", "Local Unix Domain Socket / REST")
    Rel(yard, vcs_ci, "Monitors PR states, git tags, and release workflow dispatches", "GitHub REST/GraphQL API")
    Rel(yard, omarchy, "Publishes status updates, active alerts, and quick actions to status bar", "Omarchy Shell Plugin / IPC")
```

---

## C4 Model — Level 2: Container Diagram

The Container diagram breaks YARD into its high-level runtime components: the Web Console, the Omarchy Shell Plugin, the Core API/Event Broker, and the Storage/State stores.

```mermaid
C4Container
    title Container Diagram for YARD Platform

    Person(human, "Human Operator / PO", "Uses desktop HUD or browser console")

    Container_Boundary(yard_boundary, "YARD System") {
        Container(web_ui, "YARD Web Console", "HTML5 / Vanilla JS / Tokyo Night CSS", "Keyboard-first single page interface (`1-7` views, `j/k` navigation, `/` search, real-time telemetry).")
        Container(omarchy_plugin, "Omarchy Shell Plugin", "QML / Quickshell / Python helper", "Native desktop bar widget and popup panel in Omarchy Hyprland environment.")
        Container(api_gateway, "YARD Core Dispatcher / Hub", "FastAPI / Python 3.12+ or Go", "Coordinates crews, tracks WIP limits, manages lifecycle state transitions, validates detector inputs.")
        Container(detector_engine, "Local Anomaly Detector Engine", "Python / Async IO", "Watches agent execution logs, heartbeat ticks, token curves, and flags drift locally.")
        ContainerDb(state_store, "YARD State Store & Ledger", "SQLite / JSONL Append-only log", "Durable storage for crew manifests, stories, cards, detector events, and audit logs.")
    }

    System_Ext(cursor_ext, "Cursor Agent", "Cloud agent or local editor session")
    System_Ext(grok_ext, "Grok Release Agent", "Release pipeline execution agent")
    System_Ext(local_llm_ext, "Local LLM Backend", "Ollama / llama.cpp / Antigravity")
    System_Ext(github_ext, "GitHub Platform", "PRs, Repos, Actions")

    Rel(human, web_ui, "Interacts keyboard-first via browser", "HTTP/WS")
    Rel(human, omarchy_plugin, "Clicks bar icon, hotkey panel", "Wayland / LayerShell")
    Rel(omarchy_plugin, api_gateway, "Queries status, triggers actions, syncs alerts", "Local REST / IPC")
    Rel(web_ui, api_gateway, "Fetches board state, posts human approvals", "REST / SSE / WebSockets")
    Rel(api_gateway, state_store, "Reads and writes crew/card states and audit ledger", "SQL / File IO")
    Rel(detector_engine, state_store, "Appends detector trigger cards and heartbeat metrics", "Direct DB / Internal API")
    Rel(detector_engine, local_llm_ext, "Infers log classification, anomaly summary", "OpenAI-compatible HTTP API")
    Rel(cursor_ext, api_gateway, "Registers story in-flight, reports token usage", "REST API")
    Rel(grok_ext, api_gateway, "Sends canary evaluation results and promotion tags", "REST API")
    Rel(api_gateway, github_ext, "Polls/hooks PR and release events", "HTTPS API")
```

---

## C4 Model — Level 3: Component Diagram (Core Dispatcher / Hub)

Detailed internal component breakdown of the YARD Dispatcher and local detector engine.

```mermaid
C4Component
    title Component Diagram for YARD Dispatcher & Detector Subsystems

    Container_Boundary(dispatcher_boundary, "YARD Dispatcher Service") {
        Component(rest_routes, "REST / SSE Controllers", "FastAPI Routes", "Exposes `/api/v1/crews`, `/cards`, `/detectors`, `/signals`, `/telemetry`.")
        Component(crew_manager, "Crew & WIP Manager", "Domain Logic", "Enforces strict per-crew WIP caps, validates scrum master assignments, tracks cycle times.")
        Component(lifecycle_fsm, "Story Lifecycle FSM", "State Machine", "Enforces transitions: Spec -> Cursor PR -> Lint/Eval -> Grok Canary -> Grok Promote -> Local Watch -> Accepted.")
        Component(watch_aggregator, "Watch Signal Aggregator", "Async Collector", "Collects heartbeats, token rates, and detector flags; raises cards on the board.")
        Component(event_ledger, "Audit & Event Ledger", "Append-only storage", "Guarantees immutable audit trail of agent actions, operator overrides, and state changes.")
        Component(omarchy_bridge, "Omarchy Plugin Bridge", "IPC / CLI Interface", "Emits quickshell notifications, formats desktop HUD state, handles bar button triggers.")
    }

    Container_Boundary(detector_boundary, "Local Watch Engine") {
        Component(heartbeat_mon, "Heartbeat Monitor", "Worker", "Detects stale agents (>2x mean step interval) and halts zombie loops.")
        Component(token_guard, "Token Budget Guard", "Worker", "Flags 2x budget overrun; triggers hard-stop signal at 4x.")
        Component(loop_detector, "Signature & Loop Detector", "Worker", "Flags repeated identical tool call signatures (>= 3 repetitions).")
        Component(drift_evaluator, "Goal Drift Evaluator", "Local Model Client", "Evaluates embedding/semantic similarity between sprint brief and agent diff.")
    }

    Rel(rest_routes, crew_manager, "Dispatches crew commands")
    Rel(rest_routes, lifecycle_fsm, "Processes story stage transitions")
    Rel(watch_aggregator, lifecycle_fsm, "Attaches detector warnings to active stories")
    Rel(crew_manager, event_ledger, "Appends WIP & crew events")
    Rel(lifecycle_fsm, event_ledger, "Appends lifecycle transition events")
    Rel(rest_routes, omarchy_bridge, "Pushes desktop events and quick actions")
    Rel(heartbeat_mon, watch_aggregator, "Sends HeartbeatStaleAlert")
    Rel(token_guard, watch_aggregator, "Sends TokenBudgetThresholdAlert")
    Rel(loop_detector, watch_aggregator, "Sends ToolLoopDetectedAlert")
    Rel(drift_evaluator, watch_aggregator, "Sends GoalDriftDetectedAlert")
```

---

## C4 Model — Level 4: Code & Data Flow Diagram (The Three-Runtime Pipeline)

This sequence illustrates the end-to-end lifecycle of a story across the three runtime boundaries:

```mermaid
sequenceDiagram
    autonumber
    actor PO as Human Product Owner
    participant YARD as YARD Dispatcher
    participant Cursor as Cursor Runtime
    participant CI as GitHub CI & Registry
    participant Grok as Grok Runtime
    participant LocalWatch as Local LLM Watcher
    participant Omarchy as Omarchy Desktop HUD

    Note over PO,Cursor: 1. Sprint & Build Phase
    PO->>YARD: Assigns story to Crew (e.g. Core Engine)
    YARD->>YARD: Checks Crew WIP Cap (Permit / Deny)
    YARD->>Cursor: Dispatches story task context & Domain Pack
    activate Cursor
    Cursor->>Cursor: Writes implementation, unit tests, Gherkin features
    Cursor->>CI: Pushes branch & opens Pull Request
    Cursor->>YARD: Reports token burn & PR #123 opened
    deactivate Cursor

    Note over Cursor,CI: 2. Verification & Tagging
    CI->>CI: Runs lint + cheap eval subset
    CI-->>YARD: Eval green, merge approved
    YARD->>CI: Creates image tag (SHA + prompt hash + eval snapshot)

    Note over Grok,CI: 3. Release & Canary Phase
    YARD->>Grok: Dispatches Canary Deployment Task
    activate Grok
    Grok->>CI: Triggers canary deploy to staging/edge
    Grok->>Grok: Evaluates canary error rates & operator notes
    alt Canary Successful
        Grok->>CI: Promotes tag to production
        Grok->>YARD: Reports Promote Completed (Release Note generated)
    else Canary Fails or Degraded
        Grok->>CI: Issues Rollback to previous known good tag
        Grok->>YARD: Reports Rollback Triggered with incident summary
    end
    deactivate Grok

    Note over LocalWatch,Omarchy: 4. Local Watch & Observability
    LocalWatch->>LocalWatch: Streams journald/CI logs, parses heartbeat pulses
    LocalWatch->>LocalWatch: Runs detectors (Zero-error high token, tool loop, goal drift)
    alt Anomaly Detected
        LocalWatch->>YARD: Raises Alert Card on YARD Board (No auto-fix, no code mutation)
        YARD->>Omarchy: Alerts desktop via Omarchy Bar Badge & OSD notification
        Omarchy-->>PO: Visual indicator on bar ("󱚣 1 Alert")
    else Normal Telemetry
        LocalWatch->>YARD: Quiet status heartbeat
    end

    Note over PO,YARD: 5. Final Acceptance
    PO->>YARD: Verifies deliverables on board; accepts story
    YARD->>YARD: Increments Crew Completed, releases WIP slot
```

---

## Architecture Decision Records (ADRs) Summary

| ADR ID | Decision | Key Rationale |
|---|---|---|
| **ADR-001** | Strict Three-Runtime Isolation | Cursor should not touch prod cluster/secrets; Grok should not reopen brief; Local LLM triage stays on-premise without cloud egress cost or privacy exposure. |
| **ADR-002** | Per-Crew WIP Caps over Global WIP | Different functional crews operate at different cadences and token budgets. Capping per crew prevents starvation and limits blast radius of runaway subagent loops. |
| **ADR-003** | Local-First Passive Detectors | Detectors identify anomalies and raise cards on the board; they NEVER unilaterally mutate code or force deploys. The human PO remains in control. |
| **ADR-004** | Dual Interface: Web Console & Native Omarchy Plugin | Browser provides deep multi-panel board navigation; Omarchy native QML plugin provides at-a-glance status bar health and desktop notification integration. |
