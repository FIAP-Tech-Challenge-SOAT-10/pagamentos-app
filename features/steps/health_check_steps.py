from behave import when, then

@when('eu faço uma requisição GET para "/health"')
def step_impl(context):
    context.response = context.client.get("/health")

@then('a resposta deve conter status "{expected_status}"')
def step_impl(context, expected_status):
    assert context.response.status_code == int(expected_status)
