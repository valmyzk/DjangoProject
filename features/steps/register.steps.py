from behave import given, when, then
from django.contrib.auth import get_user_model
from WebProject.models import Wallet

User = get_user_model()


@given('I am on the registration page')
def step_impl(context):
    context.browser.visit(context.get_url('/users/signup/'))


@when('I register with email "{email}", password "{password}", and phone "{phone}" and date "{date}"')
def step_impl(context, email, password, phone, date):
    context.browser.fill('email', email)
    context.browser.fill('phone', phone)
    context.browser.fill('date_of_birth', date)
    context.browser.fill('password1', password)
    context.browser.fill('password2', password)

    context.browser.execute_script("document.getElementById('tos').checked = true;")
    context.browser.execute_script("document.querySelector('form').submit();")


@then('I should be redirected to the dashboard')
def step_impl(context):
    assert context.browser.url.endswith('/'), f"Expected to be on dashboard, but was on {context.browser.url}"


@then('a wallet should be created for "{email}"')
def step_impl(context, email):
    assert Wallet.objects.filter(user__email=email).exists(), "Wallet object does not exist in DB."
