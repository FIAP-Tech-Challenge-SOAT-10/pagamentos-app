from behave import given, when, then
from decimal import Decimal
from unittest.mock import MagicMock
from app.application.use_cases.enviar_pagamento import EnviarPagamentoUseCase
from app.domain.entities.pagamento import Pagamento
from app.domain.value_objects.status_pagamento import StatusPagamento
from app.interfaces.api.models import PagamentoConfirmacao

@given('que existe um pedido com ID "{pedido_id}"')
def step_given_pedido_id(context, pedido_id):
    context.pedido_id = pedido_id

@given('um valor de pagamento de {valor:f}')
def step_given_valor_pagamento(context, valor):
    context.valor = Decimal(str(valor))

@when('eu executo o caso de uso de envio de pagamento')
def step_when_execute_usecase(context):
    # Mock do repositório
    mock_repo = MagicMock()
    mock_repo.save = MagicMock()

    # Mock do serviço de webhook que retorna confirmação
    mock_webhook = MagicMock()
    mock_webhook.enviar.return_value = PagamentoConfirmacao(
        id_pagamento=123456,
        status=StatusPagamento.RECEBIDO
    )

    # Executa o usecase com mocks
    usecase = EnviarPagamentoUseCase(mock_repo, mock_webhook)
    context.resultado = usecase.execute(context.pedido_id, context.valor)

@then('o pagamento deve ser confirmado com status "{status_esperado}"')
def step_then_confirmado(context, status_esperado):
    assert context.resultado is not None
    assert context.resultado.status == status_esperado

