def validar_frequencia(frequencia: str) -> bool:
    frequencias_validas = ['diaria', 'semanal', 'mensal']
    return frequencia.lower() in frequencias_validas