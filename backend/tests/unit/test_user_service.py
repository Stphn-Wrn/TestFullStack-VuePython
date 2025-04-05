import pytest
from unittest.mock import (
    Mock, 
    patch, 
    MagicMock
)
from datetime import timedelta
from src.users.services import UserService
from src.core.database import db_session

class TestUserServiceUnit:
    
    @patch.object(UserService, 'create_user')
    def test_create_user_success(self, mock_create):
        mock_create.return_value = 1
        
        user_id = UserService.create_user("testuser", "test@example.com", "password123")
        
        assert user_id == 1
        mock_create.assert_called_once_with("testuser", "test@example.com", "password123")

    @patch("src.users.services.db_session")
    def test_create_user_email_exists(self, mock_db_session):
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session
        mock_session.query.return_value.filter_by.return_value.first.return_value = True 

        with pytest.raises(ValueError, match="Email already exists"):
            UserService.create_user("testuser", "existing@example.com", "password123")

    @patch("src.users.services.create_access_token")
    def test_generate_auth_token(self, mock_create_token):
        mock_create_token.return_value = "fake.jwt.token"
        user_id = 42
        expires_in = 3600

        token = UserService.generate_auth_token(user_id, expires_in)

        mock_create_token.assert_called_once_with(
            identity="42",
            expires_delta=timedelta(seconds=expires_in),
            additional_headers={"alg": "HS256", "typ": "JWT"}
        )
        assert token == "fake.jwt.token"

    @patch("src.users.services.db_session")
    def test_authenticate_success(self, mock_db_session):
        
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user

        user = UserService.authenticate("valid@example.com", "goodpassword")

        assert user == mock_user

    @patch("src.users.services.db_session")
    def test_authenticate_wrong_password(self, mock_db_session):

        mock_user = MagicMock()
        mock_user.check_password.return_value = False  
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user


        with pytest.raises(ValueError, match="Incorrect password"):
            UserService.authenticate("valid@example.com", "wrongpassword")

    @patch("src.users.services.db_session")
    def test_authenticate_email_not_found(self, mock_db_session):
        
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session
        mock_session.query.return_value.filter_by.return_value.first.return_value = None  

        
        with pytest.raises(ValueError, match="Email not found"):
            UserService.authenticate("unknown@example.com", "anypassword")