import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from app.application.use_cases.enviar_pagamento import EnviarPagamentoUseCase
from app.domain.entities.pagamento import Pagamento
from app.interfaces.api.models import PagamentoConfirmacao


@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def mock_webhook_service():
    return MagicMock()


@pytest.fixture
def mock_publisher():
    """Mocka o SQSPublisher antes de instanciar o use case."""
    with patch("app.application.use_cases.enviar_pagamento.SQSPublisher") as mock:
        yield mock


@pytest.fixture
def use_case(mock_repository, mock_webhook_service, mock_publisher):
    return EnviarPagamentoUseCase(
        pagamento_repository=mock_repository,
        webhook_service=mock_webhook_service
    )


def test_enviar_pagamento_sucesso(use_case, mock_repository, mock_webhook_service):
    id_pedido = "ABC123"
    valor = Decimal("199.90")
    retorno_webhook = PagamentoConfirmacao(id_pagamento=123456, status="Recebido")

    mock_webhook_service.enviar.return_value = retorno_webhook

    result = use_case.execute(id_pedido, valor)

    # Verifica se um pagamento foi salvo
    assert mock_repository.save.call_count == 1
    pagamento_salvo = mock_repository.save.call_args[0][0]
    assert isinstance(pagamento_salvo, Pagamento)
    assert pagamento_salvo.id_pedido == id_pedido
    assert pagamento_salvo.valor == valor
    assert pagamento_salvo.status == "Pendente"

    # Verifica se o webhook foi chamado corretamente
    mock_webhook_service.enviar.assert_called_once_with(pagamento_salvo)

    # Verifica retorno
    assert result == retorno_webhook


def test_enviar_pagamento_webhook_retorna_none(use_case, mock_repository, mock_webhook_service):
    id_pedido = "XYZ999"
    valor = Decimal("10.00")
    mock_webhook_service.enviar.return_value = None

    result = use_case.execute(id_pedido, valor)

    # Deve salvar e tentar enviar mesmo assim
    assert mock_repository.save.call_count == 1
    assert mock_webhook_service.enviar.call_count == 1
    assert result is not None
    assert result.id_pagamento is not None
    assert result.status == "Desconhecido"
