import uuid


class Branch:
    def __init__(self, name, bank_id: str, address, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.bank_id = bank_id
        self.name = name
        self.address = address


