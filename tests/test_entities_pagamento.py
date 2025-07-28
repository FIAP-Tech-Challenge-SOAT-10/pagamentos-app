import pytest
from decimal import Decimal
from datetime import datetime
from app.domain.entities.pagamento import Pagamento, CriarPagamentoRequest
from pydantic import ValidationError

def test_pagamento_valido():
    pagamento = Pagamento(
        id_pagamento=1,
        id_pedido="pedido123",
        valor=Decimal("150.00"),
        status="Pendente",
        data_criacao=datetime(2023, 10, 1, 12, 0)
    )
    assert pagamento.id_pagamento == 1
    assert pagamento.valor == Decimal("150.00")

def test_pagamento_valor_invalido():
    with pytest.raises(ValidationError) as exc:
        Pagamento(
            id_pagamento=2,
            id_pedido="pedido123",
            valor=Decimal("0.00"),
            status="Pendente",
            data_criacao=datetime.now()
        )
    assert "O valor deve ser maior que zero" in str(exc.value)

def test_pagamento_campos_obrigatorios():
    with pytest.raises(ValidationError) as exc:
        Pagamento()  # falta tudo
    assert "id_pagamento" in str(exc.value)
    assert "id_pedido" in str(exc.value)
    assert "valor" in str(exc.value)

def test_criar_pagamento_request_valido():
    req = CriarPagamentoRequest(id_pedido="pedido456", valor=Decimal("10.50"))
    assert req.id_pedido == "pedido456"

def test_criar_pagamento_request_valor_invalido():
    with pytest.raises(ValidationError) as exc:
        CriarPagamentoRequest(id_pedido="pedido456", valor=Decimal("-5.00"))
    assert "O valor deve ser maior que zero" in str(exc.value)

def test_criar_pagamento_request_faltando_campos():
    with pytest.raises(ValidationError) as exc:
        CriarPagamentoRequest()
    assert "id_pedido" in str(exc.value)
    assert "valor" in str(exc.value)

