from flask import Flask
from flasgger import Swagger
from datetime import timedelta
from flask_jwt_extended import JWTManager  
from src.campaigns.routes import hello_world_bp
from src.users.routes import auth_bp
from src.swagger_definitions import swagger_template

import os

app = Flask(__name__)

# Configuration Swagger
app.config['SWAGGER'] = {
    'title': 'Campaign API',
    'uiversion': 3,
    'specs_route': '/docs/'
}
swagger = Swagger(app, template=swagger_template)

# Configuration JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# Enregistrement des Blueprints
app.register_blueprint(hello_world_bp, url_prefix="/hello")
app.register_blueprint(auth_bp, url_prefix="/auth")

# CORS Headers
@app.after_request
def add_header(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.errorhandler(RuntimeError)
def handle_runtime_error(error: RuntimeError):
    return {"message": str(error)}, 400

if __name__ == '__main__':
    app.run(debug=True)