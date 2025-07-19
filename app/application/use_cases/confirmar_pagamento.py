from infrastructure.queue.publisher import SQSPublisher 

class confirmar_pagamento:
    def __init__(self, pagamento_repository):
        self.pagamento_repository = pagamento_repository
        self.publisher = SQSPublisher()

    def execute(self, pagamento_id: int, novo_status: str):
        pagamento = self.pagamento_repository.get_pagamento_by_id(pagamento_id)
        if not pagamento:
            raise ValueError("Pagamento não encontrado")

        pagamento_atualizado = pagamento.copy(update={"status": novo_status})
        self.pagamento_repository.update_pagamento(pagamento_atualizado)

        self.publisher.publish_pagamento_event("pagamento_atualizado", pagamento_atualizado.dict())

        return pagamento_atualizado
