# Etapa 5 — Comparação de abordagens de especificação

## Ferramentas/abordagens comparadas
1. **Markdown manual livre** (`docs/spec.md`, Etapa 2) — user story, PRD,
   critérios de aceite Given/When/Then e plano de tarefas, tudo em um único
   documento corrido.
2. **Estrutura estilo OpenSpec** (`docs/openspec-style/`) — aplicada
   manualmente (sem o CLI instalado, por limitação de tempo/ambiente —
   registrado aqui com transparência), separando os artefatos em
   `proposal.md` (por quê/impacto), `specs/spec-reabertura.md`
   (requisitos formais DEVE/cenários), `design.md` (decisões técnicas e
   alternativas consideradas) e `tasks.md` (checklist de execução).

## O que foi feito
Reespecifiquei a Funcionalidade 2 (reabertura/duplicidade) usando a
estrutura de arquivos separados do OpenSpec, mantendo as mesmas regras de
negócio já validadas na Etapa 2. O código implementado na Etapa 3 já
atende integralmente aos requisitos formalizados nesta segunda spec — não
houve necessidade de alterar `rules/dedup.py`, o que por si só é um sinal
de que a primeira especificação (Markdown manual) já tinha capturado a
regra de negócio corretamente.

## Comparação — pontos positivos e negativos

| Aspecto | Markdown manual livre | Estrutura estilo OpenSpec |
|---|---|---|
| Velocidade para escrever | Mais rápido, tudo em um lugar | Mais lento, decidir o que vai em cada arquivo toma tempo |
| Separação de preocupações | Fraca — por quê, requisito e tarefa se misturam no mesmo bloco | Forte — proposal (por quê) separado de spec (o quê) separado de design (como) |
| Facilidade de revisão por terceiros | Precisa ler o documento inteiro | Dá pra revisar só o `proposal.md` para decidir se vale a pena, sem entrar em detalhe técnico |
| Rastreabilidade de decisões técnicas | Não tem espaço próprio para isso | O `design.md` registra alternativas consideradas e descartadas — útil para não repetir discussão depois |
| Risco de over-engineering para tarefa pequena | Baixo | Alto — para uma funcionalidade do tamanho desta, 4 arquivos é mais estrutura do que o necessário |

## O que se aprendeu
A estrutura do OpenSpec compensa mais em times/projetos onde várias pessoas
vão revisar a proposta antes de entrar em detalhe técnico (o `proposal.md`
serve exatamente para isso). Para uma funcionalidade pequena, feita por uma
pessoa só e sob prazo apertado, o Markdown manual livre foi mais eficiente
sem perder qualidade — a mesma regra de negócio (e o mesmo caso de borda
ADM x Técnico) foi capturada corretamente nas duas abordagens.
