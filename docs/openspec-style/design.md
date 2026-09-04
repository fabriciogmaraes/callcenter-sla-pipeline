# Design: Detecção de chamados duplicados/reabertos

## Abordagem
Função pura `classificar_reaberturas(chamados, janela_horas)` que recebe
todos os chamados já carregados, ordena por timestamp e, para cada um,
busca o chamado anterior mais recente do mesmo cliente dentro da janela.

## Alternativas consideradas
- **Consulta ao banco por chamado individual** (em vez de processar a lista
  em memória): mais próxima de um sistema real com alto volume, mas
  desnecessária para o volume de dados fictício desta atividade — decisão:
  manter em memória por simplicidade.
- **Janela fixa vs. configurável**: optou-se por deixar `janela_horas`
  como parâmetro (default 24h) para permitir ajuste futuro sem mudar código.

## Estrutura de dados
```
ChamadoClassificado = {
    chamado_id: str,
    tipo_registro: "chamado_novo" | "reabertura",
    chamado_pai_id: str | None
}
```
