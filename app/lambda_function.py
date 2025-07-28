from fastapi import FastAPI
from app.interfaces.api.routes import router
from mangum import Mangum
from dotenv import load_dotenv
load_dotenv()

# Corrige o roteamento via API Gateway (stage "v1")
app = FastAPI(root_path="/v1")

# Rotas
app.include_router(router)
# Configuração do Mangum para AWS Lambda
# Isso permite que o FastAPI funcione como um handler para AWS Lambda
# AWS Lambda handler
handler = Mangum(app)

