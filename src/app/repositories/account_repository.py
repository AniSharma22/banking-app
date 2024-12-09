from operator import truediv

from src.app.models.account import Account
from src.app.models.transaction import Transaction
from src.app.utils.db.db import DB
from src.app.utils.errors.error import DatabaseError


class AccountRepository:
    def __init__(self, database: DB):
        self.db = database

    def create_account(self, account: Account):
        try:
            conn = self.db.get_connection()
            with conn:
                conn.execute('''
                INSERT INTO accounts (id, user_id, branch_id, bank_id)
                VALUES (?,?,?,?)
                ''', (account.id, account.user_id, account.branch_id, account.bank_id))
        except Exception as e:
            raise DatabaseError(str(e))

    def delete_account(self, account_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                conn.execute('''
                        DELETE FROM accounts
                        WHERE id = ?
                        ''', (account_id,))
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_user_accounts(self, user_id: str):
        pass

    def fetch_account_by_id(self, account_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT id, user_id, branch_id, bank_id, balance FROM accounts
                WHERE id = ?
                ''', (account_id,))
                result = cursor.fetchone()
                return Account(id=result[0], user_id=result[1], branch_id=result[2], bank_id=result[3], balance=result[4]) if result else None
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_all_user_accounts(self, user_id):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT id,user_id,branch_id,bank_id,balance FROM accounts
                WHERE user_id = ?
                ''', (user_id,))
                result = cursor.fetchall()

                return [
                    Account(id=account[0], user_id=account[1], branch_id=account[2], bank_id=account[3], balance=account[4])
                    for account in result] if result else []
        except Exception as e:
            raise DatabaseError(str(e))

    def user_account_exists(self, user_id, bank_id):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT * FROM accounts 
                WHERE user_id = ? AND bank_id = ?
                ''',(user_id, bank_id))
                result = cursor.fetchone()

                if result is not None:
                    return True
                else:
                    return False
        except Exception as e:
            raise DatabaseError(str(e))
