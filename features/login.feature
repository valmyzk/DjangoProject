Feature: User login

  Scenario: Successful login with valid credentials
    Given a user exists with email "ex@gmail.com" and password "o123o123A"
    And I am on the login page
    When I enter email "email" and password "password"
    And I press the login button
    Then I should enter to the dashboard

  Scenario: Failed login with invalid credentials
    Given a user exists with email "ex@gmail.com" and password "o123o123A"
    And I am on the login page
    When I enter email "ex@gmail.com" and password "wrongPassword"
    And I press the login button
    Then I should see a login error message





