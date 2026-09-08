# Etapa 5 — Diagrama de arquitetura (versão 2)

Gerada com um prompt com **mais contexto**: pedindo explicitamente para
incluir o CSV de entrada e o banco SQLite como elementos externos ao
sistema (nível C4 de contêiner correto), mostrar os 4 módulos de `rules/`
separadamente (já que são independentes entre si, conforme Etapa 4), e
indicar a direção real do fluxo de dados.

```mermaid
C4Container
    title Pipeline de Atendimento de Call Center (v2)

    System_Ext(csv, "chamados_ficticios.csv", "Arquivo de entrada")
    System_Ext(db, "chamados.db", "SQLite")

    Container(main, "main.py", "Python", "Orquestrador: chama ingest -> rules -> storage, na ordem")
    Container(ingest, "ingest", "Python", "reader.py (le CSV), validacao.py (valida canal)")

    Container_Boundary(rules, "rules") {
        Container(dedup, "dedup.py", "Python", "Classifica reabertura (tecnico x adm)")
        Container(sla, "sla.py", "Python", "Classifica SLA por tipo de chamado")
        Container(urgencia, "urgencia.py", "Python", "Classifica urgencia (TDD)")
        Container(resumo, "resumo.py", "Python", "Resumo por canal")
    }

    Container(storage, "storage.db", "Python", "Persiste (upsert) o resultado das regras")

    Rel(csv, ingest, "le")
    Rel(main, ingest, "chama")
    Rel(main, dedup, "chama")
    Rel(main, sla, "chama")
    Rel(main, storage, "chama")
    Rel(ingest, dedup, "fornece Chamado")
    Rel(ingest, sla, "fornece Chamado")
    Rel(dedup, storage, "fornece classificacao")
    Rel(sla, storage, "fornece status SLA")
    Rel(storage, db, "grava (upsert)")
```

## Comparação escrita entre as duas versões
A **v1** comunica rápido a ideia geral (3 blocos, 1 orquestrador), mas
esconde justamente o ponto mais importante da decisão arquitetural da
Etapa 4: que as regras dentro de `rules/` são independentes entre si. Ela
também trata o CSV e o banco como implícitos, quando o nível C4 de
contêiner deveria deixá-los explícitos como elementos externos ao sistema.

A **v2** comunica melhor a arquitetura real: mostra o baixo acoplamento
entre os módulos de regra (suportando o ADR 0001 — não há motivo para
extrair serviço, pois os módulos já são independentes e pequenos), deixa
explícito o contrato de entrada/saída (CSV → `Chamado` → SQLite), e reflete
com mais fidelidade o próprio código (`git log`/imports reais checados na
Etapa 4). Fica mais verboso, mas para documentação de arquitetura — que
deve durar além da memória de quem escreveu o código — a v2 é a versão
que eu manteria.

**Versão escolhida para o projeto: v2.**
