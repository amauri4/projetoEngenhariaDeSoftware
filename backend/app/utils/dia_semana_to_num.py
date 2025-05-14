from app.models.DiaHabitoSemana import DiaSemanaEnum

def converter_numero_para_dia_semana(numero_dia: int):
    
    mapeamento = {
        0: DiaSemanaEnum.domingo,
        1: DiaSemanaEnum.segunda,
        2: DiaSemanaEnum.terca,
        3: DiaSemanaEnum.quarta,
        4: DiaSemanaEnum.quinta,
        5: DiaSemanaEnum.sexta,
        6: DiaSemanaEnum.sabado
    }
    
    if numero_dia not in mapeamento:
        raise ValueError(f"Número de dia inválido: {numero_dia}. Use valores de 0 (domingo) a 6 (sábado)")
    
    return mapeamento[numero_dia]