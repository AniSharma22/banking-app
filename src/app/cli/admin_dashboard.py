from src.app.cli.base_ui import BaseUI
from src.app.models.bank import Bank
from src.app.models.branch import Branch
from src.app.models.user import User
from src.app.services.account_service import AccountService


class AdminDashboard(BaseUI):

    def __init__(self, user_service, bank_service, branch_service, current_user: User, account_service: AccountService,
                 main_menu):
        super().__init__(user_service, bank_service, branch_service, account_service)
        self.current_user = current_user
        self.main_menu = main_menu
        self.menu_options = {
            "1": ("Manage Banks", self._manage_banks),
            "2": ("Manage Branches", self._manage_branches),
            "3": ("Monitor Transactions", self._monitor_transactions),
            "4": ("Logout", self._logout)
        }

    def show_admin_dashboard(self):
        """Display and handle admin dashboard."""
        while True:
            try:
                self._display_admin_menu()
                choice = input("Enter your choice (1-4): ")
                self._handle_choice(choice)
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def _display_admin_menu(self):
        """Display the menu options."""
        print("\n=== Admin Dashboard ===")
        print(f"Welcome, {self.current_user.name}!")
        for key, (option_name, _) in self.menu_options.items():
            print(f"{key}. {option_name}")

    def _handle_choice(self, choice):
        """Handle the user's menu choice."""
        if choice in self.menu_options:
            _, function = self.menu_options[choice]
            function()
        else:
            print("Invalid choice. Please select a valid option.")

    def _manage_banks(self):
        """Display the banks menu and let the admin add, update, or remove a bank."""
        try:
            banks = self.bank_service.get_all_banks()
            if not banks:
                print("There are no banks.")
            else:
                print("\n=== Banks ===")
                for bank in banks:
                    print(f"ID: {bank.id}, Name: {bank.name}")

            print("\n1. Add a new bank")
            print("2. Update existing bank details")
            print("3. Remove a bank")
            choice = int(input("Enter your choice (1-3): "))

            if choice == 1:
                self._add_new_bank()
            elif choice == 2:
                self._update_bank_details()
            elif choice == 3:
                self._remove_bank()
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
        except Exception as e:
            print(f"An error occurred while managing banks: {str(e)}")

    def _add_new_bank(self):
        """Add a new bank and an associated branch."""
        bank_name = input("Enter bank name: ")
        branch_name = input("Enter branch name: ")
        branch_address = input("Enter branch address: ")

        new_bank = Bank(name=bank_name)
        print(type(new_bank.id))
        new_branch = Branch(name=branch_name, bank_id=new_bank.id, address=branch_address)

        self.bank_service.create_new_bank(new_bank)
        self.branch_service.create_new_branch(new_branch)

        print("Bank and its branch have been successfully created.")

    def _update_bank_details(self):
        """Update details of an existing bank."""
        banks = self.bank_service.get_all_banks()
        if not banks:
            print("There are no banks.")
            return

        print("\n=== Banks ===")
        for bank in banks:
            print(f"ID: {bank.id}, Name: {bank.name}")
        choice = int(input("Enter bank number you want to update: "))
        if choice >= len(banks) or choice < 0:
            print("Invalid choice.")
            return
        new_bank_name = input("Enter new name for the bank: ")
        self.bank_service.update_bank(banks[choice].id, new_bank_name)

        print("Bank details updated successfully.")

    def _remove_bank(self):
        """Remove an existing bank."""
        banks = self.bank_service.get_all_banks()
        if not banks:
            print("There are no banks.")
            return

        print("\n=== Banks ===")
        for bank in banks:
            print(f"ID: {bank.id}, Name: {bank.name}")
        choice = int(input("Enter bank number you want to delete: "))
        if choice >= len(banks) or choice < 0:
            print("Invalid choice.")
            return

        self.bank_service.delete_bank(banks[choice].id)
        print(f"Bank has been removed successfully.")

    def _manage_branches(self):
        """Placeholder for branch management functionality."""
        try:
            banks = self.bank_service.get_all_banks()
            if not banks:
                print("There are no banks.")
                return
            else:
                print("\n=== Banks ===")
                for i, bank in enumerate(banks):
                    print(f"{i}. Name: {bank.name}")

            choice = int(input("Select a bank: "))
            if choice >= len(banks) or choice < 0:
                print("Invalid choice.")
                return

            selected_bank = banks[choice]

            branches = self.branch_service.get_bank_branches(selected_bank.id)
            for i, branch in enumerate(branches):
                print(f"{i}. Name: {branch.name}")

            print("\n1. Add a new branch")
            print("2. Update existing branch")
            print("3. Remove a branch")
            choice = int(input("Enter your choice (1-3): "))


            if choice == 1:
                self._add_new_branch(selected_bank.id)
            elif choice == 2:
                choice = int(input("Enter branch number you want to update: "))
                if choice >= len(branches) or choice < 0:
                    print("Invalid choice.")
                    return
                self._update_branch_details(branches[choice])
            elif choice == 3:
                choice = int(input("Enter branch number you want to remove: "))
                if choice >= len(branches) or choice < 0:
                    print("Invalid choice.")
                    return
                self._remove_branch(branches[choice].id)
            else:
                print("Invalid choice. Please select a valid option.")


        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
        except Exception as e:
            print(f"An error occurred while managing banks: {str(e)}")

    def _add_new_branch(self, bank_id: str):
        branch_name= input("Enter branch name: ")
        branch_address = input("Enter branch address: ")

        new_branch = Branch(name=branch_name, bank_id=bank_id, address=branch_address)
        self.branch_service.create_new_branch(new_branch)

    def _update_branch_details(self, branch):
        new_branch_name = input("Enter new branch name (leave empty if you dont want to update): ")
        new_branch_address = input("Enter new branch address (leave empty if you dont want to update): ")

        self.branch_service.update_branch_details(branch.id, new_branch_name, new_branch_address)
        print("Branch details updated successfully.")

    def _remove_branch(self, branch_id: str):
        self.branch_service.remove_branch(branch_id)
        print("Branch has been removed successfully.")

    def _monitor_transactions(self):
        """Placeholder for monitoring transactions."""
        print("Monitor Transactions functionality is under development.")

    def _logout(self):
        """Handle admin logout."""
        print("Logging out...")
        self.main_menu()
