Feature: Transfer funds between users

  Scenario: Authenticated user transfers funds successfully
    Given a user exists with email "ex@gmail.com" and password "o123o123A"
    And a user exists with email "receiver@gmail.com" and password "p123p123B"
    And "ex@gmail.com" has at least 100 euros in their wallet
    And I am logged in as "ex@gmail.com" with password "o123o123A"
    And I visit the transfer funds page
    When I enter "receiver@gmail.com" as the destination
    And I enter "30.00" as the transfer amount
    And I press the transfer button
    Then I should be redirected to the dashboard page
    And "ex@gmail.com" wallet balance should be "70.00"
    And "receiver@gmail.com" wallet balance should be "30.00"


  Scenario: Transfer fails when amount is invalid
    Given a user exists with email "ex@gmail.com" and password "o123o123A"
    And a user exists with email "receiver@gmail.com" and password "p123p123B"
    And "ex@gmail.com" has at least 100 euros in their wallet
    And I am logged in as "ex@gmail.com" with password "o123o123A"
    And I visit the transfer funds page
    When I enter "receiver@gmail.com" as the destination
    And I enter "-50" as the transfer amount
    And I press the transfer button
    Then I should see an error message "Ensure this value is greater than or equal to 0."
    And "ex@gmail.com" wallet balance should be "100.00"
    And "receiver@gmail.com" wallet balance should be "0.00"
