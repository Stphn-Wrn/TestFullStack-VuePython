from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity
from src.users.models import User
from src.core.database import db_session
class UserService:
    @staticmethod
    def create_user(username, email, password):
        session = db_session()
        try:
            if session.query(User).filter_by(email=email).first():
                raise ValueError("Email already exists")
            if session.query(User).filter_by(username=username).first():
                raise ValueError("Username already exists")

            user = User(username=username, email=email)
            user.set_password(password)
            session.add(user)
            session.commit()
            return user.id 
        finally:
            session.close()

    @staticmethod
    def generate_auth_token(user_id, expires_in=3600):
        return create_access_token(
            identity=str(user_id), 
            expires_delta=timedelta(seconds=expires_in),
            additional_headers={"alg": "HS256", "typ": "JWT"}
        )
    
    @staticmethod
    def get_current_user():
        user_id = get_jwt_identity()
        try:
            user_id = int(user_id)  
            session = db_session()
            return session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()
        
    @staticmethod
    def authenticate(email: str, password: str):
        session = db_session()
        try:
            user = session.query(User).filter_by(email=email).first()
            
            if not user:
                raise ValueError("Email not found")
            if not user.check_password(password):
                raise ValueError("Incorrect password")
                
            return user
        finally:
            session.close()