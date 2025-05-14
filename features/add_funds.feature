Feature: Add funds to wallet

  Scenario: Authenticated user adds funds successfully
    Given a user exists with email "ex@gmail.com" and password "o123o123A"
    And the admin has at least 100 euros in their wallet
    And I am logged in as "ex@gmail.com" with password "o123o123A"
    And I visit the add funds page
    When I enter the amount "50.00"
    And I press the add button
    Then I should be redirected to the dashboard page
    And my wallet balance should be "50.00"