from flask import Blueprint, abort, request, Response
from  campaigns.services import Helloworld
hello_world_bp = Blueprint('hello_world', __name__)

@hello_world_bp.route('/<name>', methods=['GET'])
def hello_world_route(name:str):
    hello = Helloworld(name=name)
    return Response(hello.greet(), status=200)