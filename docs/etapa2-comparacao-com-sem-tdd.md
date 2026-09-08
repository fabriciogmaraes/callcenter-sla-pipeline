# Etapa 2 — Comparação: tarefa com TDD vs. tarefa sem TDD

## Com TDD (`rules/urgencia.py`, ciclo Red-Green-Refactor)
- Nasceu com 3 testes cobrindo os 3 casos relevantes do domínio (técnico
  aberto, técnico resolvido, adm aberto) — os casos de borda foram pensados
  **antes** da implementação existir, porque escrevê-los era o único jeito
  de ver a fase RED.
- Passo de refactor explícito: extraí `TEMA_TECNICO`/`STATUS_ABERTO` como
  constantes nomeadas e adicionei type hints/docstring, com a rede de
  segurança dos testes confirmando que nada quebrou.
- O guardrail da Etapa 1 (`scripts/check_regra_sem_teste.py`) não se aplicou
  aqui porque `rules/urgencia.py` não está na lista de arquivos críticos —
  mas o hábito de "teste antes" já cobriu o mesmo objetivo do guardrail.

## Sem TDD (`rules/resumo.py`, implementado direto)
- Foi mais rápido para escrever (uma única função, um único commit), mas
  saiu **sem nenhum teste** e, ao revisar o código depois de pronto,
  encontrei pelo menos 2 lacunas que só apareceram por não ter escrito
  teste antes:
  1. Nenhum tratamento para `chamado` sem a chave `"canal"` — lançaria
     `KeyError` em produção, silenciosamente, se um registro vier
     incompleto do CSV.
  2. Não usa `ingest.validacao.canal_valido` (criado na Etapa 1) — um canal
     inválido (ex.: `"fax"`) entraria no resumo como se fosse um canal
     válido, sem nenhum alerta.
- Nenhuma dessas lacunas foi *decidida* conscientemente — elas só existem
  porque, sem escrever o teste primeiro, não fui forçado a pensar nos casos
  de borda antes de considerar a função "pronta".

## Conclusão
A diferença não foi na qualidade do "caminho feliz" (as duas funções
resolvem o caso principal corretamente), mas na **cobertura de casos de
borda**: escrever o teste primeiro obriga a enumerar os cenários antes de
codificar; implementar direto tende a parar assim que o caso óbvio funciona.
Para regra de negócio (que é exatamente o que o guardrail da Etapa 1
protege), TDD é o caminho mais seguro; para uma função utilitária de baixo
risco, o custo de pular TDD foi pequeno, mas ainda assim real.
