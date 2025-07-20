from behave import given, when, then
from app.domain.entities.pagamento import Pagamento, CriarPagamentoRequest
from decimal import Decimal
from datetime import datetime
from pydantic import ValidationError

@given("um payload de Pagamento válido")
def step_given_pagamento_valido(context):
    context.payload = {
        "id_pagamento": 123,
        "id_pedido": "pedido123",
        "valor": Decimal("150.00"),
        "status": "Pendente",
        "data_criacao": datetime.now()
    }

@given("um payload de Pagamento com valor -10.0")
def step_given_pagamento_valor_negativo(context):
    context.payload = {
        "id_pagamento": 124,
        "id_pedido": "pedido124",
        "valor": Decimal("-10.0"),
        "status": "Pendente",
        "data_criacao": datetime.now()
    }

@given('um payload de Pagamento sem campo obrigatório "{campo}"')
def step_given_pagamento_sem_campo(context, campo):
    payload = {
        "id_pagamento": 125,
        "id_pedido": "pedido125",
        "valor": Decimal("99.99"),
        "status": "Aprovado",
        "data_criacao": datetime.now()
    }
    del payload[campo]
    context.payload = payload

@given("um payload de CriarPagamentoRequest com valor 100.0")
def step_given_criar_pagamento_valido(context):
    context.payload = {
        "id_pedido": "pedidoXYZ",
        "valor": Decimal("100.0")
    }

@given("um payload de CriarPagamentoRequest com valor 0")
def step_given_criar_pagamento_zero(context):
    context.payload = {
        "id_pedido": "pedidoZero",
        "valor": Decimal("0.0")
    }

@when("eu tento criar o objeto Pagamento")
def step_when_criar_pagamento(context):
    try:
        context.resultado = Pagamento(**context.payload)
        context.erro = None
    except ValidationError as e:
        context.resultado = None
        context.erro = str(e)

@when("eu tento criar o objeto CriarPagamentoRequest")
def step_when_criar_criar_pagamento(context):
    try:
        context.resultado = CriarPagamentoRequest(**context.payload)
        context.erro = None
    except ValidationError as e:
        context.resultado = None
        context.erro = str(e)

@then("o objeto deve ser criado com sucesso")
def step_then_objeto_criado(context):
    assert context.resultado is not None
    assert context.erro is None

@then('deve ocorrer um erro de validação com a mensagem "{mensagem}"')
def step_then_erro_validacao(context, mensagem):
    assert context.resultado is None
    assert context.erro is not None
    print("Mensagem de erro capturada:\n", context.erro)
    assert mensagem.lower() in context.erro.lower()

