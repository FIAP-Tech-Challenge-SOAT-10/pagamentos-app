from decimal import Decimal
from pydantic import BaseModel, Field, validator
from datetime import datetime

class Pagamento(BaseModel):
    id_pagamento: int = Field(..., description="ID do pagamento")
    id_pedido: str = Field(..., description="ID do pedido associado ao pagamento")
    valor: Decimal = Field(..., description="Valor do pagamento")
    status: str = Field(..., description="Status do pagamento")
    data_criacao: datetime = Field(..., description="Data de criação do pagamento")

    @validator('valor')
    def valor_maior_que_zero(cls, v):
        if v <= 0:
            raise ValueError("O valor deve ser maior que zero")
        return v

class CriarPagamentoRequest(BaseModel):
    id_pedido: str = Field(..., description="ID do pedido")
    valor: Decimal = Field(..., description="Valor do pagamento")

    @validator('valor')
    def valor_maior_que_zero(cls, v):
        if v <= 0:
            raise ValueError("O valor deve ser maior que zero")
        return v
