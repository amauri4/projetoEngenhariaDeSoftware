from app import create_app
# aplicação 1
from app.controllers.Aplicacao1.ChatBotController import chat1_bp
from app.controllers.Aplicacao1.InsightHabitoController import insight1_bp
from app.controllers.Aplicacao1.DiaHabitoSemanaController import dia_habito_semana_bp
from app.controllers.Aplicacao1.DiaHabitoMesController import dia_habito_mes_bp
from app.controllers.Aplicacao1.HabitoBaseController import habito_bp
from app.controllers.Aplicacao1.HabitoUsuarioController import habito_usuario_bp
from app.controllers.Aplicacao1.RegistroController import registro_diario_bp
from app.controllers.Aplicacao1.UsuarioController import auth1_bp
# # aplicação 2
# from app.controllers.Aplicacao2.ChatBotController import chat2_bp
# from app.controllers.Aplicacao2.InsightTarefaController import insight2_bp
# from app.controllers.Aplicacao2.OcorrenciaTarefaController import ocorrencia_tarefa_bp
# from app.controllers.Aplicacao2.TarefaController import tarefa_bp
# from app.controllers.Aplicacao2.UsuariosController import auth2_bp
# # aplicação 3
# from app.controllers.Aplicacao3.ChatBotController import chat3_bp
# from app.controllers.Aplicacao3.InsightTreinoController import insight3_bp
# from app.controllers.Aplicacao3.TreinoController import treino_bp
# from app.controllers.Aplicacao3.UsuariosController import auth3_bp


app = create_app()

if __name__ == '__main__':
    # bp da aplicação 1
    app.register_blueprint(chat1_bp)
    app.register_blueprint(insight1_bp)
    app.register_blueprint(dia_habito_semana_bp)
    app.register_blueprint(dia_habito_mes_bp)
    app.register_blueprint(habito_bp)
    app.register_blueprint(habito_usuario_bp)
    app.register_blueprint(registro_diario_bp)
    app.register_blueprint(auth1_bp)
    # # bp da aplicação 2
    # app.register_blueprint(chat2_bp)
    # app.register_blueprint(insight2_bp)
    # app.register_blueprint(ocorrencia_tarefa_bp)
    # app.register_blueprint(tarefa_bp)
    # app.register_blueprint(auth2_bp)
    # # bp da aplicação 3
    # app.register_blueprint(chat3_bp)
    # app.register_blueprint(insight3_bp)
    # app.register_blueprint(treino_bp)
    # app.register_blueprint(auth3_bp)
    
    app.run(port=8000, debug=True)
