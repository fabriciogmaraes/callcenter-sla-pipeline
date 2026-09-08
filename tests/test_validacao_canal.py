from ingest.validacao import CANAIS_VALIDOS, canal_valido


def test_canal_valido_aceita_canais_conhecidos():
    for canal in CANAIS_VALIDOS:
        assert canal_valido(canal) is True


def test_canal_valido_rejeita_canal_desconhecido():
    assert canal_valido("fax") is False


def test_canal_valido_rejeita_canal_vazio():
    assert canal_valido("") is False
