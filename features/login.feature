Feature: User login

  Scenario: Successful login with valid credentials
    Given a user exists with email "email" and password "password"
    And I am on the login page

