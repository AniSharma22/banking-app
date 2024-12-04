from typing import List, Union

from src.app.models.bank import Bank
from src.app.repositories.bank_repository import BankRepository


class BankService:
    def __init__(self, bank_repository: BankRepository):
        self.bank_repository = bank_repository

    def get_available_banks_for_user(self, user_id: str) -> Union[List[Bank], None]:
        return self.bank_repository.get_new_banks_for_user(user_id)

    def get_all_banks(self):
        return self.bank_repository.get_all_banks()

    def create_new_bank(self, bank: Bank):
        self.bank_repository.create_bank(bank)

    def update_bank(self, bank_id: str, new_bank_name: str):
        self.bank_repository.update_bank_name(bank_id, new_bank_name)

    def delete_bank(self, bank_id: str):
        self.bank_repository.remove_bank(bank_id)
