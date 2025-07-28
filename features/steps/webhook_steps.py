from behave import given, when, then
from decimal import Decimal
from datetime import datetime
from unittest.mock import patch, MagicMock
from app.domain.entities.pagamento import Pagamento
from app.infrastructure.services.webhook_service import WebhookService
from app.interfaces.api.models import PagamentoConfirmacao

@given("um pagamento válido")
def step_given_pagamento(context):
    context.pagamento = Pagamento(
        id_pagamento=123456,
        id_pedido="pedido123",
        valor=Decimal("100.50"),
        status="Pendente",
        data_criacao=datetime.now()
    )

@given("o webhook responde com status 200 e dados válidos")
def step_given_webhook_200(context):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id_pagamento": 123456,
        "status": "Recebido"
    }
    context.post_patch = patch("app.infrastructure.services.webhook_service.requests.post", return_value=mock_response)
    context.post_patch.start()

@given("o webhook responde com status 500")
def step_given_webhook_500(context):
    mock_response = MagicMock()
    mock_response.status_code = 500
    context.post_patch = patch("app.infrastructure.services.webhook_service.requests.post", return_value=mock_response)
    context.post_patch.start()

@given("o webhook lança uma exceção")
def step_given_webhook_excecao(context):
    context.post_patch = patch("app.infrastructure.services.webhook_service.requests.post", side_effect=Exception("Falha"))
    context.post_patch.start()

@when("o serviço de webhook é executado")
def step_when_executa_servico(context):
    service = WebhookService()
    context.resultado = service.enviar(context.pagamento)
    context.post_patch.stop()

@then('hen a confirmação do pagamento deve ter o status "Recebido"')
def step_then_pagamento_confirmado(context, esperado):
    assert isinstance(context.resultado, PagamentoConfirmacao)
    assert context.resultado.status == esperado

@then("nenhuma confirmação de pagamento deve ser retornada")
def step_then_none(context):
    assert context.resultado is None
