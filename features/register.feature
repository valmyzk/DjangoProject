Feature: User registration

  Scenario: Successful registration creates a wallet
    Given I am on the registration page
    When I register with email "newuser@gmail.com", password "o123o123A", and phone "000 000 000"
    Then I should be redirected to the dashboard
    And a wallet should be created for "newuser@gmail.com"
