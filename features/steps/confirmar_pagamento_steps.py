from behave import given, when, then
from unittest.mock import MagicMock
from app.domain.entities.pagamento import Pagamento
from app.application.use_cases.confirmar_pagamento import confirmar_pagamento
from datetime import datetime
from decimal import Decimal

@given('que existe um pagamento com id {id_pagamento:d} e status "{status}"')
def step_given_pagamento(context, id_pagamento, status):
    pagamento = Pagamento(
        id_pagamento=id_pagamento,
        id_pedido="pedido789",
        valor=Decimal("150.00"),
        status=status,
        data_criacao=datetime.now()
    )

    context.mock_repository = MagicMock()
    context.mock_repository.get_pagamento_by_id.return_value = pagamento
    context.usecase = confirmar_pagamento(context.mock_repository)
    context.pagamento_id = id_pagamento
    context.exception = None

@given('que não existe pagamento com id {id_pagamento:d}')
def step_given_pagamento_inexistente(context, id_pagamento):
    context.mock_repository = MagicMock()
    context.mock_repository.get_pagamento_by_id.return_value = None
    context.usecase = confirmar_pagamento(context.mock_repository)
    context.pagamento_id = id_pagamento
    context.exception = None

@when('eu atualizo o status para "{novo_status}"')
def step_when_atualizo_status(context, novo_status):
    context.resultado = context.usecase.execute(context.pagamento_id, novo_status)

@when('eu tento atualizar o status para "{novo_status}"')
def step_when_tenta_atualizar(context, novo_status):
    try:
        context.usecase.execute(context.pagamento_id, novo_status)
    except Exception as e:
        context.exception = e

@then('o status do pagamento deve ser "{status_esperado}"')
def step_then_verifica_status(context, status_esperado):
    assert context.resultado.status == status_esperado

@then('uma exceção deve ser lançada com a mensagem "{mensagem}"')
def step_then_erro(context, mensagem):
    assert context.exception is not None
    assert isinstance(context.exception, ValueError)
    assert str(context.exception) == mensagem
