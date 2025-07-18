from datetime import datetime
from app.database import session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from app.repositories.Framework.RegistroDeOcorrenciaRepository import RegistroDeOcorrenciaRepository
from app.repositories.Aplicacao1.HabitoBaseRepository import HabitoBaseRepository
from app.utils.verificar_data import validar_formato_data
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError
from app.services.Framework.InsightTemplate import InsightTemplate

class InsightCorrelacaoDeHabitos(InsightTemplate):
    def __init__(self, db: session):
        self.registro_repository = RegistroDeOcorrenciaRepository(db)
        self.habito_base_repository = HabitoBaseRepository(db)
        self.db = db

    def _buscar_dados_usuairo_insight(self, usuario_id: int):
        registros = self.registro_repository.buscar_por_usuario(usuario_id)
        habitos_base = self.habito_base_repository.buscar_todos()
        habitos_base_names = [habito.nome for habito in habitos_base]
        if not registros:
            raise ServiceError("Nenhum registro encontrado para o usuário")
        if not habitos_base:
            raise ServiceError("Nenhum hábito base encontrado")
        return [registros,habitos_base_names]
    
    # pensei em dados ser uma lista de dicionarios
    def _processar_dados_insight(self, dados: List[Dict]):
        try:
            registros, nomes_habitos_base = dados
            dados_operacoes = [{
                'id': op.id,
                'data': op.data,
                'concluido': op.concluido,
                'habito_id': op.item_id
            } for op in registros]

            df_operacoes = pd.DataFrame(dados_operacoes)
            df_operacoes['data'] = pd.to_datetime(df_operacoes['data'])
            
            datas = df_operacoes["data"].unique()
            colunas = ["data"] + nomes_habitos_base
            dados = {k: [] for k in colunas}
            
            for data in datas:
                dados["data"].append(data)
                concluidos_no_dia = df_operacoes[
                    (df_operacoes["data"] == data) & 
                    (df_operacoes["concluido"] == True)
                ]
                habitos_concluidos_ids = concluidos_no_dia["habito_id"].to_list()
                
                for habito in nomes_habitos_base:
                    dados[habito].append(nomes_habitos_base.index(habito) in habitos_concluidos_ids)
            
            new_df = pd.DataFrame(dados)
            correlacao = new_df.iloc[:, 1:].corr()
            
            correlacao_long = correlacao.where(
                np.triu(np.ones(correlacao.shape), k=1).astype(bool)
            ).stack().reset_index()
            
            correlacao_long.columns = ['Variavel 1', 'Variavel 2', 'Correlacao']
            correlacao_ordenada = correlacao_long.reindex(
                correlacao_long['Correlacao'].abs().sort_values(ascending=False).index
            )
            corr_filtered = correlacao_ordenada[correlacao_ordenada["Correlacao"].abs() > 0.5]
            prompt = ""
            for i in range(corr_filtered.shape[0]):
                corr_list = corr_filtered.iloc[i,:].to_list()
                corr_sign = "Positiva" if corr_list[2] > 0 else "Negativa"
                corr_strong = "Fortemente" if abs(corr_list[2]) > 0.8 else ""
                prompt += f"{corr_list[0]} e {corr_list[1]}: Correlação {corr_strong} {corr_sign}\n"
            return prompt
        except Exception as e:
            raise ServiceError(f"Erro ao processar correlações: {str(e)}")
