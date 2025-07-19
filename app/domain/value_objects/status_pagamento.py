from enum import Enum

class StatusPagamento(str, Enum):
    PENDENTE = "Pendente"
    RECEBIDO = "Recebido"
    NEGADO = "Negado"
