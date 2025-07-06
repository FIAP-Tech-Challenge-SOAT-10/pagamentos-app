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
        pagamento = Pagamento(id_pagamento=pagamento_id, id_pedido=1234, status="Pendente", valor=100, data_criacao='20250101')
        return pagamento 

    
    def get_all_pagamentos(self) -> List[Pagamento]:
        """Retorna todos os pagamentos"""
        return self._pagamentos.copy()
    
    def update_pagamento(self, pagamento: Pagamento) -> Pagamento:
 
        return pagamento

