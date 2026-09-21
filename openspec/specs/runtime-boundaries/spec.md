# Runtime Boundaries & Contracts Specification

## Purpose

Define the operational and security boundaries separating the three primary execution runtimes in YARD:
1. **Cursor Runtime:** Construction and test generation.
2. **Grok Runtime:** Deployment, tagging, canary analysis, and release management.
3. **Local LLM Runtime:** On-premise telemetry analysis, heartbeat monitoring, and log classification.

## Requirements

### Requirement: Strict Runtime Isolation

The YARD control plane SHALL enforce that agents running within one runtime boundary cannot execute forbidden capabilities reserved for other runtimes.

#### Scenario: Cursor agent attempts direct cluster deployment
- **GIVEN** an active task assigned to the Cursor runtime
- **WHEN** the agent attempts to issue a cluster mutation or deploy command to production
- **THEN** YARD API SHALL reject the execution request with `403 Forbidden: Runtime Boundary Violation`
- **AND** SHALL record an audit warning in the event ledger
- **AND** the story SHALL remain in the `in_development` state pending standard PR review

#### Scenario: Grok agent attempts to modify product acceptance criteria
- **GIVEN** an active release task assigned to the Grok runtime
- **WHEN** the Grok agent attempts to modify `DOMAIN.md` or change story acceptance criteria
- **THEN** YARD API SHALL reject the modification request
- **AND** Grok SHALL only be permitted to append release notes, canary health scores, and promotion recommendations

#### Scenario: Local LLM runtime maintains zero egress
- **GIVEN** the Local LLM watch engine analyzing journald or CI logs
- **WHEN** telemetry is processed
- **THEN** all log classification and heartbeat checks SHALL run on-premise without outbound cloud egress
- **AND** no customer payloads or proprietary source code SHALL be transmitted externally

### Requirement: The Three-Runtime Pipeline Handshake

The YARD control plane SHALL govern state handoffs strictly according to the pipeline lifecycle contract.

#### Scenario: Transition from Cursor Build to Verification Tag
- **GIVEN** a Cursor agent completes story implementation and opens a GitHub Pull Request
- **WHEN** CI automated lint checks and golden evaluation tests pass
- **THEN** YARD SHALL generate a cryptographically signed image tag containing git SHA, prompt hash, and evaluation snapshot
- **AND** SHALL dispatch a canary deployment notification to the Grok runtime

#### Scenario: Grok triggers canary rollback on elevated error rate
- **GIVEN** Grok is monitoring a live canary deployment
- **WHEN** canary telemetry detects error rates exceeding baseline thresholds
- **THEN** Grok SHALL issue a rollback command to the prior stable tag
- **AND** YARD SHALL transition the story state to `rollback_triaged`
- **AND** a high-priority alert card SHALL be placed on the yard board
