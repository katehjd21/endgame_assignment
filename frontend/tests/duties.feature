Feature: Managing Duties
  As a user of the Automate Duties Page
  I want to manage duties correctly
  So that I can create, delete, mark complete, reset duties
  And avoid duplicating duties by ensuring names are unique

  Background:
    Given an empty duties collection

  Scenario: Add a new duty successfully
    When I add a duty with number 1, description "Test Duty", and KSBs "K, S, B"
    Then the duties collection should contain 1 duty
    And the duty's number should be 1
    And the duty's description should be "Test Duty"
    And the duty's KSBs should be "K, S, B"

  Scenario: Prevent adding a duplicate duty
    Given the duties collection contains a duty with number 1 and description "Existing Duty"
    When I try to add a duty with number 1 and description "Duplicate Duty"
    Then the addition of this duty should fail
    And the duties collection should still contain 1 duty

  Scenario: Delete a duty
    Given the duties collection contains a duty with number 1
    When I delete the duty with number 1
    Then the duties collection should contain 0 duties

  Scenario: List all duties
    Given the duties collection contains "Duty 1" and "Duty 2"
    When I list all duties
    Then I should see 2 duties with numbers 1 and 2

  Scenario: Reset all duties
    Given the duties collection contains a list of 3 duties
    When I reset all duties
    Then the duties collection should contain 0 duties