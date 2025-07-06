from datetime import datetime
import random
from pydantic import BaseModel, Field, validator
from domain.entities.pagamento import Pagamento
from domain.repositories.pagamento_repository import PagamentoRepository


class EnviarPagamentoUseCase:
    def __init__(self, pagamento_repository: PagamentoRepository):
        self.pagamento_repository = pagamento_repository

    def execute(self, id_pedido: str, valor: float) -> Pagamento:
        pagamento = Pagamento(
            id_pagamento=random.randint(100000, 999999),  # Gerando um ID único para o pagamento
            id_pedido=id_pedido,
            valor=valor, 
            status="Pendente",
            data_criacao=datetime.now()
        )

        self.pagamento_repository.save(pagamento)

        import requests
        # Simulando o envio do pagamento para um gateway externo
        response = requests.post(
            "https://api.exemplo.com/pagamentos",
            json={
                "id_pagamento": pagamento.id_pagamento,
                "id_pedido": pagamento.id_pedido,
                "valor": pagamento.valor,
                "status": pagamento.status,
                "data_criacao": pagamento.data_criacao.isoformat()
            }
        )
        
        return pagamento