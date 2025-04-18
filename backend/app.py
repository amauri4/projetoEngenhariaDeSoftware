from app import create_app 
from app.controllers.UsuarioController import user_bp

app = create_app()

if __name__ == '__main__':
    app.register_blueprint(user_bp)
    app.run(debug=True)  
