import sys
import os

# Remover lambda_package do path para evitar conflito com boto3/botocore
lambda_package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../lambda_package"))
if lambda_package_path in sys.path:
    sys.path.remove(lambda_package_path)
