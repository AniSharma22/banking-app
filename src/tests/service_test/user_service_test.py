import unittest
from unittest.mock import MagicMock, patch

from src.app.models.user import User
from src.app.repositories.user_repository import UserRepository
from src.app.services.user_service import UserService
from src.app.utils.errors.error import UserExistsError, InvalidCredentialsError
from src.app.utils.utils import Utils




class TestUserService(unittest.TestCase):

    def setUp(self):
        self.mock_user_repository = MagicMock(spec=UserRepository)
        self.user_service = UserService(self.mock_user_repository)

    def test_signup_user_success(self):
        # Mock repository behavior
        self.mock_user_repository.fetch_user_by_email.return_value = None
        self.mock_user_repository.save_user.return_value = None

        # Mock password hashing
        with patch('Utils.hash_password', return_value="hashed_password"):
            user = User(email="test@example.com", password="password123", name="test",phone_no="test123",address="Test")
            result = self.user_service.signup_user(user)

            # Assertions
            self.mock_user_repository.fetch_user_by_email.assert_called_once_with("test@example.com")
            self.mock_user_repository.save_user.assert_called_once_with(user)
            self.assertEqual(result.password, "hashed_password")

    def test_signup_user_already_exists(self):
        # Mock repository behavior
        self.mock_user_repository.fetch_user_by_email.return_value = User(email="test@example.com",
                                                                          password="hashed_password")

        user = User(email="test@example.com", password="password123")
        with self.assertRaises(UserExistsError):
            self.user_service.signup_user(user)

    def test_login_user_success(self):
        # Mock repository behavior
        user = User(email="test@example.com", password="hashed_password")
        self.mock_user_repository.fetch_user_by_email.return_value = user

        # Mock password checking
        with patch('utils.Utils.check_password', return_value=True):
            result = self.user_service.login_user("test@example.com", "password123")

            # Assertions
            self.mock_user_repository.fetch_user_by_email.assert_called_once_with("test@example.com")
            self.assertEqual(result, user)

    def test_login_user_invalid_credentials(self):
        # Mock repository behavior
        self.mock_user_repository.fetch_user_by_email.return_value = None

        with self.assertRaises(InvalidCredentialsError):
            self.user_service.login_user("test@example.com", "wrongpassword")

        # Mock repository returns a user but password check fails
        user = User(email="test@example.com", password="hashed_password")
        self.mock_user_repository.fetch_user_by_email.return_value = user

        with patch('utils.Utils.check_password', return_value=False):
            with self.assertRaises(InvalidCredentialsError):
                self.user_service.login_user("test@example.com", "wrongpassword")
