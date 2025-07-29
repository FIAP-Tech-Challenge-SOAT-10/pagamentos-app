from datetime import datetime
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key
from typing import List, Optional
from app.domain.entities.pagamento import Pagamento
import os

class PagamentoRepository:
    def __init__(self, dynamodb_resource=None):
        if dynamodb_resource:
            self.dynamodb = dynamodb_resource
        else:
            if os.environ.get("USE_LOCALSTACK", "false").lower() == "true":
                self.dynamodb = boto3.resource(
                    "dynamodb",
                    endpoint_url="http://localhost:4566",
                    aws_access_key_id="fake_access_key",
                    aws_secret_access_key="fake_secret_key",
                    region_name="us-east-1",
                )
            else:
                self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table("pagamentos")
        print("🔗 Conectado à tabela DynamoDB:", self.table.name)
        
    def save(self, pagamento: Pagamento) -> Pagamento:
        """Salva um pagamento no DynamoDB"""
        self.table.put_item(
            Item={
                "id_pagamento": pagamento.id_pagamento,
                "id_pedido": pagamento.id_pedido,
                "status": pagamento.status,
                "valor": Decimal(str(pagamento.valor)),  # ✅ garantindo Decimal
                "data_criacao": pagamento.data_criacao.isoformat()  # ✅ datetime como string
            }
        )
        return pagamento

    def get_pagamento_by_id(self, pagamento_id: int) -> Optional[Pagamento]:
        print("🔍 Buscando pagamento com ID:", pagamento_id)

        response = self.table.get_item(Key={"id_pagamento": pagamento_id})
        item = response.get("Item")

        if not item:
            print("⚠️ Pagamento não encontrado no DynamoDB.")
            return None

        return Pagamento(
            id_pagamento=item["id_pagamento"],
            id_pedido=item["id_pedido"],
            status=item["status"],
            valor=Decimal(str(item["valor"])),  # ✅ garantindo tipo correto
            data_criacao=datetime.fromisoformat(item["data_criacao"])  # ✅ convertendo string → datetime
        )

    def get_all_pagamentos(self) -> List[Pagamento]:
        response = self.table.scan()
        items = response.get("Items", [])

        return [
            Pagamento(
                id_pagamento=item["id_pagamento"],
                id_pedido=item["id_pedido"],
                status=item["status"],
                valor=Decimal(str(item["valor"])),  # ✅
                data_criacao=datetime.fromisoformat(item["data_criacao"])  # ✅
            )
            for item in items
        ]

    def update_pagamento(self, pagamento: Pagamento) -> Pagamento:
        """Atualiza os dados de um pagamento"""
        self.table.update_item(
            Key={"id_pagamento": pagamento.id_pagamento},
            UpdateExpression=(
                "SET id_pedido = :id_pedido, #s = :status, "
                "valor = :valor, data_criacao = :data_criacao"
            ),
            ExpressionAttributeNames={
                "#s": "status"
            },
            ExpressionAttributeValues={
                ":id_pedido": pagamento.id_pedido,
                ":status": pagamento.status,
                ":valor": Decimal(str(pagamento.valor)),  # ✅
                ":data_criacao": pagamento.data_criacao.isoformat()  # ✅
            }
        )
        return pagamento
