from fastapi.testclient import TestClient
from app.lambda_function import app  # ou o caminho real da sua instância FastAPI


def before_all(context):
    context.client = TestClient(app)

def before_scenario(context, scenario):
    print(f"🚀 Iniciando cenário: {scenario.name}")

def after_scenario(context, scenario):
    print(f"✅ Finalizado cenário: {scenario.name}")

