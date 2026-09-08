# Etapa 1 — Comparação entre dois modos de autonomia

**Tarefa usada nos dois testes:** adicionar validação de canal de
atendimento (`ingest/validacao.py`, função `canal_valido`, aceitando apenas
`telefone`, `chat`, `email`, `whatsapp`).

## Modo 1 — "Plan mode" (branch `demo-plan-mode`)
Passos seguidos, cada um confirmado antes do próximo: escrever o teste
primeiro → rodar e confirmar falha (red) → implementar o mínimo → rodar e
confirmar sucesso (green) → revisar o diff (`git diff --stat`,
`git status`) → rodar a suíte inteira → só então commitar.

- **Tempo gasto:** ~13s de execução (6 comandos/interações distintas).
- **Sensação de controle:** alta. Cada etapa tinha um ponto de checagem
  explícito (rodar teste antes de escrever código, revisar diff antes de
  commitar), então qualquer erro teria sido pego antes do commit.
- **Risco percebido:** baixo. O código entrou testado, com type hints e
  docstring, e a suíte completa (12 testes) foi validada antes do commit —
  incluindo os testes já existentes, então dava pra saber que nada quebrou.

## Modo 2 — "Auto-accept" (branch `demo-auto-accept`)
Implementação e commit em um único passo, sem escrever teste antes, sem
rodar a suíte, sem revisar o diff.

- **Tempo gasto:** ~0s de execução (1 comando).
- **Sensação de controle:** baixa. Não houve nenhum ponto de checagem entre
  escrever o código e ele ir para o histórico do projeto.
- **Risco percebido:** alto, apesar do código final ser funcionalmente
  parecido — sem teste, sem type hints/docstring, e sem confirmação de que a
  suíte existente continuava passando. Qualquer regressão só apareceria
  depois, quando (e se) alguém rodasse os testes.

## Conclusão
Para uma mudança pequena e isolada como essa, a diferença de tempo real foi
mínima (segundos), mas o modo auto-accept trocou verificação por velocidade
sem necessidade — o ganho de tempo não compensou a perda de garantias. Para
mudanças em regra de negócio crítica (ver guardrail da Etapa 1), o modo plan
é o indicado; auto-accept faz mais sentido em tarefas de baixíssimo risco e
alta repetição (ex.: renomear variável, formatação).

A versão trazida para o projeto principal foi a do **modo plan**
(commit `ef10f31` na branch `demo-plan-mode`), por já vir com teste.
