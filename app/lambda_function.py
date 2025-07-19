from fastapi import FastAPI
from app.interfaces.api.routes import router
from mangum import Mangum

# Corrige o roteamento via API Gateway (stage "v1")
app = FastAPI(root_path="/v1")

# Rotas
app.include_router(router)

# def handler(event, context):
#     print("Event:", event)
#     print("Context:", context)
#     return {
#         "statusCode": 200,
#         "body": f'Debugging Lambda function: {event}, {context}'
#     }

# AWS Lambda handler
handler = Mangum(app)

