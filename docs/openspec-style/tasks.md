# Tasks: Detecção de chamados duplicados/reabertos

- [x] 1. Definir schema de dados de entrada (cliente_id, tema, timestamp)
- [x] 2. Implementar busca do chamado anterior do mesmo cliente na janela
- [x] 3. Implementar regra de classificação por tema (TÉCNICO x ADM)
- [x] 4. Implementar vínculo chamado_pai_id para reaberturas
- [x] 5. Escrever testes cobrindo: chamado novo, reabertura técnica,
      repetição ADM (caso de borda), limite exato da janela
- [x] 6. Validar contra dataset fictício e revisar diff antes de aceitar
