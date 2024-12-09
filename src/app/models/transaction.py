import uuid


class Transaction:
    def __init__(self, amount: int, transaction_type, sender_acc_id=None, receiver_acc_id=None, time_stamp=None, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.sender_acc_id = sender_acc_id
        self.receiver_acc_id = receiver_acc_id
        if amount < 0:
            raise ValueError("Amount must be positive")
        self.amount = amount
        self.transaction_type = transaction_type
        self.time_stamp = time_stamp
