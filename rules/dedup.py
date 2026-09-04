"""
Regras de detecção de chamados duplicados/reabertos.

Cobre os critérios de aceite CA1-CA3 da Funcionalidade 2 em docs/spec.md.

Regra de negócio central (definida junto com o usuário, é o caso de borda
principal desta funcionalidade):
    - Se o chamado anterior do mesmo cliente, dentro da janela, for do tema
      TECNICO -> o novo chamado é REABERTURA (mesmo problema, já em tratamento).
    - Se o chamado anterior do mesmo cliente, dentro da janela, for do tema
      ADM -> o novo chamado é CHAMADO_NOVO, mesmo estando na mesma janela
      (pode ser uma demanda diferente: fatura, cadastro, etc.).
"""

from datetime import timedelta
from typing import List, Optional, TypedDict

from ingest.reader import Chamado

JANELA_REABERTURA_HORAS = 24


class ChamadoClassificado(TypedDict):
    chamado_id: str
    tipo_registro: str  # "chamado_novo" | "reabertura"
    chamado_pai_id: Optional[str]


def _chamado_anterior_na_janela(
    chamado: Chamado, chamados_ordenados: List[Chamado], janela_horas: float
) -> Optional[Chamado]:
    """Retorna o chamado anterior mais recente do mesmo cliente dentro da janela.

    Requisito 4: só compara chamados do MESMO cliente.
    """
    limite_inferior = chamado["timestamp_abertura"] - timedelta(hours=janela_horas)

    # Limite inferior EXCLUSIVO (corrigido na revisão de diff — ver docs/revisao-diff.md):
    # um chamado aberto exatamente `janela_horas` antes não conta mais como
    # "dentro da janela", evitando reabertura de um chamado já encerrado há
    # exatamente 24h.
    candidatos = [
        c
        for c in chamados_ordenados
        if c["cliente_id"] == chamado["cliente_id"]
        and c["chamado_id"] != chamado["chamado_id"]
        and limite_inferior < c["timestamp_abertura"] < chamado["timestamp_abertura"]
    ]
    if not candidatos:
        return None
    # o mais recente dentro da janela
    return max(candidatos, key=lambda c: c["timestamp_abertura"])


def classificar_reaberturas(
    chamados: List[Chamado], janela_horas: float = JANELA_REABERTURA_HORAS
) -> List[ChamadoClassificado]:
    """Classifica cada chamado como chamado_novo ou reabertura (CA1, CA2, CA3)."""
    chamados_ordenados = sorted(chamados, key=lambda c: c["timestamp_abertura"])
    resultado: List[ChamadoClassificado] = []

    for chamado in chamados_ordenados:
        anterior = _chamado_anterior_na_janela(chamado, chamados_ordenados, janela_horas)

        if anterior is None:
            # CA1: nenhum chamado anterior do cliente na janela -> chamado novo
            resultado.append(
                {
                    "chamado_id": chamado["chamado_id"],
                    "tipo_registro": "chamado_novo",
                    "chamado_pai_id": None,
                }
            )
        elif anterior["tema"] == "TECNICO":
            # CA2: chamado técnico anterior na janela -> reabertura
            resultado.append(
                {
                    "chamado_id": chamado["chamado_id"],
                    "tipo_registro": "reabertura",
                    "chamado_pai_id": anterior["chamado_id"],
                }
            )
        else:
            # CA3 (caso de borda): chamado anterior é ADM -> continua chamado novo
            resultado.append(
                {
                    "chamado_id": chamado["chamado_id"],
                    "tipo_registro": "chamado_novo",
                    "chamado_pai_id": None,
                }
            )

    return resultado
