Feature: Confirmação de pagamento

  Scenario: Atualizar status de um pagamento existente
    Given que existe um pagamento com id 123456 e status "Pendente"
    When eu atualizo o status para "Recebido"
    Then o status do pagamento deve ser "Recebido"

  Scenario: Tentar atualizar um pagamento inexistente
    Given que não existe pagamento com id 999999
    When eu tento atualizar o status para "Recebido"
    Then uma exceção deve ser lançada com a mensagem "Pagamento não encontrado"
