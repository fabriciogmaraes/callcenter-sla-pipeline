# Relatório final — Harness e Arquitetura na Prática

**Projeto:** `callcenter-sla-pipeline` (branch `harness-arquitetura`,
reaproveitando o código da atividade "De Spec a Código").

**1. Autonomia e guardrail (Etapa 1).** Guardrail configurado via
`pre-commit`: bloqueia commits que alterem regra de negócio crítica
(`rules/dedup.py`/`rules/sla.py`) sem alterar teste no mesmo commit —
testado de propósito e confirmado bloqueando. Comparação de autonomia
(mesma tarefa em modo "plan" vs. "auto-accept"): o modo plan levou pouco
mais de tempo, mas entregou código testado e revisado; o auto-accept foi
mais rápido mas sem nenhuma garantia até alguém rodar os testes depois.

**2. TDD e enforcement (Etapa 2).** Ciclo Red-Green-Refactor aplicado em
`rules/urgencia.py`. Ferramenta TDD Guard investigada via documentação
oficial (não instalável neste ambiente de chat, por depender do mecanismo
de hooks do Claude Code — documentado em detalhe como se comportaria).
Comparação com/sem TDD: a tarefa sem teste antes (`resumo.py`) saiu com 2
lacunas de cobertura reais que só apareceram na revisão posterior.

**3. Checkpoint humano (Etapa 3).** Definido: revisão humana obrigatória
antes do merge de `harness-arquitetura` para `main`. Papel assumido:
revisor técnico que prepara e recomenda a integração, mas deixa a decisão
final de push/merge para o dono do repositório.

**4 e 5. Arquitetura, ADR e diagrama (Etapas 4 e 5).** Decisão: manter o
projeto como monólito modular (sem extrair serviço), justificada por baixo
acoplamento já existente entre as regras e ausência de consumidores
externos. Registrada em ADR 0001 (formato MADR) e em 2 versões de diagrama
Mermaid C4 — a v2 (com mais contexto no prompt) comunicou melhor a
arquitetura real por explicitar o baixo acoplamento entre as regras.

**6. Dívida técnica (Etapa 6, opção A).** Análise estática com Ruff
encontrou 33 avisos; o mais relevante foi uso de `datetime` sem timezone
(`DTZ001`/`DTZ005`) numa regra que decide status de SLA — risco real de
cálculo incorreto se o pipeline rodar em timezone diferente do dos dados.
Mitigação proposta: padronizar timestamps em UTC e ativar a regra `DTZ` no
guardrail já existente.

**Dificuldade real enfrentada.** A maior dificuldade não foi técnica, mas
de gestão de tempo: esta atividade cai em cima de outros dois compromissos
da mesma semana (trabalho final de Dev Web com IA, com apresentação em
12/09, e último dia na empresa em 11/09). Isso reforçou na prática o
próprio tema da atividade — a diferença real entre revisar cada passo com
calma (modo plan) e precisar decidir rápido o que automatizar sem perder
segurança (guardrails e testes existindo justamente para cobrir esse
aperto de tempo).
