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


@then('I should see a registration error message')
def step_impl(context):
    error = context.browser.find_by_css('.alert-danger, .text-danger, .errorlist li').first
    assert error, "Expected a registration error message but none was found"


@then('a wallet should not be created for "{email}"')
def step_impl(context, email):
    assert not Wallet.objects.filter(user__email=email).exists(), f"Unexpected wallet found for {email}"


@when('I register with email "failuser@gmail.com", password "", and phone "123 456 789" and date "1970-01-01"')
def step_impl_fail(context):
    context.browser.fill('email', "failuser@gmail.com")
    context.browser.fill('phone', "123 456 789")
    context.browser.fill('date_of_birth', "1970-01-01")
    context.browser.fill('password1', "")
    context.browser.fill('password2', "")

    context.browser.execute_script("document.getElementById('tos').checked = true;")
    context.browser.execute_script("document.querySelector('form').submit();")
