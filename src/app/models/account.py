import uuid


class Account:
    def __init__(self, user_id, branch_id, bank_id, id=None, balance=0):
        self.id = id if id else str(uuid.uuid4())
        self.user_id = user_id
        self.branch_id = branch_id
        self.bank_id = bank_id
        self.balance = balance

    def __repr__(self):
        return (
            f"Account("
            f"id='{self.id}', "
            f"user_id='{self.user_id}', "
            f"branch_id='{self.branch_id}', "
            f"bank_id='{self.bank_id}', "
            f"balance={self.balance})"
        )
