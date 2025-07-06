from datetime import datetime
from pydantic import BaseModel, Field, validator

class Pagamento(BaseModel):
    id_pagamento: int = Field(..., description="ID do pagamento")
    id_pedido: str = Field(..., description="ID do pedido associado ao pagamento")
    valor: float = Field(..., description="Valor do pagamento")
    status: str = Field(..., description="Status do pagamento")
    data_criacao: datetime = Field(..., description="Data de criação do pagamento")

