#!/usr/bin/env python3
"""
Guardrail: bloqueia commits que alterem regras de negocio criticas
(rules/dedup.py ou rules/sla.py) sem que nenhum arquivo de teste
correspondente tenha sido alterado no MESMO commit.

Risco real do projeto: alguem (humano ou agente de IA) ajusta um
parametro sensivel como JANELA_REABERTURA_HORAS ou SLA_TABLE_HORAS
e a mudanca de comportamento de negocio segue para producao sem
nenhum teste validando o novo comportamento.

Diferente do exemplo de aula ("bloquear merge na main"): aqui o
guardrail e sobre a COMPOSICAO do commit (codigo de regra sem teste
junto), nao sobre o destino do merge.
"""
import subprocess
import sys

ARQUIVOS_CRITICOS = {"rules/dedup.py", "rules/sla.py"}
PASTA_TESTES = "tests/"


def arquivos_staged() -> list[str]:
    resultado = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True, check=True,
    )
    return [linha.strip() for linha in resultado.stdout.splitlines() if linha.strip()]


def main() -> int:
    staged = arquivos_staged()
    regra_alterada = ARQUIVOS_CRITICOS.intersection(staged)
    teste_alterado = any(f.startswith(PASTA_TESTES) for f in staged)

    if regra_alterada and not teste_alterado:
        print("BLOQUEADO: commit altera regra(s) de negocio critica(s) "
              f"({', '.join(sorted(regra_alterada))}) sem alterar nenhum "
              "arquivo em tests/.")
        print("Atualize (ou adicione) o teste correspondente e inclua-o "
              "no mesmo commit antes de tentar novamente.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
