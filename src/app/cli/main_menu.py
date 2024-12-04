import sys
from typing import Dict

from src.app.cli.admin_dashboard import AdminDashboard
from src.app.cli.base_ui import BaseUI
from src.app.cli.user_dashboard import UserDashboard
from src.app.models.user import User
from src.app.repositories.account_repository import AccountRepository
from src.app.repositories.bank_repository import BankRepository
from src.app.repositories.branch_repository import BranchRepository
from src.app.repositories.user_repository import UserRepository
from src.app.services.account_service import AccountService
from src.app.services.bank_service import BankService
from src.app.services.branch_service import BranchService
from src.app.services.user_service import UserService
from src.app.utils.db.db import DB
from src.app.utils.errors.error import UserExistsError, InvalidCredentialsError
from src.app.utils.types import Role
from src.app.utils.validators.validators import Validators


class MainMenu(BaseUI):
    def __init__(self, user_service: UserService, bank_service: BankService, branch_service: BranchService,
                 account_service: AccountService):
        super().__init__(user_service, bank_service, branch_service, account_service)
        self.menu_options = {
            "1": ("Login", self.login),
            "2": ("Signup", self.signup),
            "3": ("Exit", self.exit_system)
        }

    def show_main_menu(self) -> None:
        """Display and handle the main menu."""
        while True:
            try:
                self._display_menu()
                choice = input("Enter your choice (1-3): ")
                self._handle_choice(choice)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def _display_menu(self) -> None:
        """Display the menu options."""
        print("\n=== Welcome to the Banking System ===")
        for key, (option_name, _) in self.menu_options.items():
            print(f"{key}. {option_name}")

    def _handle_choice(self, choice: str) -> None:
        """Handle the user's menu choice."""
        if choice in self.menu_options:
            _, function = self.menu_options[choice]
            function()
        else:
            print("Invalid choice! Please select 1, 2, or 3.")

    def login(self) -> None:
        """Handle user login."""
        print("\n=== Welcome to the Login Page ===")
        while True:
            email = input("Enter your email: ").strip().lower()
            if not Validators.is_email_valid(email):
                print("Invalid email!")
            else:
                break
        while True:
            password = input("Enter your password: ").strip()
            if len(password) == 0:
                print("Password cannot be empty!")
            else:
                break
        try:
            current_user = self.user_service.login_user(email, password)
            print(current_user)
            self._route_to_dashboard(current_user)
        except InvalidCredentialsError as e:
            print(str(e))

    def signup(self) -> None:
        """Handle user signup process."""
        print("\n=== Signup ===")
        try:
            user_data = self._collect_user_data()
            user = User.from_dict(user_data)
            current_user = self.user_service.signup_user(user)
            self._route_to_dashboard(current_user)
        except UserExistsError as e:
            print(f"Signup failed: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def _collect_user_data(self) -> Dict[str, str]:
        """Collect and validate user input data."""
        validation_rules = {
            "name": (lambda: input("Enter your name: "), Validators.is_name_valid, "Invalid name"),
            "email": (lambda: input("Enter your email: ").strip().lower(), Validators.is_email_valid, "Invalid email"),
            "password": (
                lambda: input("Enter your password: ").strip(), Validators.is_password_valid, "Invalid password"),
            "phone_no": (
                lambda: input("Enter your phone number: "), Validators.is_valid_phone_number, "Invalid phone number"),
            "address": (lambda: input("Enter your address: "), Validators.is_valid_address, "Invalid address")
        }

        user_data = {}
        for field, (input_func, validator, error_msg) in validation_rules.items():
            while True:
                value = input_func()
                if validator(value):
                    user_data[field] = value
                    break
                print(error_msg)

        return user_data

    def _route_to_dashboard(self, user: User) -> None:
        """Route user to appropriate dashboard based on role."""
        if user.role == Role.USER.value:
            UserDashboard(self.user_service, self.bank_service, self.branch_service, user,
                          self.account_service, self).show_user_dashboard()
        else:
            AdminDashboard(self.user_service, self.bank_service, self.branch_service, user,
                           self.account_service, self).show_admin_dashboard()

    def exit_system(self) -> None:
        """Exit the system."""
        print("Thank you for using the Banking System. Goodbye!")
        sys.exit(0)


def main():
    try:
        # Initialize services
        db = DB()
        user_repository = UserRepository(db)
        bank_repository = BankRepository(db)
        branch_repository = BranchRepository(db)
        account_repository = AccountRepository(db)  # Add this

        user_service = UserService(user_repository)
        bank_service = BankService(bank_repository)
        branch_service = BranchService(branch_repository)
        account_service = AccountService(account_repository)  # Add this

        # Start the application with account_service
        main_menu = MainMenu(user_service, bank_service, branch_service, account_service)
        main_menu.show_main_menu()
    except Exception as e:
        print(f"Failed to start the application: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
