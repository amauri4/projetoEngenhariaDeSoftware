def validar_frequencia(frequencia: str) -> bool:
    frequencias_validas = ['diario', 'semanal', 'mensal']
    return frequencia.lower() in frequencias_validas