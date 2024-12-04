from enum import Enum

class Role(Enum):
    USER = 'user'
    ADMIN = "admin"

class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
