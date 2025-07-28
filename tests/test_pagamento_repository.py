import pytest
from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock
from app.domain.entities.pagamento import Pagamento
from app.domain.repositories.pagamento_repository import PagamentoRepository


@pytest.fixture
def mock_dynamodb():
    mock_resource = MagicMock()
    mock_table = MagicMock()
    mock_resource.Table.return_value = mock_table
    return mock_resource, mock_table


@pytest.fixture
def pagamento_sample():
    return Pagamento(
        id_pagamento=123456,
        id_pedido="pedido-xyz",
        status="Pendente",
        valor=Decimal("199.99"),
        data_criacao=datetime.now()
    )


def test_save_pagamento(mock_dynamodb, pagamento_sample):
    mock_resource, mock_table = mock_dynamodb
    repo = PagamentoRepository(dynamodb_resource=mock_resource)
    result = repo.save(pagamento_sample)
    mock_table.put_item.assert_called_once()
    assert result == pagamento_sample


def test_get_pagamento_by_id_found(mock_dynamodb, pagamento_sample):
    mock_resource, mock_table = mock_dynamodb
    mock_table.get_item.return_value = {
        "Item": {
            "id_pagamento": pagamento_sample.id_pagamento,
            "id_pedido": pagamento_sample.id_pedido,
            "status": pagamento_sample.status,
            "valor": str(pagamento_sample.valor),
            "data_criacao": pagamento_sample.data_criacao.isoformat()
        }
    }
    repo = PagamentoRepository(dynamodb_resource=mock_resource)
    result = repo.get_pagamento_by_id(pagamento_sample.id_pagamento)
    assert isinstance(result, Pagamento)
    assert result.id_pagamento == pagamento_sample.id_pagamento


def test_get_pagamento_by_id_not_found(mock_dynamodb):
    mock_resource, mock_table = mock_dynamodb
    mock_table.get_item.return_value = {}
    repo = PagamentoRepository(dynamodb_resource=mock_resource)
    result = repo.get_pagamento_by_id(999999)
    assert result is None


def test_get_all_pagamentos(mock_dynamodb, pagamento_sample):
    mock_resource, mock_table = mock_dynamodb
    mock_table.scan.return_value = {
        "Items": [{
            "id_pagamento": pagamento_sample.id_pagamento,
            "id_pedido": pagamento_sample.id_pedido,
            "status": pagamento_sample.status,
            "valor": str(pagamento_sample.valor),
            "data_criacao": pagamento_sample.data_criacao.isoformat()
        }]
    }
    repo = PagamentoRepository(dynamodb_resource=mock_resource)
    result = repo.get_all_pagamentos()
    assert isinstance(result, list)
    assert isinstance(result[0], Pagamento)
    assert result[0].id_pagamento == pagamento_sample.id_pagamento


def test_update_pagamento(mock_dynamodb, pagamento_sample):
    mock_resource, mock_table = mock_dynamodb
    repo = PagamentoRepository(dynamodb_resource=mock_resource)
    result = repo.update_pagamento(pagamento_sample)
    mock_table.update_item.assert_called_once()
    assert result == pagamento_sample
