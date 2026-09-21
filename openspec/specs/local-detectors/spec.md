# Local Anomaly Detectors Specification

## Purpose

Define the passive anomaly detector engine that monitors running agents and pipeline operations. Detectors run locally to flag pathological patterns, budget explosions, and stuck execution without unilaterally mutating source code or infrastructure.

## Requirements

### Requirement: Local-First Passive Alerting

The Local Watch runtime SHALL evaluate telemetry streams against detector heuristics and raise advisory cards on the YARD board without executing autonomous code edits or infrastructure mutations.

#### Scenario: Token budget 2x warning and 4x hard stop
- **GIVEN** a story running under the Cursor runtime with an estimated token budget of 50,000 tokens
- **WHEN** token consumption exceeds 100,000 tokens (2x budget threshold)
- **THEN** Local Watch SHALL raise a yellow advisory badge on the story card
- **AND** WHEN token consumption exceeds 200,000 tokens (4x hard stop threshold)
- **THEN** Local Watch SHALL trigger a hard-stop interrupt signal to pause the agent run
- **AND** notify the human Product Owner via desktop alert

#### Scenario: Repeated tool call signature detection
- **GIVEN** an active agent session executing tool calls
- **WHEN** the agent invokes the exact same tool signature with identical arguments 3 or more consecutive times
- **THEN** Local Watch SHALL detect a tool looping pattern
- **AND** raise a `ToolLoopDetected` warning card on the yard board
- **AND** flag the session for operator review

#### Scenario: Goal drift detection against sprint brief
- **GIVEN** a story with an approved sprint brief in `DOMAIN.md`
- **WHEN** the agent produces code diffs and file edits whose semantic similarity score against the brief falls below 0.60
- **THEN** Local Watch SHALL flag `GoalDriftDetected`
- **AND** display the drift score and mismatched diff files in the Signals view

#### Scenario: Stale heartbeat detection
- **GIVEN** an active agent run with an average step interval of 15 seconds
- **WHEN** no heartbeat pulse or progress event is recorded for 30 seconds (>2x mean step interval)
- **THEN** Local Watch SHALL mark the agent status as `heartbeat_stale`
- **AND** update the Omarchy bar indicator to warn the desktop operator of a stalled agent

#### Scenario: Zero-error high token anomaly
- **GIVEN** an agent running unit tests
- **WHEN** the agent reports 0 test errors but continues consuming large token volumes (>1.5x expected) without producing output files
- **THEN** Local Watch SHALL flag a `ZeroErrorHighToken` anomaly card
- **AND** surface the suspicion of spinning internal reasoning loops
