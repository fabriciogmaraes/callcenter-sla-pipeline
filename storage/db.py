"""
Persistência dos chamados processados em SQLite.
"""

import sqlite3
from typing import List

from ingest.reader import Chamado
from rules.dedup import ChamadoClassificado
from rules.sla import SlaStatus


def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chamados_processados (
            chamado_id TEXT PRIMARY KEY,
            cliente_id TEXT NOT NULL,
            tema TEXT NOT NULL,
            tipo TEXT NOT NULL,
            canal TEXT NOT NULL,
            status_sla TEXT NOT NULL,
            tipo_registro TEXT NOT NULL,
            chamado_pai_id TEXT
        )
        """
    )
    conn.commit()
    return conn


def salvar_chamados(
    conn: sqlite3.Connection,
    chamados: List[Chamado],
    status_sla_por_id: dict[str, SlaStatus],
    classificacao_reabertura: List[ChamadoClassificado],
) -> None:
    """Grava (upsert) os chamados já classificados por SLA e por reabertura.

    Usa INSERT OR REPLACE para que rodar o pipeline de novo sobre o mesmo
    chamado_id atualize o registro em vez de duplicá-lo (requisito 5 da
    Funcionalidade 1: idempotência).
    """
    reabertura_por_id = {c["chamado_id"]: c for c in classificacao_reabertura}

    for chamado in chamados:
        reabertura = reabertura_por_id[chamado["chamado_id"]]
        conn.execute(
            """
            INSERT OR REPLACE INTO chamados_processados
                (chamado_id, cliente_id, tema, tipo, canal,
                 status_sla, tipo_registro, chamado_pai_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                chamado["chamado_id"],
                chamado["cliente_id"],
                chamado["tema"],
                chamado["tipo"],
                chamado["canal"],
                status_sla_por_id[chamado["chamado_id"]],
                reabertura["tipo_registro"],
                reabertura["chamado_pai_id"],
            ),
        )
    conn.commit()
