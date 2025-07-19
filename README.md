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

## Microsserviços e comunicação via SQS

Este serviço faz parte de uma arquitetura de microsserviços e é responsável pelo processamento de pagamentos. Para garantir o isolamento dos bancos e comunicação entre serviços, utilizamos **mensageria via AWS SQS**.

Sempre que um pagamento é confirmado ou criado, o serviço publica um **evento JSON** na fila `pagamento-events`, que poderá ser consumido por outros microsserviços, como Pedido ou Produção.

---

## Execução local com LocalStack

Para testar o serviço localmente com a simulação da fila SQS, siga os passos abaixo.

### Pré-requisitos

- Docker
- Python 3.10+
- AWS CLI
- [awslocal](https://github.com/localstack/awscli-local) (ou use `aws --endpoint-url` manualmente)

### 1. Subir o ambiente com LocalStack

Na raiz do projeto, execute:

```bash
docker-compose up -d
