# Pagamentos App

API para processamento de pagamentos desenvolvida com FastAPI e deploy para AWS Lambda.

## Deploy

É possível subir a lambda para a AWS rodando o script:

```powershell
.\deploy.ps1
```

## Teste da API

Para testar o código é só utilizar esse endpoint exposto via API Gateway:

**Endpoint:** `https://qjy8d5de2c.execute-api.us-east-1.amazonaws.com/v1/pagamentos/enviar`

**Método:** POST

**Exemplo de requisição:**

```json
{
  "id_pedido": "7598432",
  "valor": 43.20
}
```

**Exemplo de resposta:**

```json
{
  "id_pagamento": 459371,
  "status": "Recebido"
}
```

A resposta indicará se o pagamento foi recebido ou negado.