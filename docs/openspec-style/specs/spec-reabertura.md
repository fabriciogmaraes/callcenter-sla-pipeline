# Spec: Detecção de chamados duplicados/reabertos

## Requisito 1 — Janela de comparação
O sistema DEVE comparar um novo chamado apenas com chamados anteriores do
MESMO cliente, dentro de uma janela de 24 horas (limite exclusivo em ambas
as pontas).

#### Cenário: Chamado fora da janela
- **DADO** um chamado anterior do cliente há mais de 24h
- **QUANDO** um novo chamado é aberto
- **ENTÃO** ele é classificado como `chamado_novo`

## Requisito 2 — Reabertura condicionada ao tema
O sistema DEVE classificar o novo chamado como `reabertura` apenas quando o
chamado anterior dentro da janela for do tema TÉCNICO. Quando o tema for
ADM, o novo chamado DEVE ser tratado como `chamado_novo`, mesmo dentro da
janela.

#### Cenário: Reabertura técnica
- **DADO** um chamado técnico aberto há 2h, ainda sem resolução
- **QUANDO** o mesmo cliente abre outro chamado
- **ENTÃO** o novo chamado é `reabertura`, vinculado ao chamado original

#### Cenário: Repetição administrativa (caso de borda)
- **DADO** um chamado ADM aberto há 2h
- **QUANDO** o mesmo cliente abre outro chamado ADM dentro da janela
- **ENTÃO** o novo chamado é `chamado_novo`, não `reabertura`

## Requisito 3 — Rastreabilidade
Todo chamado marcado como `reabertura` DEVE manter o id do chamado original
(`chamado_pai_id`) para fins de auditoria e relatório.
