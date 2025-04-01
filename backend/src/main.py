from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from src.campaigns.routes import campaigns_bp
from src.users.routes import auth_bp
from src.swagger_definitions import swagger_template

def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "votre_super_secret_key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    jwt = JWTManager(app)

    Swagger(app, template=swagger_template)

    app.register_blueprint(campaigns_bp, url_prefix="/campaigns")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.after_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.errorhandler(RuntimeError)
    def handle_runtime_error(error: RuntimeError):
        return {"message": str(error)}, 400

    return app

app = create_app()

if __name__ == '__main__':
    app.run()