from src.app.models.transaction import Transaction
from src.app.services.account_service import AccountService
from src.app.utils.errors.error import InvalidOperationError, NotExistsError
from src.app.utils.types import TransactionType


class TransactionService:
    def __init__(self, transaction_repository, account_service: AccountService):
        self.transaction_repository = transaction_repository
        self.account_service = account_service

    def create_transaction(self, transaction: Transaction, user_id: str):
        if transaction.transaction_type == TransactionType.DEPOSIT.value:
            self._initiate_deposit(transaction, user_id)
        elif transaction.transaction_type == TransactionType.WITHDRAW.value:
            self._initiate_withdrawal(transaction, user_id)
        elif transaction.transaction_type == TransactionType.TRANSFER.value:
            self._initiate_transfer(transaction, user_id)
        else:
            raise InvalidOperationError('Invalid transaction type')

    def _initiate_withdrawal(self, transaction: Transaction, user_id: str):
        if transaction.sender_acc_id is None:
            raise InvalidOperationError('Sender account id is missing')
        account = self.account_service.get_account_by_id(transaction.sender_acc_id)
        if account is None:
            raise NotExistsError('account does not exist')

        if account.user_id != user_id:
            raise InvalidOperationError('Operation denied')

        self.transaction_repository.make_withdraw_transaction(transaction)

    def _initiate_transfer(self, transaction: Transaction, user_id: str):
        if transaction.sender_acc_id is None or transaction.receiver_acc_id is None:
            raise InvalidOperationError('Sender or receiver account id is missing')

        if transaction.sender_acc_id == transaction.receiver_acc_id:
            raise InvalidOperationError('Cannot transfer money to same account')

        sender_account = self.account_service.get_account_by_id(transaction.sender_acc_id)
        receiver_account = self.account_service.get_account_by_id(transaction.receiver_acc_id)

        if sender_account is None:
            raise NotExistsError('sender account does not exist')

        if receiver_account is None:
            raise NotExistsError('receiver account does not exist')

        if sender_account.user_id != user_id:
            raise InvalidOperationError('Operation denied')

        self.transaction_repository.make_transfer_transaction(transaction)

    def _initiate_deposit(self, transaction: Transaction, user_id: str):
        if transaction.receiver_acc_id is None:
            raise InvalidOperationError('Receiver account id is missing')

        account = self.account_service.get_account_by_id(transaction.receiver_acc_id)

        if account is None:
            raise NotExistsError('account does not exist')
        if account.user_id != user_id:
            raise InvalidOperationError('Operation denied')

        self.transaction_repository.make_deposit_transaction(transaction)

    # This is for users
    def view_transactions(self, user_id: str, account_id: str):
        # check if the account belongs to the user
        account = self.account_service.get_account_by_id(account_id)
        if account is None:
            raise NotExistsError('account does not exist')
        if account.user_id != user_id:
            raise PermissionError('You do not have permission to view transactions')

        return self.transaction_repository.fetch_user_transactions(account_id)
