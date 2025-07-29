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
```


---

## 🧪 Teste da API
Você pode testar a API com o endpoint público:

Endpoint: https://qjy8d5de2c.execute-api.us-east-1.amazonaws.com/v1/pagamentos/enviar

Método: POST

🔸 Exemplo de requisição:
```json
{
  "id_pedido": "7598432",
  "valor": 43.20
}
```

🔸 Exemplo de resposta:
```json
{
  "id_pagamento": 459371,
  "status": "Recebido"
}
```

A resposta indicará se o pagamento foi Recebido ou Negado, simulando o comportamento da integração com um sistema financeiro.

---

## 🛠 Tecnologias utilizadas


* FastAPI

* AWS Lambda

* Amazon API Gateway

* GitHub Actions

* SonarCloud

* Behave + coverage.py

---

## 📊 Qualidade de código

Este projeto utiliza o SonarCloud para verificar:

✅ Cobertura de testes

🐞 Bugs e vulnerabilidades

📐 Code smells

A Quality Gate está configurada para exigir no mínimo 70% de cobertura de testes na branch main.

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

No diretório do projeto, rode:

```bash
docker-compose up -d
```

Isso irá subir o container do LocalStack simulando os serviços AWS (SQS, DynamoDB).

---

## 2. Criando recursos AWS (Fila SQS e Tabela DynamoDB) manualmente

### 2.1 Acessar o container LocalStack

```bash
docker exec -it localstack bash
```

### 2.2 Criar a fila SQS

```bash
awslocal sqs create-queue --queue-name pagamento-events
```

Saída esperada:

```json
{
  "QueueUrl": "http://localhost:4566/000000000000/pagamento-events"
}
```

### 2.3 Criar a tabela DynamoDB

```bash
awslocal dynamodb create-table \
  --table-name pagamentos \
  --attribute-definitions AttributeName=id_pagamento,AttributeType=N \
  --key-schema AttributeName=id_pagamento,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

Saída esperada (informa que a tabela está sendo criada):

```json
{
  "TableDescription": {
    "TableStatus": "CREATING",
    ...
  }
}
```

### 2.4 Confirmar que recursos foram criados

```bash
awslocal sqs list-queues
# Deve listar a fila pagamento-events

awslocal dynamodb list-tables
# Deve listar a tabela pagamentos
```

---

## 3. Configurar variáveis de ambiente para a aplicação

No arquivo `.env` (ou exportando no terminal), configure:

```
USE_LOCALSTACK=true
PAGAMENTO_QUEUE_URL=http://localhost:4566/000000000000/pagamento-events
AWS_ACCESS_KEY_ID=fake
AWS_SECRET_ACCESS_KEY=fake
AWS_DEFAULT_REGION=us-east-1
```

---

## 4. Rodar a aplicação FastAPI localmente

```bash
uvicorn app.lambda_function:app --reload
```

---

## 5. Testar envio de pagamento via API

Com o FastAPI rodando, execute:

```bash
curl -X POST http://localhost:8000/v1/pagamentos/enviar \
  -H "Content-Type: application/json" \
  -d '{"id_pedido": "abc123", "valor": 150.00}'
```

Resposta esperada: objeto JSON com confirmação do pagamento.

---

## 6. Verificar mensagens publicadas na fila SQS

Ainda dentro do container LocalStack, execute:

```bash
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/pagamento-events
```

Você verá as mensagens publicadas, com o evento `"pagamento_criado"` e os dados do pagamento.

---

## 7. Parar e limpar ambiente LocalStack (opcional)

Para parar e remover containers e volumes, rode:

```bash
docker-compose down -v
```

### Estrutura de publicação de eventos

Quando um pagamento é confirmado, o evento publicado segue o formato:

```json
{
  "event_type": "pagamento_confirmado",
  "data": {
    "id_pagamento": 459371,
    "id_pedido": "7598432",
    "valor": 43.2,
    "status": "Confirmado",
    "data_criacao": "2025-07-19T13:32:00"
  }
}
```

Outros microsserviços podem consumir essa fila e sincronizar seus próprios bancos de dados sem depender diretamente do serviço de pagamentos.
