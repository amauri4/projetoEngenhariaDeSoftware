import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

def criar_token(dados: dict, expira_em_min=60):
    dados_copia = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=expira_em_min)
    dados_copia["exp"] = expiracao
    token = jwt.encode(dados_copia, SECRET_KEY, algorithm="HS256")
    return token

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")

def login_requerido(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {"erro": "Token não fornecido"}, 401

        try:
            token = auth_header.split(" ")[1]
            payload = verificar_token(token)
            request.usuario = payload
        except Exception as e:
            return {"erro": str(e)}, 401

        return func(*args, **kwargs)
    return wrapper
