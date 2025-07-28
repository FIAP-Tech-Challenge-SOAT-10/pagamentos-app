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

Na raiz do projeto, execute:

```bash
docker-compose up -d
```

Esse comando iniciará o LocalStack e criará automaticamente a fila `pagamento-events`.

### 2. Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
USE_LOCALSTACK=true
SQS_PAGAMENTO_URL=http://localhost:4566/000000000000/pagamento-events
```

> Certifique-se de que o código está carregando o `.env` com `dotenv.load_dotenv()` na inicialização da aplicação.

### 3. Rodar localmente

Com o LocalStack rodando, execute a aplicação localmente com Uvicorn:

```bash
uvicorn interfaces.lambda_function:app --reload
```

A aplicação estará disponível em `http://localhost:8000/v1`

### 4. Testar o envio de um pagamento

Faça uma requisição para criar um pagamento (como feito na AWS):

```bash
curl -X POST http://localhost:8000/v1/pagamentos/enviar \
  -H "Content-Type: application/json" \
  -d '{"id_pedido": "123456", "valor": 25.90}'
```

### 5. Verificar mensagens na fila

Após um `UPDATE` de pagamento ou confirmação, você pode verificar as mensagens publicadas no SQS:

```bash
awslocal sqs receive-message \
  --queue-url http://localhost:4566/000000000000/pagamento-events
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
