from rules.urgencia import chamado_urgente


def test_chamado_tecnico_aberto_e_urgente():
    chamado = {"tema": "TECNICO", "status": "aberto"}
    assert chamado_urgente(chamado) is True


def test_chamado_tecnico_resolvido_nao_e_urgente():
    chamado = {"tema": "TECNICO", "status": "resolvido"}
    assert chamado_urgente(chamado) is False


def test_chamado_adm_aberto_nao_e_urgente():
    chamado = {"tema": "ADM", "status": "aberto"}
    assert chamado_urgente(chamado) is False
