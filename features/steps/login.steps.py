from datetime import date

from behave import given, when, then
from django.contrib.auth import get_user_model

User = get_user_model()


@given('a user exists with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    if not User.objects.filter(email=email).exists():
        User.objects.create_user(email=email, password=password, phone='+34 123 456 789',
                                 date_of_birth=date(1970, 1, 1))


@given('I am on the login page')
def step_impl(context):
    context.browser.visit(context.get_url('/users/login/'))


@when('I enter email "{email}" and password "{password}"')
def step_impl(context, email, password):
    context.browser.fill('username', email)
    context.browser.fill('password', password)


@when('I press the login button')
def step_impl(context):
    context.browser.find_by_value('Log In').click()


@then('I should enter to the dashboard')
def step_impl(context):
    assert context.browser.url.endswith('/'), f"Expected to be on dashboard, but was on {context.browser.url}"


@then('I should see a login error message')
def step_impl(context):
    error = context.browser.find_by_css('.alert-danger').first
    assert error, "Expected a login error message but none was found"
    assert "correct" in error.text.lower(), f"Unexpected error message text: {error.text}"
