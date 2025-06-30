from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from app.repositories.RegistroRepository import RegistroDiarioRepository
from app.repositories.HabitoBaseRepository import HabitoBaseRepository
from app.utils.verificar_data import validar_formato_data
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError
from app.repositories.CategoriaRepository import CategoriaRepository

class CorrelacaoHabitoService:
    def __init__(self, db: Session):
        self.registro_repository = RegistroDiarioRepository(db)
        self.categoria_repository = CategoriaRepository(db)
        self.habito_base_repository = HabitoBaseRepository(db)
        self.db = db

    def _processar_correlacoes(self, registros: List[Dict], habitos_base_names: List[str]) -> str:
        try:
            dados_operacoes = [{
                'id': op.id,
                'data': op.data,
                'concluido': op.concluido,
                'habito_id': op.item_id
            } for op in registros]

            df_operacoes = pd.DataFrame(dados_operacoes)
            df_operacoes['data'] = pd.to_datetime(df_operacoes['data'])
            
            datas = df_operacoes["data"].unique()
            colunas = ["data"] + habitos_base_names
            dados = {k: [] for k in colunas}
            
            for data in datas:
                dados["data"].append(data)
                concluidos_no_dia = df_operacoes[
                    (df_operacoes["data"] == data) & 
                    (df_operacoes["concluido"] == True)
                ]
                habitos_concluidos_ids = concluidos_no_dia["habito_id"].to_list()
                
                for habito in habitos_base_names:
                    dados[habito].append(habitos_base_names.index(habito) in habitos_concluidos_ids)
            
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

    def buscar_correlacoes_habitos(self, usuario_id: int) -> str:
        try:
            registros = self.registro_repository.buscar_por_usuario(usuario_id)
            habitos_base = self.habito_base_repository.buscar_todos()
            
            if not registros:
                raise ServiceError("Nenhum registro encontrado para o usuário")
            if not habitos_base:
                raise ServiceError("Nenhum hábito base encontrado")
            
            habitos_base_names = [habito.nome for habito in habitos_base]
            return self._processar_correlacoes(registros, habitos_base_names)
            
        except ServiceError as e:
            raise e
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ServiceError(f"Erro no banco de dados ao buscar correlações: {str(e)}")
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao buscar correlações: {str(e)}")
        
    def buscar_categorias_usuario(self, usuario_id:int):
        try:
            categorias_usuario = self.categoria_repository.buscar_categorias_por_usuario(usuario_id=usuario_id)
            if not categorias_usuario:
                raise ConflictError("Categorias de hábito não encontradas.")
            return categorias_usuario
        except ConflictError as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao buscar categorias de usuário: {str(e)}")