# Especificação — Pipeline de Atendimento de Call Center

Abordagem escolhida: **Markdown manual** (sem OpenSpec/Traycer). Justificativa:
com o prazo apertado, markdown manual permite percorrer o fluxo completo do
SDD (user story → PRD → critérios de aceite → plano de tarefas) sem overhead
de instalar/configurar ferramenta nova, mantendo os mesmos artefatos que o
OpenSpec exigiria (proposta, especificação, plano), só que em arquivos simples.

---

## Funcionalidade 1 — Roteamento de chamados por SLA de prioridade

### User Story (prompt inicial, sem decisão técnica)
> Como gestor de call center, quero que cada chamado recebido seja classificado
> automaticamente quanto ao seu status de SLA, para que eu saiba quais chamados
> estão dentro do prazo, em risco de estourar ou já estourados, sem precisar
> calcular isso manualmente.

### PRD — Requisitos
1. Cada tipo de chamado possui um SLA-alvo (tempo máximo esperado até tratamento),
   definido em uma tabela de referência.
2. O sistema calcula o tempo decorrido entre a abertura do chamado e o momento
   da avaliação (ou o momento de resolução, se já resolvido).
3. O sistema classifica o chamado em três estados: `dentro_do_prazo`,
   `em_risco` (ex.: acima de 80% do SLA) e `estourado` (acima de 100% do SLA).
4. Chamados sem tipo cadastrado na tabela de SLA devem cair em um SLA padrão
   (fallback), nunca causar erro no pipeline.
5. A classificação deve ser recalculável (idempotente) — rodar o pipeline de
   novo sobre o mesmo chamado não deve gerar classificações divergentes para
   o mesmo instante de avaliação.

### Critérios de aceite (Given/When/Then)

**CA1 — Chamado dentro do prazo**
- Given um chamado do tipo "Técnico" com SLA-alvo de 4 horas
- When o chamado é avaliado 1 hora após a abertura
- Then ele é classificado como `dentro_do_prazo`

**CA2 — Chamado em risco**
- Given um chamado do tipo "Técnico" com SLA-alvo de 4 horas
- When o chamado é avaliado 3h30 após a abertura (87,5% do SLA)
- Then ele é classificado como `em_risco`

**CA3 — Chamado estourado**
- Given um chamado do tipo "Técnico" com SLA-alvo de 4 horas
- When o chamado é avaliado 5 horas após a abertura
- Then ele é classificado como `estourado`

**CA4 — Caso de borda: tipo sem SLA cadastrado**
- Given um chamado com um tipo que não existe na tabela de SLA
- When o pipeline tenta classificá-lo
- Then o sistema aplica o SLA padrão de fallback e registra a classificação
  normalmente, sem interromper o processamento dos demais chamados

---

## Funcionalidade 2 — Detecção de chamados duplicados/reabertos

### User Story (prompt inicial, sem decisão técnica)
> Como gestor de call center, quero que o sistema identifique quando um chamado
> é uma reabertura de um chamado técnico anterior do mesmo cliente (e não um
> chamado genuinamente novo), para que as métricas de volume não fiquem infladas
> e o time saiba que aquele problema já está em tratamento.

### PRD — Requisitos
1. O sistema compara cada novo chamado com chamados anteriores do mesmo cliente
   dentro de uma janela de tempo configurável (ex.: 24h).
2. Se o chamado anterior dentro da janela for do tema **TÉCNICO**, o novo
   chamado é marcado como `reabertura` e vinculado ao chamado original.
3. Se o chamado anterior dentro da janela for do tema **ADM**, o novo chamado
   é tratado como `chamado_novo`, mesmo estando dentro da mesma janela de tempo.
4. A regra de reabertura só compara chamados do mesmo cliente — chamados de
   clientes diferentes nunca são considerados duplicados entre si.
5. Um chamado marcado como `reabertura` mantém referência ao chamado original
   (id do chamado pai), para rastreabilidade.

### Critérios de aceite (Given/When/Then)

**CA1 — Chamado genuinamente novo**
- Given um cliente sem chamados anteriores nas últimas 24h
- When ele abre um novo chamado
- Then o chamado é classificado como `chamado_novo`

**CA2 — Reabertura de chamado técnico**
- Given um cliente com um chamado do tema TÉCNICO aberto há 2 horas, ainda em
  tratamento
- When o mesmo cliente abre outro chamado dentro da janela de 24h
- Then o novo chamado é classificado como `reabertura` e vinculado ao chamado
  técnico original

**CA3 — Caso de borda: repetição em tema ADM não é reabertura**
- Given um cliente com um chamado do tema ADM (ex.: fatura) aberto há 2 horas
- When o mesmo cliente abre outro chamado dentro da janela de 24h, também de
  tema ADM
- Then o novo chamado é classificado como `chamado_novo`, e NÃO como
  reabertura, pois o tema ADM pode representar uma demanda diferente mesmo
  dentro da mesma janela de tempo

---

## Plano de tarefas (TO-DO) — gerado por agente de IA

Plano inicial proposto (task list bruta, como pedida a um agente):

1. Criar estrutura do projeto (pastas `ingest/`, `rules/`, `storage/`, `docs/`)
2. Implementar leitura do CSV de chamados fictícios
3. Implementar tabela de SLA por tipo de chamado
4. Implementar cálculo de tempo decorrido e classificação de SLA
5. Implementar persistência dos chamados classificados em SQLite
6. Implementar detecção de chamado anterior do mesmo cliente na janela de tempo
7. Implementar regra de reabertura (técnico) vs. chamado novo (ADM)
8. Implementar vínculo entre chamado reaberto e chamado original
9. Escrever testes para os critérios de aceite (CA1–CA4 da func. 1, CA1–CA3 da func. 2)
10. Gerar relatório final consolidado (contagem por status de SLA e por reabertura)

### Revisão do plano (edições e justificativa)
- **Reordenei** a tarefa 3 (tabela de SLA) para antes da tarefa 2 (leitura do CSV):
  faz mais sentido ter a regra de referência pronta antes de processar dados,
  evita retrabalho na tarefa de classificação.
- **Adicionei** uma tarefa 0 explícita de "definir o schema do CSV fictício
  (colunas e tipos)", que o plano original assumiu como dado — sem isso as
  tarefas 2 e 6 ficariam ambíguas sobre quais campos usar.
- **Não removi** nenhuma tarefa: todas são necessárias para cobrir os critérios
  de aceite definidos acima; o plano gerado já veio enxuto o suficiente.
- **Mantive** a tarefa de testes (9) antes do relatório (10), pois valida as
  regras de negócio antes de gerar qualquer número consolidado — evita reportar
  métricas erradas por bug de classificação.
