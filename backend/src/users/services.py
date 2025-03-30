from datetime import timedelta
from flask_jwt_extended import create_access_token
from users.models import User
from core.database import db_session

class UserService:
    @staticmethod
    def create_user(username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        db_session.add(user)
        db_session.commit()
        return user

    @staticmethod
    def generate_auth_token(user_id, expires_in=3600):
        return create_access_token(
            identity=user_id,
            expires_delta=timedelta(seconds=expires_in)
        )