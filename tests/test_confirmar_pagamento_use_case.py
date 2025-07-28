import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from app.application.use_cases.confirmar_pagamento import confirmar_pagamento
from app.domain.entities.pagamento import Pagamento

@pytest.fixture
def pagamento_exemplo():
    return Pagamento(
        id_pagamento=1,
        id_pedido="123",
        status="pendente",
        data_criacao="2023-10-01T12:00:00",
        valor=Decimal("100.00")
    )

@pytest.fixture
def mock_repository(pagamento_exemplo):
    repo = MagicMock()
    repo.get_pagamento_by_id.return_value = pagamento_exemplo
    return repo

@pytest.fixture
def use_case(mock_repository):
    with patch("app.application.use_cases.confirmar_pagamento.SQSPublisher") as mock_publisher:
        return confirmar_pagamento(mock_repository)

def test_confirmar_pagamento_sucesso(use_case, mock_repository, pagamento_exemplo):
    novo_status = "confirmado"
    resultado = use_case.execute(pagamento_id=1, novo_status=novo_status)
    
    assert resultado.status == novo_status
    mock_repository.get_pagamento_by_id.assert_called_once_with(1)
    mock_repository.update_pagamento.assert_called_once()
    assert mock_repository.update_pagamento.call_args[0][0].status == novo_status

def test_confirmar_pagamento_pagamento_nao_encontrado():
    repo = MagicMock()
    repo.get_pagamento_by_id.return_value = None

    with patch("app.application.use_cases.confirmar_pagamento.SQSPublisher"):
        use_case = confirmar_pagamento(repo)

    with pytest.raises(ValueError, match="Pagamento não encontrado"):
        use_case.execute(pagamento_id=999, novo_status="confirmado")
