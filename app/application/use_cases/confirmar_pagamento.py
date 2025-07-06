class confirmar_pagamento:
    def __init__(self, pagamento_repository):
        self.pagamento_repository = pagamento_repository

    def execute(self, pagamento_id: int, novo_status: str):
        pagamento = self.pagamento_repository.get_pagamento_by_id(pagamento_id)
        if not pagamento:
            raise ValueError("Pagamento não encontrado")

        # ✅ Pydantic v1: use .copy(update={...})
        pagamento_atualizado = pagamento.copy(update={"status": novo_status})
        self.pagamento_repository.update_pagamento(pagamento_atualizado)
        return pagamento_atualizado
