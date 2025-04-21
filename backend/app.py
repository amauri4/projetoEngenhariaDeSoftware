from app import create_app 
from app.controllers.UsuarioController import user_bp
from app.controllers.HabitoBaseController import habito_bp

app = create_app()

if __name__ == '__main__':
    app.register_blueprint(user_bp)
    app.register_blueprint(habito_bp)
    app.run(port=8000, debug=True)
