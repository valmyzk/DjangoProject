Feature: User registration

  Scenario: Successful registration creates a wallet
    Given I am on the registration page
    When I register with email "newuser@gmail.com", password "o123o123A", and phone "000 000 000" and date "1970-01-01"
    Then I should be redirected to the dashboard
    And a wallet should be created for "newuser@gmail.com"

  Scenario: Failed registration with missing password
    Given I am on the registration page
    When I register with email "failuser@gmail.com", password "", and phone "123 456 789" and date "1970-01-01"
    Then I should see a registration error message
    And a wallet should not be created for "failuser@gmail.com"
