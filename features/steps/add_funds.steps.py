from behave import given, when, then
from django.contrib.auth import get_user_model
from  WebProject.utils import get_admin
from WebProject.models import Wallet

User = get_user_model()
@given('the admin has at least 100 euros in their wallet')
def step_impl(context):
    admin = get_admin()
    wallet, _ = Wallet.objects.get_or_create(user=admin)
    wallet.balance = 100.00
    wallet.save()


@given('I am logged in as "{email}" with password "{password}"')
def step_impl(context, email, password):
    context.browser.visit(context.get_url('/users/login/'))
    context.browser.fill('username', email)
    context.browser.fill('password', password)
    context.browser.find_by_value('Log In').click()

@given('I visit the add funds page')
def step_impl(context):
    context.browser.visit(context.get_url('/funds/add/'))

@when('I enter the amount "{amount}"')
def step_impl(context, amount):
    context.browser.fill('amount', amount)

@when('I press the add button')
def step_impl(context):
    context.browser.find_by_value('Add').click()

@then('I should be redirected to the dashboard page')
def step_impl(context):
    assert context.browser.url.endswith('/'), f"Expected to be on dashboard, but was on {context.browser.url}"

@then('my wallet balance should be "{expected_balance}"')
def step_impl(context, expected_balance):
    wallet = Wallet.objects.get(user__email="ex@gmail.com")
    assert str(wallet.balance) == expected_balance, f"Expected balance {expected_balance}, but got {wallet.balance}"
