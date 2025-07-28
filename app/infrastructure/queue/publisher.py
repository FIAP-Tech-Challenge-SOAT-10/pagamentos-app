import json
from decimal import Decimal
from datetime import datetime

from app.infrastructure.queue.boto3_client import get_sqs_client

import os

class SQSPublisher:
    def __init__(self):
        self.client = get_sqs_client()
        self.queue_url = os.environ.get("PAGAMENTO_QUEUE_URL")

    def publish_pagamento_event(self, event_type: str, data: dict):
        message = {
            "event_type": event_type,
            "data": data,
        }

        def default_serializer(obj):
            if isinstance(obj, Decimal):
                return str(obj)
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

        print("📤 Publicando mensagem no SQS:", message)

        self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message, default=default_serializer),
        )
