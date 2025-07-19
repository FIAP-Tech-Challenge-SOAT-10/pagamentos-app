from fastapi import APIRouter, HTTPException
from interfaces.api.models import PagamentoRequisicao, PagamentoConfirmacao, CriarPagamentoRequest
from application.use_cases.enviar_pagamento import EnviarPagamentoUseCase
from application.use_cases.confirmar_pagamento import confirmar_pagamento
from infrastructure.repositories.pagamento_repository import PagamentoRepository
import traceback

router = APIRouter()

# Instâncias de repositório e casos de uso
repo = PagamentoRepository()
enviar_pagamento_use_case = EnviarPagamentoUseCase(repo)

@router.get("/health")
async def health_check():
    """
    Endpoint de verificação de disponibilidade da API.
    """
    return {"status": "ok"}

@router.post("/pagamentos/enviar", response_model=PagamentoConfirmacao)  
async def enviar_pagamento(request: CriarPagamentoRequest):
    try:
        print("🟡 Requisição recebida:", request)
        pagamento = enviar_pagamento_use_case.execute(request.id_pedido, request.valor)
        print("🟢 Pagamento criado:", pagamento)
        return pagamento
    except Exception as e:
        print("🔴 Erro interno:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro interno ao registrar pagamento {str(e)}")
    
@router.post("/pagamentos/confirmar", response_model=PagamentoConfirmacao)
async def confirmar_pagamento_endpoint(pagamento: PagamentoConfirmacao):
    try:
        print("📥 Requisição recebida:", pagamento)

        use_case = confirmar_pagamento(repo)
        print("🔄 Chamando use_case.execute...")

        pagamento_confirmado = use_case.execute(
            pagamento.id_pagamento,
            pagamento.status
        )

        print("✅ Pagamento atualizado:", pagamento_confirmado)
        print("🔍 Detalhes:", vars(pagamento_confirmado))

        return PagamentoConfirmacao(
            id_pagamento=pagamento_confirmado.id_pagamento,
            status=pagamento_confirmado.status
        )

    except ValueError as e:
        print("⚠️ ValueError:", str(e))
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        import traceback
        print("❌ ERRO INTERNO:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
