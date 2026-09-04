# Revisão de diff — Etapa 3, Tarefa 12

## Diff revisado
`rules/dedup.py` — função `_chamado_anterior_na_janela`, comparação da janela
de tempo de reabertura.

## O que a implementação original fazia
```python
limite_inferior <= c["timestamp_abertura"] < chamado["timestamp_abertura"]
```
O limite inferior da janela de 24h era **inclusivo**.

## O que eu teria deixado passar sem revisar
Sem revisar com atenção, esse diff pareceria correto — os testes originais
(CA1, CA2, CA3) todos passavam, porque nenhum deles testava exatamente o
limite da janela. Rodando o pipeline sobre o CSV fictício, notei que o
chamado 1009 (cliente C001, tema TÉCNICO, aberto às 08:00 do dia 02/09) foi
classificado como **reabertura** do chamado 1001 — que tinha sido aberto
**exatamente 24h antes** (08:00 do dia 01/09) e já estava **resolvido** há
mais de um dia.

Isso expõe dois problemas que passariam batido sem revisão manual do
resultado (não só do código):
1. O limite inclusivo faz um chamado aberto na borda exata da janela contar
   como "dentro dela" — um efeito de +1 instante que não estava explícito na
   regra de negócio combinada ("dentro da janela de 24h").
2. A regra de reabertura não distinguia se o chamado original ainda estava
   em aberto ou já resolvido — o que é discutível do ponto de vista de
   negócio (um chamado técnico já resolvido há 24h ainda representa "o mesmo
   problema em tratamento"?).

## Decisão tomada
Corrigi o ponto (1), tornando o limite inferior **exclusivo** — é a correção
mínima, objetiva e alinhada à leitura mais natural de "dentro da janela de
24h" (janela aberta, não fechada). Adicionei um teste
(`test_exatamente_no_limite_da_janela_e_chamado_novo`) pra travar esse
comportamento e evitar regressão.

O ponto (2) — se reabertura deveria considerar o status do chamado original —
não foi corrigido agora porque muda a regra de negócio combinada
originalmente (que fala só de tema, não de status). Ficou registrado aqui
como decisão consciente de escopo, não como bug corrigido.
