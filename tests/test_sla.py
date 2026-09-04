from datetime import datetime

from rules.sla import classificar_sla


def _chamado(tipo, timestamp_abertura, timestamp_resolucao=None):
    return {
        "chamado_id": "X",
        "cliente_id": "C",
        "tema": "TECNICO",
        "tipo": tipo,
        "canal": "chat",
        "timestamp_abertura": timestamp_abertura,
        "status": "aberto" if timestamp_resolucao is None else "resolvido",
        "timestamp_resolucao": timestamp_resolucao,
    }


def test_ca1_dentro_do_prazo():
    chamado = _chamado("suporte_tecnico", datetime(2026, 9, 1, 8, 0))
    momento = datetime(2026, 9, 1, 9, 0)  # 1h de 4h de SLA
    assert classificar_sla(chamado, momento) == "dentro_do_prazo"


def test_ca2_em_risco():
    chamado = _chamado("suporte_tecnico", datetime(2026, 9, 1, 8, 0))
    momento = datetime(2026, 9, 1, 11, 30)  # 3h30 de 4h de SLA (87.5%)
    assert classificar_sla(chamado, momento) == "em_risco"


def test_ca3_estourado():
    chamado = _chamado("suporte_tecnico", datetime(2026, 9, 1, 8, 0))
    momento = datetime(2026, 9, 1, 13, 0)  # 5h de 4h de SLA
    assert classificar_sla(chamado, momento) == "estourado"


def test_ca4_tipo_sem_sla_usa_fallback():
    chamado = _chamado("tipo_inexistente", datetime(2026, 9, 1, 8, 0))
    momento = datetime(2026, 9, 1, 9, 0)  # 1h de 6h de SLA padrão
    # não deve lançar exceção e deve classificar normalmente
    assert classificar_sla(chamado, momento) == "dentro_do_prazo"
