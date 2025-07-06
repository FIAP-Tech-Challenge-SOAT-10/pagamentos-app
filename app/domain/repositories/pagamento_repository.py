from typing import List, Optional
from domain.entities.pagamento import Pagamento


class PagamentoRepository:
    def __init__(self):
        # In-memory storage for demo purposes
        # In a real application, this would connect to a database
        self._pagamentos: List[Pagamento] = []
    
    def save(self, pagamento: Pagamento) -> Pagamento:
        """Salva um pagamento no repositório"""
        self._pagamentos.append(pagamento)
        return pagamento
    
    def get_pagamento_by_id(self, pagamento_id: int) -> Optional[Pagamento]:
        """Busca um pagamento pelo ID"""
        for pagamento in self._pagamentos:
            if pagamento.id_pagamento == pagamento_id:
                return pagamento
        return None
    
    def get_all_pagamentos(self) -> List[Pagamento]:
        """Retorna todos os pagamentos"""
        return self._pagamentos.copy()
    
    def update(self, pagamento: Pagamento) -> Pagamento:
        """Atualiza um pagamento existente"""
        for i, p in enumerate(self._pagamentos):
            if p.id_pagamento == pagamento.id_pagamento:
                self._pagamentos[i] = pagamento
                return pagamento
        raise ValueError(f"Pagamento com ID {pagamento.id_pagamento} não encontrado")
