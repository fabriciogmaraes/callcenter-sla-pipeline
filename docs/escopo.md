# Escopo — Pipeline de Atendimento de Call Center

## Projeto base
Pipeline que ingere um CSV fictício de chamados de call center (cliente, tema,
canal, timestamp, status) e carrega os registros em um banco local (SQLite),
servindo de base para regras de negócio de roteamento e deduplicação.

## Funcionalidades escolhidas

### 1. Roteamento de chamados por SLA de prioridade
Classifica cada chamado como dentro do SLA, em risco ou estourado, com base
no tempo decorrido desde a abertura e no SLA-alvo definido por tipo de chamado.

### 2. Detecção de chamados duplicados/reabertos
Identifica se um novo chamado do mesmo cliente, dentro de uma janela de tempo
curta, deve ser tratado como reabertura ou como chamado novo — dependendo do
tema do chamado (TÉCNICO vs. ADM).

## Justificativa (por que são boas candidatas para SDD)
Ambas as funcionalidades têm regras de negócio explícitas que não são óbvias
a partir do nome da feature (SLA por tipo de chamado; reabertura condicionada
ao tema, não só ao tempo). Cada uma tem múltiplos cenários de uso distintos
com comportamentos diferentes entre si (SLA: dentro do prazo / em risco /
estourado; reabertura: técnico repetido / ADM repetido / chamado genuinamente
novo), incluindo casos de borda que fogem da regra padrão. As duas mexem em
mais de um arquivo do pipeline (ingestão, motor de regras, persistência/saída),
o que exige uma spec clara antes de codar para evitar retrabalho.
