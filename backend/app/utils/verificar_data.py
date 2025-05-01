from datetime import datetime

def validar_formato_data(data_str: str):
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
        return data
    except ValueError:
        raise ValueError("Formato de data inválido. Use o formato 'YYYY-MM-DD'.")
