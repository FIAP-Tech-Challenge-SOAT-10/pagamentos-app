from app.interfaces.api.models import PagamentoConfirmacao
from app.domain.entities.pagamento import Pagamento
from app.domain.repositories.pagamento_repository import PagamentoRepository
from app.infrastructure.services.webhook_service import WebhookService
from datetime import datetime
from decimal import Decimal
import random

class EnviarPagamentoUseCase:
    def __init__(
        self,
        pagamento_repository: PagamentoRepository,
        webhook_service: WebhookService
    ):
        self.pagamento_repository = pagamento_repository
        self.webhook_service = webhook_service

    def execute(self, id_pedido: str, valor: Decimal) -> PagamentoConfirmacao | None:
        pagamento = Pagamento(
            id_pagamento=random.randint(100000, 999999),
            id_pedido=id_pedido,
            valor=valor,
            status="Pendente",
            data_criacao=datetime.now()
        )

        self.pagamento_repository.save(pagamento)

        return self.webhook_service.enviar(pagamento)
