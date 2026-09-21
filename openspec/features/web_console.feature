@yard @ui @keyboard
Feature: Tokyo Night Keyboard-First Web Console Navigation
  As a developer and operator
  I want a fast, keyboard-first dashboard in Tokyo Night styling
  So that I can switch views, filter cards, and triage anomalies instantly without touching the mouse

  Background:
    Given the YARD Web Console is loaded at "index.html"
    And the Tokyo Night theme is active

  Scenario Outline: Switching dashboard views via numerical keys 1 through 7
    When the user presses key "<key>"
    Then the active view switches to "<view_name>"
    And the header displays active view "<view_name>"
    And the URL hash or state updates accordingly

    Examples:
      | key | view_name    |
      | 1   | overview     |
      | 2   | the yard     |
      | 3   | crews        |
      | 4   | cursor build |
      | 5   | grok ship    |
      | 6   | local watch  |
      | 7   | signals      |

  Scenario: Navigating cards using vim keys j and k
    Given the user is on view "the yard"
    And there are 5 active cards displayed
    When the user presses "j"
    Then the focus shifts from card 1 to card 2
    When the user presses "j"
    Then the focus shifts to card 3
    When the user presses "k"
    Then the focus shifts back to card 2

  Scenario: Filtering cards with forward slash key
    Given the user is on any view with cards
    When the user presses "/"
    Then the cursor focus moves to the search filter input
    When the user types "canary"
    Then only cards matching "canary" are rendered in the list
    When the user presses "Escape"
    Then the filter input loses focus and card selection is restored

  Scenario: Inspecting card details with Return and dismissing with Escape
    Given card "STORY-204" is currently focused
    When the user presses "Enter"
    Then the detail drawer for "STORY-204" opens
    And displays the token trajectory, git branch, and runtime logs
    When the user presses "Escape"
    Then the detail drawer closes
