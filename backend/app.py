from app import create_app 
from app.controllers.UsuarioController import user_bp
from app.controllers.HabitoBaseController import habito_bp
from app.controllers.HabitoUsuarioController import habito_usuario_bp
from app.controllers.RegistroController import registro_diario_bp
from app.controllers.DiaHabitoMesController import dia_habito_mes_bp
from app.controllers.DiaHabitoSemanaController import dia_habito_semana_bp
from app.controllers.ChatBotController import chat_bp
from app.controllers.CorrelacaoHabitoController import operacoes_extra_bp
from app.controllers.Aplicacao2.UsuariosController import auth_bp
from app.controllers.Aplicacao2.TarefaController import tarefa_bp
from app.controllers.Aplicacao2.OcorrenciaTarefaController import ocorrencia_tarefa_bp

app = create_app()

if __name__ == '__main__':
    app.register_blueprint(user_bp)
    app.register_blueprint(habito_bp)
    app.register_blueprint(habito_usuario_bp)
    app.register_blueprint(registro_diario_bp)
    app.register_blueprint(dia_habito_mes_bp)
    app.register_blueprint(dia_habito_semana_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(operacoes_extra_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tarefa_bp)
    app.register_blueprint(ocorrencia_tarefa_bp)
    
    app.run(port=8000, debug=True)
