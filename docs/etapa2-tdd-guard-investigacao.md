# Etapa 2 — Investigação de ferramenta de enforcement (TDD Guard)

**Ferramenta escolhida:** [TDD Guard](https://github.com/nizos/tdd-guard) (nizos/tdd-guard).

## O que ela faz
Roda como um hook `PreToolUse` do **Claude Code** (o CLI da Anthropic),
interceptando as operações `Write`, `Edit`, `MultiEdit` e `TodoWrite` antes
de elas serem aplicadas. A cada tentativa de alteração de arquivo, ela
analisa o estado atual (resultado do último teste rodado, lista de todos,
diff pretendido) e bloqueia a ação se detectar uma violação de TDD:
implementar funcionalidade sem um teste falhando antes, implementar mais do
que o teste atual exige, ou pular a etapa de refactor. Suporta
TypeScript/JavaScript (via reporter do Vitest) e Python (via reporter do
pytest), e pode usar tanto um Claude local quanto a API da Anthropic para
validar cada tentativa.

## Por que não foi instalada neste ambiente
TDD Guard se integra especificamente ao mecanismo de hooks do **Claude
Code** (comando `/hooks`, matcher em `Write|Edit|MultiEdit|TodoWrite`) e
depende de Node.js 18+ rodando localmente junto ao CLI. Esta atividade foi
executada num ambiente de chat com um container Linux (sem o Claude Code
CLI instalado nem o mecanismo de hooks dele disponível), então não havia
como registrar o hook `PreToolUse` que a ferramenta exige. Por isso, optei
por documentar o comportamento a partir da documentação oficial em vez de
instalar.

## Como ela se comportaria no meu cenário
Se estivesse ativa durante a Etapa 2 deste projeto:
- Ao tentar criar `rules/urgencia.py` **antes** de `tests/test_urgencia.py`
  existir e falhar, TDD Guard bloquearia a escrita do arquivo de
  implementação, exigindo primeiro um teste falhando (fase RED).
- Durante a fase GREEN, se eu tentasse implementar de uma vez mais do que
  os 3 testes cobriam (ex.: adicionar suporte a um quarto tema não testado),
  ela bloquearia por "over-implementation".
- Na tarefa "sem TDD" feita logo abaixo (`resumir_por_canal`), TDD Guard
  teria bloqueado a própria primeira escrita do arquivo de implementação,
  já que nenhum teste existia ainda — ou seja, essa comparação só foi
  possível justamente por a ferramenta não estar ativa.
- O guardrail que já configurei na Etapa 1 (`scripts/check_regra_sem_teste.py`)
  atua num momento diferente do pipeline (no `commit`, via `pre-commit`),
  enquanto TDD Guard atuaria antes, no momento da própria edição do
  arquivo — os dois são complementares, não substitutos.
