Feature: Envio de pagamento

  Scenario: Enviar um pagamento com valor válido
    Given que existe um pedido com ID "123"
    And um valor de pagamento de 150.75
    When eu executo o caso de uso de envio de pagamento
    Then o pagamento deve ser confirmado com status "Recebido"
