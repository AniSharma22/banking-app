import uuid

class Transaction:
    def __init__(self, sender_acc_id, receiver_acc_id, amount, time_stamp, transaction_type):
        self.id = uuid.uuid4()
        self.sender_acc_id = sender_acc_id
        self.receiver_acc_id = receiver_acc_id
        self.amount = amount
        self.time_stamp = time_stamp
        self.transaction_type = transaction_type




