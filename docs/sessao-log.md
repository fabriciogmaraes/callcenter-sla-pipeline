# Log da sessão do agente — Atividade Harness e Arquitetura

Registro cronológico das ações realizadas com o agente de IA (Claude) nesta
branch, com base no repositório `callcenter-sla-pipeline` (criado na
atividade "De Spec a Código"). Não editado/limpo — reflete a ordem real de
execução.

1. Clonado o repositório e criada a branch `harness-arquitetura` a partir de
   `origin/feat/regras-sla-reabertura` (código completo do pipeline).
2. Suíte de testes existente rodada e confirmada passando (9 testes) antes
   de qualquer alteração.
3. **Etapa 1:** criado o guardrail `scripts/check_regra_sem_teste.py`
   (registrado via `pre-commit`), commitado, e testado de propósito
   alterando `JANELA_REABERTURA_HORAS` sem tocar em `tests/` — commit
   bloqueado como esperado; alteração revertida sem entrar no histórico.
4. **Etapa 1 (continuação):** mesma tarefa pequena (validação de canal)
   executada duas vezes em branches separadas — `demo-plan-mode` (teste
   antes da implementação, diff revisado, suíte completa rodada antes do
   commit) e `demo-auto-accept` (implementação e commit direto, sem teste).
   Comparação escrita registrada; versão do modo plan trazida para a branch
   principal via `git cherry-pick`; branches de demonstração removidas.
5. **Etapa 2:** ciclo TDD completo (red → green → refactor) aplicado à
   função `chamado_urgente` em `rules/urgencia.py`. Ferramenta TDD Guard
   investigada via documentação oficial (não instalável neste ambiente de
   chat, por depender do mecanismo de hooks do Claude Code). Tarefa
   separada (`resumir_por_canal`) implementada sem teste antes, para
   comparação — 2 lacunas de cobertura identificadas na revisão posterior.
6. **Etapa 3:** checkpoint humano definido (antes do merge para `main`) e
   simulado — decisão registrada em `docs/checkpoint-humano-etapa3.md`.
7. (Continua nas Etapas 4-6: revisão arquitetural, ADR + diagrama, e opção
   de dívida técnica — ver commits e docs subsequentes nesta mesma branch.)

Todos os comandos executados (git, pytest, pre-commit) e suas saídas reais
estão preservados no histórico de commits desta branch; nenhum passo foi
omitido ou reescrito.
