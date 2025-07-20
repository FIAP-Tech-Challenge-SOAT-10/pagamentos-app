from unittest.mock import MagicMock
from requests import patch
from fastapi.testclient import TestClient
from app.lambda_function import app  # ou o caminho real da sua instância FastAPI


def before_all(context):
    context.client = TestClient(app)
    context.dynamo_patch = patch("app.domain.repositories.pagamento_repository.boto3.resource")
    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = MagicMock()
    context.dynamo_patch.start().return_value = mock_dynamodb

def before_scenario(context, scenario):
    print(f"🚀 Iniciando cenário: {scenario.name}")

def after_scenario(context, scenario):
    print(f"✅ Finalizado cenário: {scenario.name}")

def after_all(context):
    context.dynamo_patch.stop()
    print("🔚 Testes concluídos, DynamoDB mock finalizado.")
