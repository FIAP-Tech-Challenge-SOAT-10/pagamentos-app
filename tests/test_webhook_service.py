import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from decimal import Decimal

from app.domain.entities.pagamento import Pagamento
from app.infrastructure.services.webhook_service import WebhookService
from app.interfaces.api.models import PagamentoConfirmacao

@pytest.fixture
def pagamento_exemplo():
    return Pagamento(
        id_pagamento=123456,
        id_pedido="ABC123",
        valor=Decimal("150.00"),
        status="Pendente",
        data_criacao=datetime(2023, 10, 1, 12, 0, 0)
    )

@patch("app.infrastructure.services.webhook_service.requests.post")
def test_enviar_sucesso(mock_post, pagamento_exemplo):
    # Simula resposta do webhook
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id_pagamento": 123456,
        "status": "Recebido"
    }
    mock_post.return_value = mock_response

    service = WebhookService()
    result = service.enviar(pagamento_exemplo)

    assert isinstance(result, PagamentoConfirmacao)
    assert result.id_pagamento == 123456
    assert result.status == "Recebido"

@patch("app.infrastructure.services.webhook_service.requests.post")
def test_enviar_falha_status_code(mock_post, pagamento_exemplo):
    # Simula resposta com erro (status 500)
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_post.return_value = mock_response

    service = WebhookService()
    result = service.enviar(pagamento_exemplo)

    assert result is None

@patch("app.infrastructure.services.webhook_service.requests.post")
def test_enviar_excecao(mock_post, pagamento_exemplo):
    # Simula exceção durante envio
    mock_post.side_effect = Exception("Falha de conexão")

    service = WebhookService()
    result = service.enviar(pagamento_exemplo)

    assert result is None

@patch("app.infrastructure.services.webhook_service.requests.post")
def test_enviar_payload_correto(mock_post, pagamento_exemplo):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id_pagamento": 123456,
        "status": "Pendente"
    }
    mock_post.return_value = mock_response

    service = WebhookService()
    service.enviar(pagamento_exemplo)

    expected_payload = {
        "id_pagamento": 123456,
        "valor": float(pagamento_exemplo.valor),
        "status": "Pendente",
        "data_criacao": pagamento_exemplo.data_criacao.isoformat()
    }

    mock_post.assert_called_once_with(
        "https://vk45ivvi9k.execute-api.us-east-1.amazonaws.com/v1/pagamento",
        json=expected_payload,
        timeout=5
    )
