Feature: Operações com o repositório de pagamento

  Scenario: Salvar um novo pagamento
    Given um pagamento válido chega ao sistema
    When eu salvar o pagamento
    Then o pagamento deve ser retornado com sucesso

  Scenario: Buscar um pagamento existente
    Given um pagamento com ID 123456 existe no banco
    When eu buscar o pagamento pelo ID
    Then o pagamento deve ser retornado

  Scenario: Buscar um pagamento inexistente
    Given nenhum pagamento com ID 999999 existe no banco
    When eu buscar o pagamento pelo ID
    Then nenhum pagamento deve ser encontrado

  Scenario: Atualizar um pagamento existente
    Given um pagamento válido chega ao sistema
    When eu atualizar o pagamento
    Then o pagamento deve ser atualizado com sucesso
