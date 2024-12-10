import pytest
from unittest.mock import Mock, patch, MagicMock
from werkzeug.routing import ValidationError

from src.app.controller.user_urls.user_routes import UserHandler
from src.app.models.user import User


class TestUserHandler:
    @pytest.fixture
    def mock_user_service(self):
        """Create a mock UserService for testing"""
        return MagicMock()

    @pytest.fixture
    def user_handler(self, mock_user_service):
        """Create a UserHandler instance with mock user service"""
        return UserHandler.create(mock_user_service)

    def test_login_successful(self, user_handler, mock_user_service):
        """Test successful login"""
        # Prepare mock data
        mock_user = Mock(
            id='user123',
            role='customer',
            email='test@example.com'
        )
        # Configure mock service to return a user
        mock_user_service.login_user.return_value = mock_user
        # Simulate request context
        with patch('flask.request') as mock_request:
            # Set up mock request JSON
            mock_request.get_json.return_value = {
                'email': 'test@example.com',
                'password': 'validpassword'
            }
            # Call login method
            response, status_code = user_handler.login()
            # Assertions
            assert status_code == 200
            assert 'token' in response.json
            assert response.json['role'] == 'customer'
            # Verify service method was called with correct arguments
            mock_user_service.login_user.assert_called_once_with(
                'test@example.com',
                'validpassword'
            )

    # def test_login_invalid_email(self, user_handler):
    #     """Test login with invalid email format"""
    #     with patch('flask.request') as mock_request:
    #         # Set up mock request with invalid email
    #         mock_request.get_json.return_value = {
    #             'email': 'invalid-email',
    #             'password': 'somepassword'
    #         }
    #         # Call login method
    #         response, status_code = user_handler.login()
    #         # Assertions
    #         assert status_code == 400
    #         assert 'Email is not valid' in response.json['message']
    #
    # def test_signup_successful(self, user_handler, mock_user_service):
    #     """Test successful user signup"""
    #     with patch('flask.request') as mock_request:
    #         # Set up mock request JSON with valid data
    #         mock_request.get_json.return_value = {
    #             'name': 'John Doe',
    #             'email': 'john@example.com',
    #             'password': 'StrongPass123!',
    #             'phone_no': '+1234567890',
    #             'address': '123 Test Street, Testville'
    #         }
    #         # Configure mock service to not raise exceptions
    #         mock_user_service.signup_user.return_value = None
    #         # Call signup method
    #         response, status_code = user_handler.signup()
    #         # Assertions
    #         assert status_code == 200
    #         assert 'token' in response.json
    #         # Verify user service was called with a User object
    #         assert mock_user_service.signup_user.called
    #         user_args = mock_user_service.signup_user.call_args[0][0]
    #         assert isinstance(user_args, User)
    #         assert user_args.name == 'John Doe'
    #         assert user_args.email == 'john@example.com'
    #
    # def test_signup_invalid_name(self, user_handler):
    #     """Test signup with invalid name"""
    #     with patch('flask.request') as mock_request:
    #         # Set up mock request with invalid name
    #         mock_request.get_json.return_value = {
    #             'name': '',  # Empty name
    #             'email': 'john@example.com',
    #             'password': 'StrongPass123!',
    #             'phone_no': '+1234567890',
    #             'address': '123 Test Street, Testville'
    #         }
    #         # Call signup method
    #         response, status_code = user_handler.signup()
    #         # Assertions
    #         assert status_code == 400
    #         assert 'Name is not valid' in response.json['message']
    #
    # def test_signup_invalid_password(self, user_handler):
    #     """Test signup with invalid password"""
    #     with patch('flask.request') as mock_request:
    #         # Set up mock request with weak password
    #         mock_request.get_json.return_value = {
    #             'name': 'John Doe',
    #             'email': 'john@example.com',
    #             'password': 'weak',  # Too short
    #             'phone_no': '+1234567890',
    #             'address': '123 Test Street, Testville'
    #         }
    #         # Call signup method
    #         response, status_code = user_handler.signup()
    #         # Assertions
    #         assert status_code == 400
    #         assert 'Password is not valid' in response.json['message']