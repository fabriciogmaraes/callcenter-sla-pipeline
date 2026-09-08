# Etapa 4 — Resumo da arquitetura atual e decisão

## Módulos e dependências (a partir do código real)
- **`ingest/`** — `reader.py` (lê o CSV, define o tipo `Chamado`) e
  `validacao.py` (valida canal). Não depende de nenhum outro módulo do
  projeto — é a base da árvore de dependências.
- **`rules/`** — `dedup.py`, `sla.py`, `urgencia.py`, `resumo.py`. Todos
  dependem apenas de `ingest.reader.Chamado` (para o tipo de entrada).
  **Não dependem uns dos outros** — cada regra é independente e pode ser
  testada isoladamente (confirmado pelos testes unitários por arquivo).
- **`storage/db.py`** — depende de `ingest.reader.Chamado` e dos tipos de
  saída de `rules.dedup` e `rules.sla`. É o módulo com mais acoplamento de
  entrada, porque sua função é justamente persistir o resultado das regras.
- **`main.py`** — orquestrador único: importa `ingest`, `rules.dedup`,
  `rules.sla` e `storage.db`, e chama cada um na ordem
  ingestão → regras → persistência → relatório.
- **`scripts/check_regra_sem_teste.py`** — isolado, só usado pelo
  `pre-commit`, sem acoplamento com o código de produção.

## Pontos de acoplamento
- Acoplamento é **baixo entre regras** (dedup, sla, urgência, resumo não se
  conhecem) e **concentrado na borda** (`ingest.reader.Chamado` como
  contrato de dados comum, e `main.py` como único ponto que conhece todos
  os módulos). Esse é o padrão desejável para um pipeline em etapas.
- O único acoplamento "denso" é `storage/db.py`, que depende de 3 módulos —
  mas é esperado, pois sua responsabilidade é agregar o resultado de todos.

## Decisão arquitetural
**O projeto está no tamanho certo como está — não deveria virar mais
módulos nem virar um serviço separado.**

Justificativa (critérios vistos em aula, não só opinião):
- **Tamanho/time:** projeto pequeno, mantido por 1 pessoa. Extrair serviço
  adiciona API, deploy e contrato de rede sem nenhum consumidor externo
  hoje que justifique isso.
- **Padrão de execução:** é um pipeline batch (roda do início ao fim,
  processa um CSV, grava e sai) — não há necessidade de escalar partes
  independentemente nem de disponibilidade contínua, que são os motivos
  mais comuns para extrair um serviço.
- **Acoplamento já é baixo onde importa:** as regras de negócio (o código
  que mais muda) já são módulos independentes entre si, testáveis
  isoladamente — o principal benefício de "mais modularidade" já existe na
  estrutura atual de pastas.
- **Contrato claro:** `ingest.reader.Chamado` (TypedDict) já funciona como
  um contrato de dados explícito entre as camadas, sem precisar de um
  serviço/API para formalizar isso.

**Único ponto de atenção para o futuro:** se `rules/` passar a ser
consumido por outro projeto (ex.: um dashboard ou uma API), o passo
intermediário correto seria empacotar `rules/` como uma biblioteca Python
instalável — não pular direto para um microsserviço.
