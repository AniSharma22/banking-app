from src.app.models.user import User
from src.app.repositories.user_repository import UserRepository
from src.app.utils.errors.error import UserExistsError, InvalidCredentialsError
from src.app.utils.utils import Utils


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def signup_user(self, user: User) -> User:
        if self.user_repository.fetch_user_by_email(user.email) is not None:
            raise UserExistsError("User with this email already exists")

        # hash the password
        user.password = Utils.hash_password(user.password)

        # Save to database
        self.user_repository.save_user(user)
        return user

    def login_user(self, email: str, password: str) -> User:
        user = self.user_repository.fetch_user_by_email(email)
        if user is None or not Utils.check_password(password, user.password):
            raise InvalidCredentialsError("Email or password incorrect")
        return user
