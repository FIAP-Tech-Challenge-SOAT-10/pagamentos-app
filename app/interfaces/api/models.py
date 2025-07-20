from decimal import Decimal
from pydantic import BaseModel, Field


class CriarPagamentoRequest(BaseModel):
    id_pedido: str = Field(..., description="ID do pedido")
    valor: Decimal = Field(..., description="Valor do pagamento (deve ser maior que 0)")

class PagamentoRequisicao(BaseModel):
    id_pagamento: int = Field(..., description="ID do pagamento")
    status: str = Field(..., description="Status do pagamento")

class PagamentoConfirmacao(BaseModel):
    id_pagamento: int = Field(..., description="ID do pagamento")
    status: str = Field(..., description="Novo status do pagamento")
