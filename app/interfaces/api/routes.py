from app.infrastructure.services.webhook_service import WebhookService
from fastapi import APIRouter, HTTPException
from app.interfaces.api.models import PagamentoConfirmacao, CriarPagamentoRequest
from app.application.use_cases.enviar_pagamento import EnviarPagamentoUseCase
from app.application.use_cases.confirmar_pagamento import confirmar_pagamento
from app.domain.repositories.pagamento_repository import PagamentoRepository
import traceback

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Endpoint de verificação de disponibilidade da API.
    """
    return {"status": "ok"}


@router.post("/pagamentos/enviar", response_model=PagamentoConfirmacao)
async def enviar_pagamento(request: CriarPagamentoRequest):
    try:
        repo = PagamentoRepository()  
        webhook = WebhookService()
        use_case = EnviarPagamentoUseCase(repo, webhook)

        print("🟡 Requisição recebida:", request)
        pagamento = use_case.execute(request.id_pedido, request.valor)
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

        repo = PagamentoRepository() 
        use_case = confirmar_pagamento(repo)

        print("🔄 Chamando use_case.execute...")
        pagamento_confirmado = use_case.execute(
            pagamento.id_pagamento,
            pagamento.status
        )

        print("✅ Pagamento atualizado:", pagamento_confirmado)
        return PagamentoConfirmacao(
            id_pagamento=pagamento_confirmado.id_pagamento,
            status=pagamento_confirmado.status
        )

    except ValueError as e:
        print("⚠️ ValueError:", str(e))
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        print("❌ ERRO INTERNO:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
