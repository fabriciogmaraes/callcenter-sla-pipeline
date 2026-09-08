# Etapa 6 — Opção A: Dívida técnica (análise estática com Ruff)

Saída completa: `docs/etapa6-ruff-output.txt` (33 avisos). A maioria é
estilo (`typing.List` → `list`), mas um achado é real dívida técnica com
risco de negócio:

## Sinal real de dívida técnica encontrado
`DTZ005` em `main.py`:
```
momento_avaliacao = momento_avaliacao or datetime.now()
```
`datetime.now()` é chamado **sem timezone**. Isso é um risco de negócio, não
só estilo: `classificar_sla` (a regra que decide se um chamado está
"dentro do prazo", "em risco" ou "estourado") compara esse timestamp
"naive" contra `timestamp_abertura` lido do CSV (também sem timezone
explícito, `DTZ001` nos testes confirma o mesmo padrão). Se o pipeline
algum dia rodar em um servidor com timezone diferente do timezone em que os
dados foram gerados, o cálculo de SLA fica silenciosamente errado — sem
nenhum erro, sem nenhum teste que pegue isso hoje, porque os testes também
usam `datetime()` naive (mesmo padrão, mesmo ponto cego).

## Mitigação proposta
1. Padronizar todos os timestamps do pipeline como timezone-aware em UTC:
   `datetime.now(timezone.utc)` em `main.py`, e normalizar
   `timestamp_abertura`/`timestamp_resolucao` para UTC já na leitura do CSV
   (`ingest/reader.py`), documentando a convenção (ex.: "CSV sempre em
   horário de Brasília, convertido para UTC na ingestão").
2. Adicionar `ruff` com a regra `DTZ` ativa no guardrail de pre-commit já
   existente (`.pre-commit-config.yaml`), para que datas naive não voltem a
   entrar no projeto sem ser notadas.
3. Não apliquei o fix automático (`ruff --fix`) agora para não misturar essa
   mudança de comportamento com o restante da atividade — fica registrado
   aqui como próximo passo, a ser feito com teste cobrindo timezone
   diferente do UTC antes do merge.
