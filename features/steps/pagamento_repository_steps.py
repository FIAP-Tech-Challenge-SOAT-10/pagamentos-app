from behave import given, when, then
from unittest.mock import MagicMock
from datetime import datetime
from decimal import Decimal
from app.domain.entities.pagamento import Pagamento
from app.domain.repositories.pagamento_repository import PagamentoRepository


def criar_pagamento_mock():
    return Pagamento(
        id_pagamento=123456,
        id_pedido="pedido-abc",
        status="Pendente",
        valor=Decimal("99.99"),
        data_criacao=datetime.now()
    )


@given("um pagamento válido chega ao sistema")
def step_given_pagamento_valido(context):
    context.pagamento = criar_pagamento_mock()


@given("um pagamento com ID 123456 existe no banco")
def step_given_pagamento_existe(context):
    context.pagamento_id = 123456
    context.pagamento_mock = {
        "id_pagamento": 123456,
        "id_pedido": "pedido-abc",
        "status": "Recebido",
        "valor": "150.00",
        "data_criacao": datetime.now().isoformat()
    }

    mock_table = MagicMock()
    mock_table.get_item.return_value = {"Item": context.pagamento_mock}

    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table

    context.repo = PagamentoRepository(dynamodb_resource=mock_dynamodb)


@given("nenhum pagamento com ID 999999 existe no banco")
def step_given_pagamento_inexistente(context):
    context.pagamento_id = 999999

    mock_table = MagicMock()
    mock_table.get_item.return_value = {}  # nenhum pagamento encontrado

    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table

    context.repo = PagamentoRepository(dynamodb_resource=mock_dynamodb)


@when("eu salvar o pagamento")
def step_when_salvar_pagamento(context):
    mock_table = MagicMock()
    mock_table.put_item.return_value = {}

    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table

    repo = PagamentoRepository(dynamodb_resource=mock_dynamodb)
    context.resultado = repo.save(context.pagamento)


@when("eu buscar o pagamento pelo ID")
def step_when_buscar_pagamento(context):
    context.resultado = context.repo.get_pagamento_by_id(context.pagamento_id)


@when("eu atualizar o pagamento")
def step_when_atualizar_pagamento(context):
    mock_table = MagicMock()
    mock_table.update_item.return_value = {}

    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table

    repo = PagamentoRepository(dynamodb_resource=mock_dynamodb)
    context.resultado = repo.update_pagamento(context.pagamento)


@then("o pagamento deve ser retornado com sucesso")
@then("o pagamento deve ser atualizado com sucesso")
def step_then_pagamento_retornado(context):
    assert context.resultado is not None
    assert isinstance(context.resultado, Pagamento)


@then("o pagamento deve ser retornado")
def step_then_pagamento_encontrado(context):
    assert context.resultado is not None
    assert isinstance(context.resultado, Pagamento)
    assert context.resultado.id_pagamento == 123456


@then("nenhum pagamento deve ser encontrado")
def step_then_pagamento_nao_encontrado(context):
    assert context.resultado is None
