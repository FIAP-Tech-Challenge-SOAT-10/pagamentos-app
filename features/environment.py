from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.lambda_function import app 


def before_all(context):
    context.dynamo_patch = patch("app.domain.repositories.pagamento_repository.boto3.resource")
    mock_resource = context.dynamo_patch.start()
    
    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = MagicMock()
    mock_resource.return_value = mock_dynamodb

    # Cliente da API
    context.client = TestClient(app)

def before_scenario(context, scenario):
    print(f"🚀 Iniciando cenário: {scenario.name}")

def after_scenario(context, scenario):
    print(f"✅ Finalizado cenário: {scenario.name}")

def after_all(context):
    context.dynamo_patch.stop()
    print("🔚 Testes concluídos, DynamoDB mock finalizado.")
