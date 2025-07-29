from app.interfaces.api.models import PagamentoConfirmacao
from app.domain.entities.pagamento import Pagamento
from app.infrastructure.services.webhook_service import WebhookService
from datetime import datetime
from decimal import Decimal
import random
from app.interfaces.api.models import PagamentoConfirmacao
from pydantic import BaseModel, Field, validator
from app.domain.entities.pagamento import Pagamento
from app.infrastructure.repositories.pagamento_repository import PagamentoRepository
import requests
import secrets
from app.infrastructure.queue.publisher import SQSPublisher 

class EnviarPagamentoUseCase:
    def __init__(
        self,
        pagamento_repository: PagamentoRepository,
        webhook_service: WebhookService
    ):
        self.pagamento_repository = pagamento_repository
        self.webhook_service = webhook_service
        self.publisher = SQSPublisher()

    def execute(self, id_pedido: str, valor: Decimal) -> PagamentoConfirmacao | None:
        id_pagamento = secrets.randbelow(900000) + 100000  # int seguro de 6 dígitos

        pagamento = Pagamento(
            id_pagamento=id_pagamento,
            id_pedido=id_pedido,
            valor=valor,
            status="Pendente",
            data_criacao=datetime.now()
        )

        self.pagamento_repository.save(pagamento)

        self.publisher.publish_pagamento_event("pagamento_criado", pagamento.dict())

        confirmacao = self.webhook_service.enviar(pagamento)
        if confirmacao is None:
            # Retorna um objeto padrão com status de erro ou pendente
            return PagamentoConfirmacao(
                id_pagamento=pagamento.id_pagamento,
                status="Desconhecido"
            )
        return confirmacao
