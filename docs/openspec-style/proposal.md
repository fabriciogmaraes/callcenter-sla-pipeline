# Proposal: Detecção de chamados duplicados/reabertos

## Por que
Sem essa funcionalidade, chamados repetidos do mesmo cliente inflam as
métricas de volume do call center e escondem o fato de que um problema
técnico ainda está em tratamento.

## O que muda
Adiciona uma etapa no pipeline que compara cada novo chamado com chamados
anteriores do mesmo cliente dentro de uma janela de 24h, classificando o
novo chamado como `reabertura` (vinculado ao chamado original) ou
`chamado_novo`, dependendo do tema do chamado anterior (TÉCNICO x ADM).

## Impacto
- Afeta: `rules/`, `storage/` (novo campo `tipo_registro` e `chamado_pai_id`)
- Não afeta: a classificação de SLA (funcionalidade independente)
- Risco: erro nesta regra distorce métricas reportadas à gestão — por isso
  tem checkpoint humano dedicado (ver `docs/checkpoint-humano.md`)
