from flask import Flask
from flasgger import Swagger
from datetime import (
    timedelta,
    datetime,
    timezone
)
from datetime import timedelta, datetime, timezone
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    get_jwt,
    get_jwt_identity,
    jwt_required
)
from src.campaigns.routes import campaign_bp
from src.users.routes import auth_bp
from src.swagger_definitions import swagger_template

import os, logging

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'Campaign API',
    'uiversion': 3,
    'specs_route': '/docs/'
}
swagger = Swagger(app, template=swagger_template)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "votre_super_secret_ici")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"] 
app.config["JWT_COOKIE_SECURE"] = True  
app.config["JWT_COOKIE_CSRF_PROTECT"] = True  

jwt = JWTManager(app)

app.register_blueprint(campaign_bp, url_prefix="/api/campaigns")
app.register_blueprint(auth_bp, url_prefix="/auth")


@app.after_request
def after_request_handler(response):
    response = add_header(response)
    response = refresh_expiring_jwts(response)
    return response

def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = os.getenv("FRONTEND_URL", "http://localhost:3000") 
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRF-TOKEN'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

@app.after_request
def refresh_expiring_jwts(response):
    try:
        # Ne rafraîchir que si c'est une requête API réussie
        if not 200 <= response.status_code < 300:
            return response

        # Vérifier si le token est sur le point d'expirer
        jwt_data = get_jwt()
        exp_timestamp = jwt_data.get("exp")
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=5))  # 5 min avant expiration

        if exp_timestamp and exp_timestamp < target_timestamp:
            current_user_id = get_jwt_identity()
            new_access_token = create_access_token(identity=current_user_id)
            set_access_cookies(response, new_access_token)

        return response
    except Exception as e:
        logging.exception(f"Error refreshing JWT: {e}")
        return response

@app.errorhandler(RuntimeError)
def handle_runtime_error(error: RuntimeError):
    return {"message": str(error)}, 400

if __name__ == '__main__':
    app.run(debug=True)
