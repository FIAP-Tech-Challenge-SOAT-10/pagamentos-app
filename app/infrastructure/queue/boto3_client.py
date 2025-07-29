import boto3
import os

def get_sqs_client():
    if os.environ.get("USE_LOCALSTACK", "false").lower() == "true":
        return boto3.client(
            "sqs",
            region_name="us-east-1",
            endpoint_url="http://localhost:4566",
            aws_access_key_id="fake",
            aws_secret_access_key="fake"
        )
    else:
        return boto3.client("sqs")
