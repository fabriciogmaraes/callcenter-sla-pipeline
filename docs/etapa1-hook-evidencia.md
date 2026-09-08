# Etapa 1 — Evidência do guardrail funcionando

## Guardrail configurado
`scripts/check_regra_sem_teste.py` (registrado via `.pre-commit-config.yaml`,
hook `regra-sem-teste`). Bloqueia qualquer commit que altere `rules/dedup.py`
ou `rules/sla.py` sem que nenhum arquivo dentro de `tests/` também esteja
incluído no mesmo commit.

**Risco que ele mitiga:** alteração silenciosa de regra de negócio crítica
(ex.: janela de reabertura, tabela de SLA) sem cobertura de teste — diferente
do exemplo de aula (bloquear merge na main), pois atua sobre a *composição*
do commit, não sobre o destino do merge.

## Teste do bloqueio (log real)

Comando: alterei `JANELA_REABERTURA_HORAS` de 24 para 48 em `rules/dedup.py`
e tentei commitar **sem** tocar em `tests/`.

```
$ git commit -m "teste proposital: altera janela de reabertura sem mexer em testes"
Bloqueia alteração de regra de negócio sem teste correspondente.......................Failed
- hook id: regra-sem-teste
- exit code: 1

BLOQUEADO: commit altera regra(s) de negocio critica(s) (rules/dedup.py) sem
alterar nenhum arquivo em tests/.
Atualize (ou adicione) o teste correspondente e inclua-o no mesmo commit
antes de tentar novamente.
```

Commit rejeitado, exatamente como esperado. A alteração foi revertida em
seguida (`git checkout -- rules/dedup.py`) — não ficou registrada no
histórico do projeto.
