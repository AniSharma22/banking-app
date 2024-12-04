from src.app.models.account import Account
from src.app.repositories.account_repository import AccountRepository


class AccountService:
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def create_new_account(self, account: Account):
        self.account_repository.create_account(account)


