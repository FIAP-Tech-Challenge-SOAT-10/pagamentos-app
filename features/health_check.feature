Feature: Health check

  Scenario: Verificar se a API está online
    When eu faço uma requisição GET para "/health"
    Then a resposta deve conter status "200"
