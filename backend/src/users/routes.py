from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, Unauthorized
from users.services import UserService
from users.schemas import UserSchema
from users.models import User
from datetime import timedelta
from src.core.database import db_session

from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import logging

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        schema = UserSchema()
        user_data = schema.load(data)
        
        user_id = UserService.create_user(  # Reçoit l'ID seulement
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        
        token = UserService.generate_auth_token(user_id)
        
        return jsonify({
            "message": "User created successfully",
            "token": token,
            "user_id": user_id
        }), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.exception("Registration error")
        return jsonify({"error": "Registration failed"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email and password required"}), 400

        user = UserService.authenticate(
            email=data['email'],
            password=data['password']
        )

        token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=1)
        )

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": UserSchema().dump(user)
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        logging.exception("Login error")
        return jsonify({"error": "Login failed"}), 500



@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        print(f"JWT Identity: {current_user_id}, Type: {type(current_user_id)}")

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