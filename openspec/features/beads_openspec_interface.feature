Feature: OpenSpec and Beads Baseball Card Progress Interface
  As a Product Owner and Platform Operator
  I want an integrated interface between OpenSpec project requirements and Beads issue tracking
  So that I can monitor active beads in work, inspect their formal specifications via a baseball card modal, and see last completed, in-work, and next bead progression.

  Background:
    Given the YARD mixed-fleet control plane is active
    And multiple projects with Beads issue trackers are connected:
      | project                 | current_bead         | spec_id                                    |
      | mowgli42/schwerpunkt    | schwerpunkt-i0i.3.1  | openspec/specs/orientation-layer/spec.md   |
      | mowgli42/yard-console   | yard-042             | openspec/specs/beads-openspec-interface/   |
      | mowgli42/o-my-sim       | o-my-sim-u1n.1       | docs/MISSION-PLAN-INGEST.md                |

  Scenario: Persistent current bead ticker on console header
    Given the web console is loaded on any view
    Then the header ribbon SHALL display the active bead "schwerpunkt-i0i.3.1"
    And the bead ticker SHALL display project "mowgli42/schwerpunkt"
    And the bead ticker SHALL display assigned agent "Cursor Cloud Agent (bc-709a)"
    And the bead ticker SHALL display model "gemini-3.8-flash"
    And clicking the ticker SHALL open the Baseball Card modal

  Scenario: Three-bead pipeline ribbon display
    Given the operator views the Beads Pipeline ribbon
    Then the ribbon SHALL display three sequential beads:
      | position       | issue_id             | status      | title                                              |
      | last_completed | schwerpunkt-i0i.2.5  | closed      | Operator REST API (manual demo, no AI)             |
      | in_work        | schwerpunkt-i0i.3.1  | in_progress | Observation impact hints + orient plan-impact      |
      | next           | schwerpunkt-i0i.3.2  | open        | MTO decision tree + Observe-Orient integration     |
    And the in-work bead SHALL exhibit an active pulse indicator
    And clicking "last_completed" SHALL switch the Baseball Card focus to "schwerpunkt-i0i.2.5"
    And clicking "next" SHALL switch the Baseball Card focus to "schwerpunkt-i0i.3.2"

  Scenario: OpenSpec Baseball Card modal content
    When the operator presses "b" or clicks the current bead
    Then the Baseball Card modal SHALL open
    And the card header SHALL show "schwerpunkt-i0i.3.1" with badge "IN WORK"
    And the card stats SHALL show token burn "38,200 / 50,000" (76%)
    And the OpenSpec section SHALL display the spec path "openspec/specs/orientation-layer/spec.md"
    And the OpenSpec section SHALL display the formal requirement "The orientation layer SHALL maintain a structured WorldModel"
    And the Gherkin section SHALL display formatted Gherkin steps:
      """
      GIVEN a completed Orient phase with known_facts
      WHEN a new Observe phase completes in the same session
      THEN Orient SHALL load the prior WorldModel from persistent store
      """

  Scenario: Stepping between pipeline beads inside the Baseball Card
    Given the Baseball Card modal is open on "schwerpunkt-i0i.3.1"
    When the operator presses "]"
    Then the Baseball Card SHALL advance to next bead "schwerpunkt-i0i.3.2"
    When the operator presses "["
    Then the Baseball Card SHALL step back to "schwerpunkt-i0i.3.1"
    When the operator presses "[" again
    Then the Baseball Card SHALL step back to last completed bead "schwerpunkt-i0i.2.5"
    When the operator presses "Escape"
    Then the Baseball Card modal SHALL close
