# 💳 Pagamentos App

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=FIAP-Tech-Challenge-SOAT-10_pagamentos-app&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=FIAP-Tech-Challenge-SOAT-10_pagamentos-app)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=FIAP-Tech-Challenge-SOAT-10_pagamentos-app&metric=coverage)](https://sonarcloud.io/summary/new_code?id=FIAP-Tech-Challenge-SOAT-10_pagamentos-app)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=FIAP-Tech-Challenge-SOAT-10_pagamentos-app&metric=bugs)](https://sonarcloud.io/summary/new_code?id=FIAP-Tech-Challenge-SOAT-10_pagamentos-app)

API para processamento de pagamentos desenvolvida com **FastAPI**, utilizando arquitetura serverless com **AWS Lambda** e exposta via **API Gateway**.

---

## 🚀 Deploy

Para realizar o deploy da Lambda na AWS, execute o script abaixo:

```powershell
.\deploy.ps1
🧪 Teste da API
Você pode testar a API com o endpoint público:

URL: https://qjy8d5de2c.execute-api.us-east-1.amazonaws.com/v1/pagamentos/enviar

Método: POST

🔸 Exemplo de requisição:
{
  "id_pedido": "7598432",
  "valor": 43.20
}

🔸 Exemplo de resposta:
{
  "id_pagamento": 459371,
  "status": "Recebido"
}
A resposta indicará se o pagamento foi Recebido ou Negado, simulando o comportamento da integração com um sistema financeiro.

🛠 Tecnologias utilizadas
FastAPI

AWS Lambda

Amazon API Gateway

GitHub Actions

SonarCloud

Behave + coverage.py

📊 Qualidade de código
Este projeto utiliza o SonarCloud para verificar:

✅ Cobertura de testes

🐞 Bugs e vulnerabilidades

📐 Code smells

A Quality Gate está configurada para exigir no mínimo 70% de cobertura de testes na branch main.