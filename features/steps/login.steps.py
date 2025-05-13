from behave import given, when, then
from django.contrib.auth import get_user_model


User = get_user_model()

@given('a user exists with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    if not User.objects.filter(email=email).exists():
        User.objects.create_user(email=email, password=password)

@given('I am on the login page')
def step_impl(context):
    context.browser.visit(context.get_url('/users/login/'))




