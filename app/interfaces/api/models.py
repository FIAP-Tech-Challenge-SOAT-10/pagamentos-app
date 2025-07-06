from pydantic import BaseModel, Field
from datetime import datetime

class CriarPagamentoRequest(BaseModel):
    id_pedido: str = Field(..., description="ID do pedido")
    valor: float = Field(..., gt=0, description="Valor do pagamento (deve ser maior que 0)")

class PagamentoRequisicao(BaseModel):
    id_pagamento: int = Field(..., description="ID do pagamento")

class PagamentoConfirmacao(BaseModel):
    id_pagamento: int = Field(..., description="ID do pagamento")
    status: str = Field(..., description="Novo status do pagamento")
