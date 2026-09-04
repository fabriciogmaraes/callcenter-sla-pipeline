"""
Módulo de ingestão dos chamados fictícios de call center.

Schema esperado do CSV (definido na Tarefa 0 do plano revisado em docs/spec.md):
    chamado_id, cliente_id, tema, tipo, canal,
    timestamp_abertura, status, timestamp_resolucao
"""

import csv
from datetime import datetime
from typing import List, Optional, TypedDict


class Chamado(TypedDict):
    chamado_id: str
    cliente_id: str
    tema: str
    tipo: str
    canal: str
    timestamp_abertura: datetime
    status: str
    timestamp_resolucao: Optional[datetime]


def _parse_datetime(value: str) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value)


def read_chamados(csv_path: str) -> List[Chamado]:
    """Lê o CSV de chamados e retorna uma lista de dicts tipados.

    Não lança erro se um campo opcional (timestamp_resolucao) estiver vazio.
    """
    chamados: List[Chamado] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            chamados.append(
                {
                    "chamado_id": row["chamado_id"],
                    "cliente_id": row["cliente_id"],
                    "tema": row["tema"],
                    "tipo": row["tipo"],
                    "canal": row["canal"],
                    "timestamp_abertura": _parse_datetime(row["timestamp_abertura"]),
                    "status": row["status"],
                    "timestamp_resolucao": _parse_datetime(row["timestamp_resolucao"]),
                }
            )
    return chamados
