from app.services.TemplateMethodOcorrencia.OcorrenciaService import ServicoDeGeracaoDeOcorrencias
from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from app.repositories.RegistroRepository import RegistroDiarioRepository
from app.models.InstanciaDeHabito import InstanciaDeHabito
from app.models.RegistroDeOcorrencia import RegistroDeOcorrencia
from app.models.enums.frequencia_enums import FrequenciaEnum
from typing import Dict, Any, List
from datetime import date, timedelta
from sqlalchemy.exc import NoResultFound
from app.utils.verificar_data import validar_formato_data
from app.exceptions.service_exceptions import ServiceError

class ServicoDeOcorrenciasDeHabito(ServicoDeGeracaoDeOcorrencias):
    def _get_repositorio_item(self) -> HabitoUsuarioRepository:
        return HabitoUsuarioRepository(self.db)
    
    def _get_repositorio_ocorrencia(self) -> RegistroDiarioRepository:
        return RegistroDiarioRepository(self.db)

    def _extrair_configuracao_agendamento(self, item: InstanciaDeHabito) -> Dict[str, Any]:
        return {
            "frequencia": item.frequencia,
            "dias_semana": {dia.dia_semana for dia in item.dias_semana},
            "dias_mes": {dia.dia for dia in item.dias_mes}
        }
    
    def _validar_formato_data(self, data:str) -> Any:
        return validar_formato_data(data)

    def _calcular_ocorrencias(self, item_id: int, config: Dict[str, Any], periodo_em_dias: int) -> List[RegistroDeOcorrencia]:
        novas_ocorrencias = []
        hoje = date.today()
        frequencia = config["frequencia"]

        for i in range(periodo_em_dias):
            data_futura = hoje + timedelta(days=i)
            deve_criar = False
            
            if frequencia == FrequenciaEnum.DIARIA:
                if not config["dias_semana"] or data_futura.strftime('%A').upper() in config["dias_semana"]:
                     deve_criar = True
            elif frequencia == FrequenciaEnum.SEMANAL:
                if data_futura.strftime('%A').upper() in config["dias_semana"]:
                    deve_criar = True
            elif frequencia == FrequenciaEnum.MENSAL:
                if data_futura.day in config["dias_mes"]:
                    deve_criar = True
            
            if deve_criar:
                ocorrencia = RegistroDeOcorrencia(
                    item_id=item_id,
                    data=data_futura,
                    concluido=config["concluido"]
                )
                novas_ocorrencias.append(ocorrencia)
        
        return novas_ocorrencias
    
    def criar_ocorrencia_unica(self, item_id: int, data_str: str, status: bool) -> List[RegistroDeOcorrencia]:
        try:
            habito_usuario = self.item_repo.buscar_por_id(item_id)
            if not habito_usuario:
                raise NoResultFound("Hábito não encontrado.")
            data = self._validar_formato_data(data_str)
            novo_registro = self.ocorrencia_repo.criar_registro(data, item_id, status)
            return novo_registro
        except (NoResultFound, ValueError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao criar registro diário: {str(e)}") from e