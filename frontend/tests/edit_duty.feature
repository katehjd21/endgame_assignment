Feature: Edit an existing duty
  As a user
  I want to update the details of a duty
  So that I can correct mistakes or improve the information

  Scenario: Successfully editing a duty
    Given there is a duty with number 1 and description "Original Duty Description" and KSBs "K, S, B"
    When I edit the duty with number 1 to have description "Updated Duty Description" and KSBs "K1, S1, B1"
    Then the duty with number 1 should have description "Updated Duty Description"
    And the duty with number 1 should have KSBs "K1, S1, B1"

  Scenario: Attempting to edit a non-existent duty
    When I try to edit a duty with number 999 to have description "Duty Does Not Exist" and KSBs "K, S, B"
    Then the edit should fail