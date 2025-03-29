from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from backend.src.campaigns.routes import hello_world_bp
from core.database import init_db

app = Flask(__name__)
init_db(app)
app.register_blueprint(hello_world_bp, url_prefix="/hello") #prefixe

@app.after_request
def add_header(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH')
    response.headers.add('Access-Control-Allow-Origin', '*') #On aime pas le CORS(e), on peut la configurer avec du .env ou autre
    return response

@app.errorhandler(RuntimeError)
def handle_runtime_error(error: RuntimeError):
    return {
        "message": str(error)
    }, 400


if __name__ == '__main__':
    app.run()