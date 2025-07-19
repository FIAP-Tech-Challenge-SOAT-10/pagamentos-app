import json
import os
from infrastructure.config.boto3_client import get_sqs_client

class SQSPublisher:
    def __init__(self):
        self.sqs = get_sqs_client()
        self.queue_url = os.environ.get("SQS_PAGAMENTO_URL")  # ex: http://localhost:4566/000000000000/pagamento-events

    def publish_pagamento_event(self, event_type: str, data: dict):
        message = {
            "event_type": event_type,
            "data": data
        }

        print("📤 Publicando mensagem no SQS:", message)

        response = self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message)
        )

        print("📬 Mensagem publicada. MessageId:", response.get("MessageId"))
