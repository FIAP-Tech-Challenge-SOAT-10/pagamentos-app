import pytest
from httpx import AsyncClient
from fastapi import status
from app.lambda_function import app  
from app.domain.entities.pagamento import Pagamento
from app.interfaces.api.models import PagamentoConfirmacao
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal

@pytest.mark.asyncio
async def test_health_check():
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_enviar_pagamento(monkeypatch):
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    # Mock da response do webhook
    mock_webhook = MagicMock()
    mock_response = PagamentoConfirmacao(id_pagamento=123456, status="Pendente")
    mock_webhook.enviar.return_value = mock_response

    # Mock do repositório
    mock_repo = MagicMock()
    mock_repo.save.return_value = None

    mock_sqs = MagicMock()
    # Monkeypatch no método get_sqs_client
    monkeypatch.setattr("app.infrastructure.queue.publisher.get_sqs_client", lambda: mock_sqs)

    monkeypatch.setenv("PAGAMENTO_QUEUE_URL", "https://mock-queue-url")

    # Override das dependências no escopo do teste
    monkeypatch.setattr("app.interfaces.api.routes.PagamentoRepository", lambda: mock_repo)
    monkeypatch.setattr("app.interfaces.api.routes.WebhookService", lambda: mock_webhook)

    payload = {
        "id_pedido": "abc123",
        "valor": "150.00"
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/pagamentos/enviar", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "id_pagamento": 123456,
        "status": "Pendente"
    }


@pytest.mark.asyncio
async def test_enviar_pagamento_erro_interno(monkeypatch):
    # Mock do webhook e repositório
    mock_webhook = MagicMock()
    mock_repo = MagicMock()

    mock_sqs = MagicMock()
    # Monkeypatch no método get_sqs_client
    monkeypatch.setattr("app.infrastructure.queue.publisher.get_sqs_client", lambda: mock_sqs)
    monkeypatch.setenv("PAGAMENTO_QUEUE_URL", "https://mock-queue-url")

    # Mock do UseCase que lança exceção
    mock_use_case = MagicMock()
    mock_use_case.execute.side_effect = Exception("Simulated failure")

    # Substitui apenas as dependências usadas diretamente no endpoint
    monkeypatch.setattr("app.interfaces.api.routes.PagamentoRepository", lambda: mock_repo)
    monkeypatch.setattr("app.interfaces.api.routes.WebhookService", lambda: mock_webhook)

    # Mock do EnviarPagamentoUseCase para injetar exceção no execute()
    from app.interfaces.api import routes
    monkeypatch.setattr(routes, "EnviarPagamentoUseCase", lambda *_: mock_use_case)

    payload = {
        "id_pedido": "abc123",
        "valor": "150.00"
    }

    from httpx import ASGITransport
    transport=transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/pagamentos/enviar", json=payload)

    assert response.status_code == 500
    assert "Erro interno ao registrar pagamento" in response.json()["detail"]


@pytest.mark.asyncio
async def test_confirmar_pagamento(monkeypatch):
    mock_pagamento = Pagamento(
        id_pagamento=123456,
        id_pedido="abc123",
        valor=Decimal("150.00"),
        status="Confirmado",
        data_criacao="2023-10-01T12:00:00"
    )

    # Mock do repositório com pagamento existente
    mock_repo = MagicMock()
    mock_repo.get_pagamento_by_id.return_value = mock_pagamento
    
    mock_sqs = MagicMock()
    # Monkeypatch no método get_sqs_client
    monkeypatch.setattr("app.infrastructure.queue.publisher.get_sqs_client", lambda: mock_sqs)

    monkeypatch.setenv("PAGAMENTO_QUEUE_URL", "https://mock-queue-url")

    monkeypatch.setattr("app.interfaces.api.routes.PagamentoRepository", lambda: mock_repo)

    payload = {
        "id_pagamento": 123456,
        "status": "Confirmado"
    }

    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/pagamentos/confirmar", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "id_pagamento": 123456,
        "status": "Confirmado"
    }

@pytest.mark.asyncio
async def test_confirmar_pagamento_nao_encontrado(monkeypatch):
    # Mock do repositório que retorna None
    mock_repo = MagicMock()
    mock_repo.get_pagamento_by_id.return_value = None

    mock_sqs = MagicMock()
    # Monkeypatch no método get_sqs_client
    monkeypatch.setattr("app.infrastructure.queue.publisher.get_sqs_client", lambda: mock_sqs)

    monkeypatch.setenv("PAGAMENTO_QUEUE_URL", "https://mock-queue-url")

    # Patch da dependência
    monkeypatch.setattr("app.interfaces.api.routes.PagamentoRepository", lambda: mock_repo)

    payload = {
        "id_pagamento": 999,
        "status": "Confirmado"
    }

    from httpx import ASGITransport
    transport=transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/pagamentos/confirmar", json=payload)

    assert response.status_code == 404
    assert "Pagamento não encontrado" in response.json()["detail"]

@pytest.mark.asyncio
async def test_confirmar_pagamento_erro_interno(monkeypatch):
    # Mock do repositório com exceção
    mock_repo = MagicMock()
    mock_repo.get_pagamento_by_id.side_effect = Exception("Erro inesperado")

    mock_sqs = MagicMock()
    # Monkeypatch no método get_sqs_client
    monkeypatch.setattr("app.infrastructure.queue.publisher.get_sqs_client", lambda: mock_sqs)

    monkeypatch.setenv("PAGAMENTO_QUEUE_URL", "https://mock-queue-url")

    monkeypatch.setattr("app.interfaces.api.routes.PagamentoRepository", lambda: mock_repo)

    payload = {
        "id_pagamento": 123456,
        "status": "Confirmado"
    }

    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/pagamentos/confirmar", json=payload)

    assert response.status_code == 500
    assert "Erro interno" in response.json()["detail"]
