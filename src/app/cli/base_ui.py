from src.app.services.account_service import AccountService
from src.app.services.bank_service import BankService
from src.app.services.branch_service import BranchService
from src.app.services.user_service import UserService


class BaseUI:
    def __init__(self, user_service: UserService, bank_service: BankService, branch_service: BranchService, account_service: AccountService):
        self.user_service = user_service
        self.bank_service = bank_service
        self.branch_service = branch_service
        self.account_service = account_service
