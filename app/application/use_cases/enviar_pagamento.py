from datetime import datetime
from decimal import Decimal
import random
from interfaces.api.models import PagamentoConfirmacao
from pydantic import BaseModel, Field, validator
from domain.entities.pagamento import Pagamento
from infrastructure.repositories.pagamento_repository import PagamentoRepository
import requests

class EnviarPagamentoUseCase:
    def __init__(self, pagamento_repository: PagamentoRepository):
        self.pagamento_repository = pagamento_repository

    def execute(self, id_pedido: str, valor: Decimal) -> Pagamento:
        # ✅ Criando o pagamento com datetime e decimal corretamente
        pagamento = Pagamento(
            id_pagamento=random.randint(100000, 999999),
            id_pedido=id_pedido,
            valor=valor,
            status="Pendente",
            data_criacao=datetime.now()  # armazena como datetime (converteremos depois)
        )

        # ✅ Salvando no DynamoDB (assumindo que o repositório converte .isoformat() e Decimal)
        self.pagamento_repository.save(pagamento)

        self.publisher.publish_pagamento_event("pagamento_criado", pagamento.dict())

        # ✅ Preparando o payload do webhook
        webhook_payload = {
            "id_pagamento": pagamento.id_pagamento,
            "valor": float(pagamento.valor),  # Enviar como float (webhook pode não aceitar Decimal)
            "status": pagamento.status,
            "data_criacao": pagamento.data_criacao.isoformat()  # datetime → string
        }

        print("📤 Enviando webhook:", webhook_payload)

        try:
            response = requests.post(
                "https://vk45ivvi9k.execute-api.us-east-1.amazonaws.com/v1/pagamento",
                json=webhook_payload,
                timeout=5
            )
            print("📥 Resposta do webhook:", response.status_code, response.text)

            if response.status_code == 200:
                # ✅ Extrai os dados do corpo JSON da resposta
                response_data = response.json()

                # ✅ Cria o objeto PagamentoConfirmacao com os dados do webhook
                response_pagamento = PagamentoConfirmacao(
                    id_pagamento=response_data.get("id_pagamento"),
                    status=response_data.get("status", "Desconhecido")
                )
                return response_pagamento
            else:
                return None

        except Exception as e:
            print("❌ Falha ao enviar webhook:", str(e))
            return None
        
