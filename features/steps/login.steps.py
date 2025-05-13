from behave import given, when, then
from django.contrib.auth import get_user_model

from datetime import date

User = get_user_model()

@given('a user exists with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    if not User.objects.filter(email=email).exists():
        User.objects.create_user(email=email, password=password, phone='+34 123 456 789', date_of_birth=date(1970, 1, 1))

@given('I am on the login page')
def step_impl(context):
    context.browser.visit(context.get_url('/users/login/'))




