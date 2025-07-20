import requests
from app.domain.entities.pagamento import Pagamento
from app.interfaces.api.models import PagamentoConfirmacao

class WebhookService:
    def enviar(self, pagamento: Pagamento) -> PagamentoConfirmacao | None:
        payload = {
            "id_pagamento": pagamento.id_pagamento,
            "valor": float(pagamento.valor),
            "status": pagamento.status,
            "data_criacao": pagamento.data_criacao.isoformat()
        }

        try:
            response = requests.post(
                "https://vk45ivvi9k.execute-api.us-east-1.amazonaws.com/v1/pagamento",
                json=payload,
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return PagamentoConfirmacao(
                    id_pagamento=data.get("id_pagamento"),
                    status=data.get("status", "Desconhecido")
                )
        except Exception as e:
            print("❌ Erro ao enviar webhook:", str(e))
        return None
# This service handles the communication with the external webhook endpoint.
# It prepares the payload from the Pagamento entity and sends it as a POST request.