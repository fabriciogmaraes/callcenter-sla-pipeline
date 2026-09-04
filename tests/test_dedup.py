from datetime import datetime

from rules.dedup import classificar_reaberturas


def _chamado(chamado_id, cliente_id, tema, timestamp_abertura):
    return {
        "chamado_id": chamado_id,
        "cliente_id": cliente_id,
        "tema": tema,
        "tipo": "suporte_tecnico" if tema == "TECNICO" else "fatura",
        "canal": "chat",
        "timestamp_abertura": timestamp_abertura,
        "status": "aberto",
        "timestamp_resolucao": None,
    }


def test_ca1_chamado_genuinamente_novo():
    chamados = [_chamado("1", "C001", "TECNICO", datetime(2026, 9, 1, 8, 0))]
    resultado = classificar_reaberturas(chamados)
    assert resultado[0]["tipo_registro"] == "chamado_novo"
    assert resultado[0]["chamado_pai_id"] is None


def test_ca2_reabertura_de_chamado_tecnico():
    chamados = [
        _chamado("1", "C001", "TECNICO", datetime(2026, 9, 1, 8, 0)),
        _chamado("2", "C001", "TECNICO", datetime(2026, 9, 1, 10, 0)),
    ]
    resultado = {c["chamado_id"]: c for c in classificar_reaberturas(chamados)}
    assert resultado["2"]["tipo_registro"] == "reabertura"
    assert resultado["2"]["chamado_pai_id"] == "1"


def test_ca3_repeticao_adm_nao_e_reabertura():
    """Caso de borda: repetição na mesma janela, mas tema ADM -> chamado novo."""
    chamados = [
        _chamado("1", "C003", "ADM", datetime(2026, 9, 1, 8, 0)),
        _chamado("2", "C003", "ADM", datetime(2026, 9, 1, 10, 0)),
    ]
    resultado = {c["chamado_id"]: c for c in classificar_reaberturas(chamados)}
    assert resultado["2"]["tipo_registro"] == "chamado_novo"
    assert resultado["2"]["chamado_pai_id"] is None


def test_exatamente_no_limite_da_janela_e_chamado_novo():
    """Achado na revisão de diff (docs/revisao-diff.md): limite deve ser
    exclusivo. Um chamado aberto EXATAMENTE 24h antes não conta como reabertura."""
    chamados = [
        _chamado("1", "C001", "TECNICO", datetime(2026, 9, 1, 8, 0)),
        _chamado("2", "C001", "TECNICO", datetime(2026, 9, 2, 8, 0)),  # exatamente 24h depois
    ]
    resultado = {c["chamado_id"]: c for c in classificar_reaberturas(chamados)}
    assert resultado["2"]["tipo_registro"] == "chamado_novo"
    assert resultado["2"]["chamado_pai_id"] is None


def test_fora_da_janela_e_chamado_novo():
    chamados = [
        _chamado("1", "C001", "TECNICO", datetime(2026, 9, 1, 8, 0)),
        _chamado("2", "C001", "TECNICO", datetime(2026, 9, 3, 8, 0)),  # 48h depois
    ]
    resultado = {c["chamado_id"]: c for c in classificar_reaberturas(chamados)}
    assert resultado["2"]["tipo_registro"] == "chamado_novo"
