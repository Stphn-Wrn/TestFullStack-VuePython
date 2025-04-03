from flask import Flask
from flasgger import Swagger
from datetime import (
    timedelta,
    datetime,
    timezone
)
from flask_jwt_extended import (
    JWTManager,
    set_access_cookies,
    create_access_token,
    get_jwt,
    get_jwt_identity
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
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
jwt = JWTManager(app)

app.register_blueprint(campaign_bp, url_prefix="/api/campaigns")
app.register_blueprint(auth_bp, url_prefix="/auth")


@app.after_request
def add_header(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def refresh_expiring_jwts(response):
    try:
        jwt_data = get_jwt()
        if not jwt_data:
            return response

        exp_timestamp = jwt_data.get("exp")
        if not exp_timestamp:
            return response

        now = datetime.now(timezone.utc)
        remaining_time = exp_timestamp - datetime.timestamp(now)

        if remaining_time < 1:  
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)

        return response
    except Exception as e:
        logging.exception(f"Error refreshing JWT: {e}")
        return response

@app.errorhandler(RuntimeError)
def handle_runtime_error(error: RuntimeError):
    return {"message": str(error)}, 400

if __name__ == '__main__':
    app.run(debug=True)
