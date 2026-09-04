"""
Pipeline de atendimento de call center.

Executa, em ordem, o plano de tarefas revisado em docs/spec.md:
ingestão -> classificação de SLA -> classificação de reabertura -> persistência
-> relatório.
"""

from collections import Counter
from datetime import datetime

from ingest.reader import read_chamados
from rules.dedup import classificar_reaberturas
from rules.sla import classificar_sla
from storage.db import init_db, salvar_chamados

CSV_PATH = "data/chamados_ficticios.csv"
DB_PATH = "data/chamados.db"


def rodar_pipeline(momento_avaliacao: datetime | None = None) -> None:
    momento_avaliacao = momento_avaliacao or datetime.now()

    chamados = read_chamados(CSV_PATH)

    status_sla_por_id = {
        c["chamado_id"]: classificar_sla(c, momento_avaliacao) for c in chamados
    }
    classificacao_reabertura = classificar_reaberturas(chamados)

    conn = init_db(DB_PATH)
    salvar_chamados(conn, chamados, status_sla_por_id, classificacao_reabertura)

    gerar_relatorio(chamados, status_sla_por_id, classificacao_reabertura)
    conn.close()


def gerar_relatorio(chamados, status_sla_por_id, classificacao_reabertura) -> None:
    contagem_sla = Counter(status_sla_por_id.values())
    contagem_reabertura = Counter(c["tipo_registro"] for c in classificacao_reabertura)

    print("=== Relatório do Pipeline de Atendimento ===")
    print(f"Total de chamados processados: {len(chamados)}")
    print("\n-- SLA --")
    for status, qtd in contagem_sla.items():
        print(f"  {status}: {qtd}")
    print("\n-- Reabertura --")
    for tipo, qtd in contagem_reabertura.items():
        print(f"  {tipo}: {qtd}")


if __name__ == "__main__":
    rodar_pipeline()
