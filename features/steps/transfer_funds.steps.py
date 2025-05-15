from behave import given, when, then
from django.contrib.auth import get_user_model
from WebProject.models import Wallet
from WebProject.utils import get_admin

User = get_user_model()



@given('"{email}" has at least {amount} euros in their wallet')
def step_impl(context, email, amount):
    user = User.objects.get(email=email)
    wallet, _ = Wallet.objects.get_or_create(user=user)
    wallet.balance = float(amount)
    wallet.save()

@given('I visit the transfer funds page')
def step_impl(context):
    context.browser.visit(context.get_url('/funds/transfer/'))

@when('I enter "{destination}" as the destination')
def step_impl(context, destination):
    context.browser.fill('destination', destination)

@when('I enter "{amount}" as the transfer amount')
def step_impl(context, amount):
    context.browser.fill('amount', amount)

@when('I press the transfer button')
def step_impl(context):
    context.browser.find_by_value('Transfer').click()

@then('"{email}" wallet balance should be "{expected_balance}"')
def step_impl(context, email, expected_balance):
    user = User.objects.get(email=email)
    wallet = Wallet.objects.get(user=user)
    assert str(wallet.balance) == expected_balance, f"Expected balance {expected_balance}, but got {wallet.balance}"
