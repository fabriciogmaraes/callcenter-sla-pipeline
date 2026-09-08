def resumir_por_canal(chamados):
    resumo = {}
    for c in chamados:
        canal = c["canal"]
        resumo[canal] = resumo.get(canal, 0) + 1
    return resumo
