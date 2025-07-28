Feature: Validação das entidades de pagamento

  Scenario: Criar Pagamento com dados válidos
    Given um payload de Pagamento válido
    When eu tento criar o objeto Pagamento
    Then o objeto deve ser criado com sucesso

  Scenario: Criar Pagamento com valor negativo
    Given um payload de Pagamento com valor -10.0
    When eu tento criar o objeto Pagamento
    Then deve ocorrer um erro de validação com a mensagem "O valor deve ser maior que zero"

  Scenario: Criar Pagamento com campo faltando
    Given um payload de Pagamento sem campo obrigatório "status"
    When eu tento criar o objeto Pagamento
    Then deve ocorrer um erro de validação com a mensagem "field required"

  Scenario: Criar CriarPagamentoRequest com dados válidos
    Given um payload de CriarPagamentoRequest com valor 100.0
    When eu tento criar o objeto CriarPagamentoRequest
    Then o objeto deve ser criado com sucesso

  Scenario: Criar CriarPagamentoRequest com valor zero
    Given um payload de CriarPagamentoRequest com valor 0
    When eu tento criar o objeto CriarPagamentoRequest
    Then deve ocorrer um erro de validação com a mensagem "O valor deve ser maior que zero"
