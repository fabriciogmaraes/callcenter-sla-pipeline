"""
Regras de SLA por tipo de chamado.

Cobre os critérios de aceite CA1-CA4 da Funcionalidade 1 em docs/spec.md.
"""

from datetime import datetime
from typing import Literal

from ingest.reader import Chamado

SlaStatus = Literal["dentro_do_prazo", "em_risco", "estourado"]

# Requisito 1: SLA-alvo (em horas) por tipo de chamado.
SLA_TABLE_HORAS = {
    "instabilidade_conexao": 4.0,
    "suporte_tecnico": 4.0,
    "fatura": 8.0,
    "cadastro": 8.0,
    "cancelamento": 8.0,
}

# Requisito 4: fallback para tipos não cadastrados na tabela.
SLA_PADRAO_HORAS = 6.0

LIMIAR_EM_RISCO = 0.8  # 80% do SLA


def obter_sla_horas(tipo: str) -> float:
    """Retorna o SLA-alvo em horas para um tipo de chamado (com fallback)."""
    return SLA_TABLE_HORAS.get(tipo, SLA_PADRAO_HORAS)


def classificar_sla(chamado: Chamado, momento_avaliacao: datetime) -> SlaStatus:
    """Classifica um chamado quanto ao SLA (CA1, CA2, CA3, CA4).

    Usa o timestamp de resolução como momento de avaliação se o chamado já
    estiver resolvido; caso contrário, usa `momento_avaliacao` (ex.: "agora").
    """
    sla_horas = obter_sla_horas(chamado["tipo"])

    momento_fim = chamado["timestamp_resolucao"] or momento_avaliacao
    horas_decorridas = (momento_fim - chamado["timestamp_abertura"]).total_seconds() / 3600

    if horas_decorridas > sla_horas:
        return "estourado"
    if horas_decorridas >= sla_horas * LIMIAR_EM_RISCO:
        return "em_risco"
    return "dentro_do_prazo"
