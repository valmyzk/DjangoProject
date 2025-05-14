from behave import given, when, then
from django.contrib.auth import get_user_model
from WebProject.models import Wallet  # Replace 'myapp' with the actual app name that defines Wallet

User = get_user_model()

@given('I am on the registration page')
def step_impl(context):
    context.browser.visit(context.get_url('/users/signup/'))

from time import sleep

@when('I register with email "{email}", password "{password}", and phone "{phone}"')
def step_impl(context, email, password, phone):
    context.browser.fill('email', email)
    context.browser.fill('phone', phone)
    context.browser.fill('date_of_birth', '1970-01-01')
    context.browser.fill('password1', password)
    context.browser.fill('password2', password)

    checkbox = context.browser.find_by_id('tos').first
    context.browser.execute_script("arguments[0].click();", checkbox._element)

    # Scroll to the submit button
    button = context.browser.find_by_value('Sign up').first
    context.browser.execute_script("arguments[0].scrollIntoView(true);", button._element)

    sleep(0.5)  # Give time for scroll or animations to finish
    button.click()

@then('I should be redirected to the dashboard')
def step_impl(context):
    assert context.browser.url.endswith('/'), f"Expected to be on dashboard, but was on {context.browser.url}"

@then('a wallet should be created for "{email}"')
def step_impl(context, email):
    user = User.objects.get(email=email)
    assert Wallet.objects.filter(user=user).exists(), "Wallet object does not exist in DB."
