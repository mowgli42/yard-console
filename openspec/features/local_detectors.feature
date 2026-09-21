@yard @detectors
Feature: Local Passive Anomaly Detectors
  As a platform operator and human product owner
  I want passive local detectors watching agent execution
  So that runaway loops, budget overruns, and goal drift are flagged without autonomous destructive edits

  Background:
    Given the YARD local watch engine is active
    And an append-only event ledger is initialized

  Scenario: Token consumption 2x warning and 4x hard-stop flag
    Given a task "STORY-204" with an allocated budget of 50000 tokens
    When the Cursor agent burns 105000 tokens
    Then the detector flags a "Token2xExceeded" advisory warning
    And displays a yellow alert badge on the story card
    When the Cursor agent reaches 201000 tokens
    Then the detector flags a "Token4xHardStop" critical event
    And dispatches a pause signal to the running agent
    And sends an urgent notification to the desktop

  Scenario: Repeated identical tool call signature loop detection
    Given an agent session running on story "API-302"
    When the agent invokes "fetch_schema(endpoint='/v1/users')" 3 consecutive times with identical response
    Then the detector raises a "ToolLoopDetected" anomaly card
    And flags the session with "repeated_signature_count: 3"
    And marks the card on view "signals"

  Scenario: Goal drift detection against sprint brief
    Given an approved sprint brief in "DOMAIN.md" for story "AUTH-404"
    When the agent generates code edits and git diff
    And the semantic similarity vector score against the brief is 0.48
    Then the detector flags a "GoalDriftDetected" alert
    And surfaces the drift score "0.48 < 0.60" on the watch panel

  Scenario: Stale agent heartbeat warning
    Given an agent working on "DATA-501" with a mean step interval of 15 seconds
    When no activity or heartbeat event is received for 35 seconds
    Then the detector marks the agent as "heartbeat_stale"
    And updates the Omarchy status bar icon with an attention state
