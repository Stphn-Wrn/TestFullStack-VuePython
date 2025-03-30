from flask import Blueprint, abort, request, Response
from  campaigns.services import Helloworld
user_bp = Blueprint('user', __name__)

@user_bp.route('/<name>', methods=['GET'])
def user_route(name:str):
    user = Helloworld(name=name)
    return Response(hello.greet(), status=200)