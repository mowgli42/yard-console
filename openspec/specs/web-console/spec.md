# Web Console UI & Navigation Specification

## Purpose

Define the user experience, interaction architecture, and visual aesthetics of the standalone YARD Web Console.

## Requirements

### Requirement: Tokyo Night Theme & High-Density Presentation

The Web Console UI SHALL strictly conform to the Tokyo Night color palette and provide clear visual contrast between runtime states and detector alerts.

- Background: `#1a1b26` (Canvas) / `#24283b` (Cards & Panels)
- Accents: `#7aa2f7` (Tokyo Blue), `#bb9af7` (Purple), `#7dcfff` (Cyan)
- State Colors: `#9ece6a` (Green/Pass), `#e0af68` (Yellow/Warning), `#f7768e` (Red/Danger)
- Typography: Clean monospace and system sans-serif with high legibility.

#### Scenario: Displaying high-contrast runtime cards
- **GIVEN** the YARD Web Console opened in a modern browser
- **WHEN** the dashboard renders
- **THEN** Cursor cards SHALL feature Tokyo Blue accents (`#7aa2f7`)
- **AND** Grok cards SHALL feature Cyan/Purple accents (`#7dcfff` / `#bb9af7`)
- **AND** Local Watch alerts SHALL feature high-visibility Warning (`#e0af68`) or Urgent (`#f7768e`) indicators

### Requirement: Full Keyboard-First Navigation

The Web Console SHALL be fully operable without requiring a mouse, enabling rapid terminal-like operator interactions.

#### Scenario: Switching views via number keys
- **GIVEN** any active view in the web console
- **WHEN** the operator presses keys `1` through `7`
- **THEN** the console SHALL instantly transition to the corresponding view:
  - `1`: Overview
  - `2`: The Yard (Kanban / Fleet Board)
  - `3`: Crews (Domain teams & WIP caps)
  - `4`: Cursor Build (PRs & test generation)
  - `5`: Grok Ship (Canaries & releases)
  - `6`: Local Watch (Detector log triage)
  - `7`: Signals (Anomalies & heartbeats)
- **AND** SHALL update the active tab header without reloading the page

#### Scenario: Navigating cards via vim-style j/k keys
- **GIVEN** The Yard view or Signals view with multiple cards
- **WHEN** the operator presses `j`
- **THEN** the selection cursor SHALL move to the next card in the list
- **AND** WHEN the operator presses `k`
- **THEN** the selection cursor SHALL move to the previous card
- **AND** the currently selected card SHALL exhibit a prominent Tokyo Night focus outline

#### Scenario: Quick filter via slash key
- **GIVEN** any card listing or telemetry view
- **WHEN** the operator presses `/`
- **THEN** keyboard focus SHALL immediately jump to the search/filter input box
- **AND** typing characters SHALL filter the visible cards in real-time
- **AND** pressing `esc` SHALL clear filter focus and return to card selection

#### Scenario: Inspecting details via Return key
- **GIVEN** a card selected via navigation keys
- **WHEN** the operator presses `return`
- **THEN** a modal detail panel or drawer SHALL open showing complete token curves, diff previews, detector logs, or run metadata
- **AND** pressing `esc` SHALL close the detail panel
