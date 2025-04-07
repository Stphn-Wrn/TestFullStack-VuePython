from flask import Blueprint, request, jsonify
from users.services import UserService
from src.users.schemas import UserSchema
from src.users.models import User
from datetime import timedelta
from src.core.database import db_session


from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    set_access_cookies,
    set_refresh_cookies
)
import logging


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        schema = UserSchema()
        user_data = schema.load(data)
        
        user_id = UserService.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        
        tokens = UserService.generate_auth_tokens(user_id)
        
        response = jsonify({
            "message": "User created successfully",
            "user_id": user_id
        })
        
        set_access_cookies(response, tokens["access_token"])
        set_refresh_cookies(response, tokens["refresh_token"])
        
        return response, 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        user = UserService.authenticate(
            email=data['email'],
            password=data['password']
        )

        tokens = UserService.generate_auth_tokens(user.id)
        
        response = jsonify({
            "message": "Login successful",
            "user": UserSchema().dump(user)
        })
        
        set_access_cookies(response, tokens["access_token"])
        set_refresh_cookies(response, tokens["refresh_token"])
        
        return response
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    
    try:

        current_user_id = get_jwt_identity()
        print("[JWT] identity récupérée (auth route) :", get_jwt_identity())

        user_id = int(current_user_id) if isinstance(current_user_id, (str, int)) else None
        if user_id is None:
            return jsonify({"error": "Invalid user ID"}), 400

        session = db_session()
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(UserSchema().dump(user))

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Server error"}), 500
    finally:
        session.close()
        
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  
def refresh():
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        
        response = jsonify({
            "message": "Token refreshed successfully",
            "access_token": new_access_token
        })
        
        set_access_cookies(response, new_access_token)
        
        return response, 200
        
    except Exception as e:
        logging.exception("Token refresh failed")
        return jsonify({"error": "Token refresh failed"}), 401
    
@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
@jwt_required()
def logout():
    if request.method == 'OPTIONS':
        return '', 200
    response = jsonify({"message": "Logout successful"})
    response.set_cookie('access_token_cookie', '', expires=0)
    response.set_cookie('refresh_token_cookie', '', expires=0)
    return response