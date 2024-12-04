from src.app.models.branch import Branch
from typing import List, Union


class BranchService:
    def __init__(self, branch_repository):
        self.branch_repository = branch_repository

    def get_bank_branches(self, bank_id:str)-> Union[List[Branch], None]:
        return self.branch_repository.fetch_bank_branches(bank_id)

    def create_new_branch(self, branch: Branch):
        self.branch_repository.create_branch(branch)

    def update_branch_details(self, branch_id: str, new_branch_name: str, new_branch_address: str):
        self.branch_repository.update_branch(branch_id, new_branch_name, new_branch_address)

    def remove_branch(self, branch_id: str):
        self.branch_repository.delete_branch(branch_id)
