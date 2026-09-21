@yard @runtime
Feature: Runtime Boundary Isolation & Pipeline Enforcement
  As a product owner and platform operator
  I want strict boundaries between Cursor, Grok, and Local LLM runtimes
  So that code generation, deployment authority, and log observation never mix dangerously

  Background:
    Given a configured YARD control plane
    And active domain crews with assigned runtime agents

  Scenario: Cursor agent cannot directly mutate production clusters
    Given a story "CORE-101" assigned to runtime "cursor"
    When the "cursor" agent submits a command "kubectl apply -f prod-deployment.yaml"
    Then the YARD control plane rejects the execution with status 403
    And an audit event "runtime_boundary_violation" is appended to the ledger
    And the story remains in state "in_development"

  Scenario: Grok agent cannot modify story domain scope or acceptance criteria
    Given a release candidate "v1.4.0-rc2" assigned to runtime "grok"
    When the "grok" agent attempts to edit "DOMAIN.md" acceptance criteria
    Then the YARD control plane rejects the write request
    And the agent is restricted to tagging, canary telemetry, and promote/rollback decisions

  Scenario: Local LLM watcher maintains strict on-premise zero egress
    Given the local LLM watcher analyzing systemd journald logs
    When log anomaly classification is performed
    Then all token evaluation executes on localhost
    And zero network packets are egressed to public cloud LLM providers
    And no customer payloads or secrets leave the local machine

  Scenario: Grok executes automatic canary rollback on elevated error rates
    Given a live canary deployment for tag "sha-709a-v2"
    When canary error rate exceeds the baseline threshold by 15 percent
    Then the "grok" runtime issues a rollback command to "sha-stable-v1"
    And YARD transitions the story to "rollback_triaged"
    And an urgent alert card is raised on "the yard" board
