Feature: Envio de webhook de pagamento

  Scenario: Webhook responde com sucesso
    Given um pagamento válido
    And o webhook responde com status 200 e dados válidos
    When o serviço de webhook é executado
    Then o pagamento deve ser confirmado com status "Recebido"

  Scenario: Webhook responde com erro
    Given um pagamento válido
    And o webhook responde com status 500
    When o serviço de webhook é executado
    Then nenhuma confirmação de pagamento deve ser retornada

  Scenario: Webhook gera uma exceção
    Given um pagamento válido
    And o webhook lança uma exceção
    When o serviço de webhook é executado
    Then nenhuma confirmação de pagamento deve ser retornada
