from flask import Flask, request, Response
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
    verify_jwt_in_request,
    jwt_required
)
from src.campaigns.routes import campaign_bp
from src.users.routes import auth_bp
from src.swagger_definitions import swagger_template
from flask_cors import CORS


import os, logging

app = Flask(__name__)
CORS(app,
  supports_credentials=True,
  origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173"
  ],
  methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-CSRF-TOKEN"],
  expose_headers=["Set-Cookie"]
)

app.config['SWAGGER'] = {
    'title': 'API Documentation',
    'uiversion': 3,
    'specs_route': '/docs/',
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

app.config.update({
    "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "stephen/test/secretKey"),
    "JWT_ACCESS_TOKEN_EXPIRES": timedelta(minutes=15),
    "JWT_REFRESH_TOKEN_EXPIRES": timedelta(days=30),
    "JWT_TOKEN_LOCATION": ["cookies"],
    "JWT_COOKIE_SECURE": False,
    "JWT_COOKIE_CSRF_PROTECT": True,
    "JWT_COOKIE_SAMESITE": "None"
})

jwt = JWTManager(app)
swagger = Swagger(app, template=swagger_template)
app.register_blueprint(campaign_bp, url_prefix="/api/campaigns")
app.register_blueprint(auth_bp, url_prefix="/api/auth")


@app.after_request
def after_request_handler(response):
    response = refresh_expiring_jwts(response)
    response = handle_response(response)
    return response

def handle_response(response):
    try:
        if not response.is_json or request.method == 'OPTIONS':
            return response
            
        try:
            verify_jwt_in_request(optional=True)  
            jwt_data = get_jwt()
            
            response = refresh_expiring_jwts(response, jwt_data)
            
        except Exception as jwt_error:
            app.logger.debug(f"JWT verification skipped: {str(jwt_error)}")
            
        return response
    except Exception as e:
        app.logger.error(f"Error in response handler: {str(e)}")
        return response
    
def refresh_expiring_jwts(response, jwt_data=None):
    try:
        if not jwt_data:
            return response

        exp_timestamp = jwt_data.get("exp")
        if not exp_timestamp:
            return response

        now = datetime.now(timezone.utc)
        refresh_threshold = datetime.timestamp(now + timedelta(minutes=5))

        if exp_timestamp < refresh_threshold:
            current_user = get_jwt_identity()
            new_token = create_access_token(identity=current_user)
            set_access_cookies(response, new_token)

        return response
    except Exception as e:
        app.logger.error(f"JWT refresh error: {str(e)}")
        return response

@app.errorhandler(RuntimeError)
def handle_runtime_error(error: RuntimeError):
    return {"message": str(error)}, 400

if __name__ == '__main__':
    app.run(debug=True)