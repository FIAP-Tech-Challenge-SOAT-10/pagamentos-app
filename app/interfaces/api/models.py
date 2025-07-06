from pydantic import BaseModel, Field
from datetime import datetime

class PagamentoRequisicao(BaseModel):
    id_pagamento: int = Field(..., description="ID do pagamento")

class PagamentoConfirmacao(BaseModel):
    id_pagamento: int = Field(..., description="ID do pagamento")
    status: str = Field(..., description="Novo status do pagamento")
