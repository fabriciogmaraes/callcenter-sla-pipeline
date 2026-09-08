# Etapa 3 — Checkpoint humano obrigatório

## Checkpoint definido
**Antes de fazer merge da branch de trabalho (`harness-arquitetura`) para
`main`.** Nenhum merge para `main` acontece sem uma revisão humana explícita
do que foi acumulado na branch — diferente do guardrail automatizado da
Etapa 1 (que roda a cada commit, sem intervenção), este é um ponto de
parada manual, único, antes da integração final.

## Simulação do checkpoint
Ao chegar ao fim das Etapas 1-6 desta atividade, a execução foi
interrompida antes de qualquer merge para `main`. Resumo apresentado para
decisão:

- 2 guardrails/funcionalidades novas (`validacao.py`, `urgencia.py`,
  `resumo.py`) com 6 testes novos, suíte completa em 15 testes passando.
- Guardrail de commit (`regra-sem-teste`) testado e funcionando.
- Documentação das Etapas 1-6 desta atividade, mais ADR e diagrama de
  arquitetura (Etapa 5).
- Branch **não** inclui nenhuma alteração que afete a regra de negócio já
  existente (`JANELA_REABERTURA_HORAS`, `SLA_TABLE_HORAS`) — só código novo,
  aditivo.

## Decisão tomada
**Aprovar**, com uma edição: manter o merge para `main` como uma decisão do
Fabrício, feita depois de revisar os arquivos localmente (ele quem tem
acesso de push ao repositório) — ou seja, o papel humano assumido aqui foi
o de **revisor técnico que prepara e recomenda a integração**, mas a
execução do merge em si fica para o dono do repositório revisar antes de
confirmar. Justificativa: mesmo com testes e guardrail passando, decisões
de merge para `main` de um repositório acadêmico avaliado devem ter
confirmação humana final, não só validação automatizada.
