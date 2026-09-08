"""
Validação de valores de canal de atendimento.
"""

CANAIS_VALIDOS = {"telefone", "chat", "email", "whatsapp"}


def canal_valido(canal: str) -> bool:
    """Retorna True se o canal informado está entre os canais suportados."""
    return canal in CANAIS_VALIDOS
