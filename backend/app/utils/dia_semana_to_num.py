from app.models.DiaHabitoSemana import DiaSemanaEnum

def converter_numero_para_dia_semana(numero_dia: int):
    
    mapeamento = {
        1: DiaSemanaEnum.segunda,
        2: DiaSemanaEnum.terca,
        3: DiaSemanaEnum.quarta,
        4: DiaSemanaEnum.quinta,
        5: DiaSemanaEnum.sexta,
        6: DiaSemanaEnum.sabado,
        7: DiaSemanaEnum.domingo
    }
    
    if numero_dia not in mapeamento:
        raise ValueError(f"Número de dia inválido: {numero_dia}. Use valores de 1 (segunda) a 7 (domingo)")
    
    return mapeamento[numero_dia]