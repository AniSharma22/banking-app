from src.app.cli.base_ui import BaseUI
from src.app.models.account import Account
from src.app.models.user import User
from src.app.services.account_service import AccountService


class UserDashboard(BaseUI):

    def __init__(self, user_service, bank_service, branch_service, current_user: User, account_service: AccountService,
                 main_menu):
        super().__init__(user_service, bank_service, branch_service, account_service)
        self.menu_options = {
            "1": ("Create New Account", self._create_new_account),
            "2": ("View Accounts", self._view_accounts),
            "3": ("Initiate Transactions", self._initiate_transaction),
            "4": ("View Previous Transactions", self._view_prev_transactions),
            "5": ("Update Profile", self._update_profile),
            "6": ("Logout", self._logout)

        }
        self.current_user = current_user
        self.main_menu = main_menu

    def show_user_dashboard(self):
        """ Display and handle user dashboard"""
        while True:
            try:
                self._display_user_menu()
                choice = input("Enter your choice (1-3): ")
                self._handle_choice(choice)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def _display_user_menu(self):
        """Display the menu options."""
        print("\n=== User Dashboard ===")
        print(f"Welcome, {self.current_user.name}!")
        for key, (option_name, _) in self.menu_options.items():
            print(f"{key}. {option_name}")

    def _handle_choice(self, choice):
        """Handle the user's menu choice."""
        if choice in self.menu_options:
            _, function = self.menu_options[choice]
            function()

    def _create_new_account(self):
        """Create a new bank account"""
        try:
            available_banks = self.bank_service.get_available_banks_for_user(self.current_user.id)
            if len(available_banks) == 0:
                print("No banks available at the moment.")
                return

            print("\nAvailable banks:")
            for i, bank in enumerate(available_banks, 1):  # Start counting from 1
                print(f"{i}. {bank.name}")

            while True:
                try:
                    choice = int(input("\nEnter Bank No to open a new account: "))
                    if choice < 1 or choice > len(available_banks):
                        print("Invalid choice. Please select a number from the list.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")

            selected_bank = available_banks[choice - 1]  # Adjust for 0-based indexing
            branches = self.branch_service.get_bank_branches(selected_bank.id)

            if not branches:
                print(f"No branches available for {selected_bank.name}.")
                return

            print("\nAvailable branches:")
            for i, branch in enumerate(branches, 1):  # Start counting from 1
                print(f"{i}. {branch.name}")

            while True:
                try:
                    choice = int(input("\nEnter Branch No to open a new account: "))
                    if choice < 1 or choice > len(branches):
                        print("Invalid choice. Please select a number from the list.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")

            selected_branch = branches[choice - 1]  # Adjust for 0-based indexing
            new_account = Account(
                user_id=self.current_user.id,
                branch_id=selected_branch.id,
                bank_id=selected_bank.id
            )

            self.account_service.create_new_account(new_account)
            print("\nAccount creation successful!")
        except Exception as e:
            print(f"\nError creating account: {str(e)}")
        finally:
            self.show_user_dashboard()

    def _view_accounts(self):
        pass

    def _initiate_transaction(self):
        pass

    def _view_prev_transactions(self):
        pass

    def _update_profile(self):
        pass

    def _logout(self):
        self.main_menu.show_main_menu()
