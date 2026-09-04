# Relatório Final — De Spec a Código

**Projeto:** Pipeline de atendimento de call center
**Repositório:** github.com/fabriciogmaraes/callcenter-sla-pipeline
**Pull Request:** github.com/fabriciogmaraes/callcenter-sla-pipeline/pull/1

## Funcionalidades escolhidas e por que eram bons casos para SDD
Escolhi duas funcionalidades de um pipeline de dados de call center:
(1) roteamento de chamados por SLA de prioridade e (2) detecção de chamados
duplicados/reabertos. Ambas tinham regra de negócio não trivial e casos de
borda reais: no SLA, tipos de chamado sem SLA cadastrado precisavam de um
fallback; na reabertura, a regra dependia do **tema** do chamado anterior
(TÉCNICO vira reabertura, ADM vira chamado novo mesmo dentro da mesma
janela de tempo) — uma decisão de negócio que só ficou clara ao escrever
os critérios de aceite, não ao pensar no nome da feature.

## Abordagens de especificação usadas
Usei Markdown manual livre na Etapa 2 (user story, PRD, critérios Given/When/
Then e plano de tarefas em um único documento) e, na Etapa 5, reespecifiquei
a funcionalidade de reabertura na estrutura de artefatos do OpenSpec
(proposal/specs/design/tasks), aplicada manualmente por limitação de tempo
para instalar o CLI. Na prática, a abordagem manual livre foi mais rápida e
suficiente para o escopo do projeto; a estrutura OpenSpec só se justificaria
com mais pessoas revisando a proposta antes do detalhe técnico. Nenhuma das
duas exigiu mudança no código já implementado — sinal de que a spec original
já tinha capturado a regra corretamente.

## Dificuldade real enfrentada
A dificuldade concreta apareceu na revisão de diff da Tarefa 12: o código
gerado para a janela de tempo da reabertura usava um limite inferior
inclusivo, o que fazia um chamado aberto **exatamente** 24h antes (já
resolvido) contar como "dentro da janela" e ser marcado como reabertura.
Os testes originais passavam normalmente, porque nenhum deles cobria
exatamente o limite da janela — só rodando o pipeline sobre os dados e
desconfiando do número de reaberturas no relatório (caiu de 3 para 2 depois
da correção) foi possível identificar o problema. Isso reforçou que revisar
diff não é só ler código linha a linha: é rodar o resultado e questionar se
o número final faz sentido de negócio, especialmente em regras que
alimentam métricas de gestão (por isso o checkpoint humano definido na
Etapa 4 é justamente antes de mesclar mudanças nessa regra).
