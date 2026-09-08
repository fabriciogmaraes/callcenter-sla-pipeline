"""
Classificação de urgência de chamados para fins de priorização em relatório.
"""

TEMA_TECNICO = "TECNICO"
STATUS_ABERTO = "aberto"


def chamado_urgente(chamado: dict) -> bool:
    """Retorna True se o chamado for técnico e ainda estiver aberto."""
    return chamado["tema"] == TEMA_TECNICO and chamado["status"] == STATUS_ABERTO
