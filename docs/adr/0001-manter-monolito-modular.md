# 0001-manter-monolito-modular.md (formato MADR)

## Contexto
O pipeline de atendimento (`callcenter-sla-pipeline`) processa chamados de
call center em lote: ingestão de CSV, classificação de SLA, classificação
de reabertura, persistência em SQLite e geração de relatório. É mantido por
uma única pessoa, sem consumidores externos hoje. Na Etapa 4 desta
atividade, avaliamos se o projeto deveria ser dividido em mais módulos, ter
um serviço extraído, ou permanecer como está.

## Decisão
Manter o projeto como um **monólito modular** — módulos separados por pasta
(`ingest/`, `rules/`, `storage/`) com um único orquestrador (`main.py`),
sem extrair nenhum módulo como serviço/API independente.

## Consequências
**Ganhos:**
- Sem overhead operacional de deploy, rede ou versionamento de API entre
  serviços que hoje não têm motivo para existir.
- Módulos de regra (`rules/`) já são independentes entre si e testáveis
  isoladamente, então o principal benefício de modularidade já é obtido sem
  o custo de um serviço separado.
- Mudança simples de rodar e depurar (um único processo, `python main.py`).

**Perdas / trade-offs aceitos:**
- Se outro sistema (ex.: um dashboard web) precisar reaproveitar `rules/`
  no futuro, será necessário empacotar o módulo como biblioteca instalável
  (ou, em último caso, extrair um serviço) — decisão adiada
  conscientemente, não descartada.
- Sem extração de serviço, não há escalabilidade independente por módulo
  (ex.: escalar só a classificação de SLA) — aceitável hoje porque o volume
  processado é baixo e o padrão é batch, não tempo real.
