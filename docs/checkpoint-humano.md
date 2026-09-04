# Checkpoint humano — Etapa 4

## Checkpoint definido
**Antes de mesclar/commitar qualquer alteração em `rules/dedup.py` (motor de
regras de reabertura x chamado novo) no branch principal**, é obrigatória a
revisão humana do resultado do pipeline rodado sobre o CSV fictício (não só
a leitura do código).

### Por que este é o checkpoint certo para este projeto
Diferente de `rules/sla.py` (cujo erro só afeta a cor/etiqueta de um chamado
individual), um erro em `rules/dedup.py` muda a **contagem** de chamados
novos vs. reaberturas — número que vai direto para o relatório de gestão.
Um bug aqui é silencioso: o pipeline roda sem erro, os testes existentes
podem passar, e o número errado só aparece quando alguém olha o relatório
final e desconfia dele.

## Simulação do checkpoint
- **Ponto de parada:** após implementar a Tarefa 7 do plano (regra de
  reabertura técnico x ADM) e antes de considerar a Etapa 3 concluída.
- **O que foi observado:** ao rodar o pipeline sobre os dados fictícios, o
  chamado 1009 apareceu como reabertura de um chamado já resolvido há
  exatamente 24h (detalhe completo em `docs/revisao-diff.md`).
- **Decisão tomada:** **editar** — não foi "aprovar como está" (o
  comportamento na borda da janela não estava claramente coberto pela regra
  combinada) nem "rejeitar e voltar à especificação" (não era um erro de
  entendimento da regra, era um detalhe de implementação do limite da
  janela). Corrigi o limite inferior da janela para exclusivo, adicionei um
  teste de regressão, e documentei separadamente a questão do status do
  chamado original como decisão de escopo não resolvida nesta rodada.
- **Papel humano assumido:** revisor técnico-de-negócio — não bastava ler o
  código, foi preciso rodar o pipeline e questionar se o número que ele
  produzia fazia sentido para quem vai usar o relatório.
