# OpenSpec & Beads Issue Tracking Interface Specification

## Purpose

Define the interface connecting YARD to OpenSpec project definitions and Beads issue tracking (`.beads/issues.jsonl`). YARD acts as the mixed-fleet visual HUD that maps running agent tasks back to their formal OpenSpec architectural requirements and presents linear bead progress with a rich "Baseball Card" display.

## Requirements

### Requirement: Active Bead Progress Tracking

The YARD Console SHALL continuously identify and display the current active bead being worked across projects, highlighting the 3-step pipeline: the last completed bead, the currently in-work bead, and the next queued bead.

#### Scenario: Displaying current active bead in persistent console header
- **GIVEN** an active agent crew working on a project repository (e.g., `schwerpunkt` or `yard-console`)
- **WHEN** the YARD Web Console loads or updates
- **THEN** the console SHALL display a persistent Current Bead indicator pill showing:
  - Bead Issue ID (e.g. `schwerpunkt-i0i.3.1`)
  - Project repository name
  - Issue title
  - Assigned agent and model
  - Running elapsed time or pulse status
- **AND** clicking the Current Bead indicator or pressing shortcut `b` SHALL immediately open the Baseball Card modal

#### Scenario: Three-bead pipeline trio visibility
- **GIVEN** a project with Beads tracking enabled
- **WHEN** the operator views the Beads Pipeline Ribbon or Baseball Card
- **THEN** the interface SHALL render three interconnected beads in execution order:
  - **Last Completed Bead:** displaying issue ID, title, completion timestamp, and closure reason
  - **In-Work Bead:** highlighted with active pulse, token burn, agent model, and elapsed duration
  - **Next Bead:** displaying issue ID, title, priority, blockers/dependencies, and readiness status
- **AND** clicking either the last completed or next bead SHALL pivot the Baseball Card inspection to that bead

### Requirement: OpenSpec Baseball Card Representation

The YARD Console SHALL provide an interactive "Baseball Card" popover modal that marries Beads task metadata with formal OpenSpec architectural definitions and executable Gherkin scenarios.

#### Scenario: Front of card: OpenSpec capability and formal SHALL requirements
- **GIVEN** an open Baseball Card modal for an active or selected bead
- **WHEN** the card renders
- **THEN** it SHALL display the associated OpenSpec document path (e.g., `openspec/specs/orientation-layer/spec.md`)
- **AND** SHALL extract and display the Capability Purpose statement
- **AND** SHALL display the formal requirement text containing RFC-2119 `SHALL` clauses
- **AND** SHALL display the full executable Gherkin scenario (`GIVEN`, `WHEN`, `THEN`, `AND`) formatted in syntax-highlighted code blocks

#### Scenario: Card header and telemetry stats
- **GIVEN** the Baseball Card modal
- **WHEN** inspected by an operator or Product Owner
- **THEN** the card header SHALL present:
  - Card identification badge and project slug
  - Assigned runtime and agent ID
  - Underlying LLM / foundation model (e.g., `gemini-3.8-flash`, `claude-sonnet-5-thinking-high`, `grok-4.6`)
  - Live token burn progress bar against allocated budget
  - Anomaly status indicators from Local Watch detectors

#### Scenario: Stepping between beads via keyboard navigation
- **GIVEN** the Baseball Card modal is open
- **WHEN** the operator presses `[` (bracket left)
- **THEN** the view SHALL transition to the Last Completed bead in the pipeline
- **AND** WHEN the operator presses `]` (bracket right)
- **THEN** the view SHALL transition to the Next bead in the pipeline
- **AND** WHEN the operator presses `esc`
- **THEN** the Baseball Card modal SHALL close immediately
