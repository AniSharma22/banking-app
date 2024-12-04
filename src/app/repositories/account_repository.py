from src.app.models.account import Account
from src.app.utils.db.db import DB


class AccountRepository:
    def __init__(self, database: DB):
        self.db = database

    def create_account(self, account: Account):
        conn = self.db.get_connection()
        with conn:
            conn.execute('''
            INSERT INTO accounts (id, user_id, branch_id, bank_id)
            VALUES (?,?,?,?)
            ''', (account.id, account.user_id, account.branch_id, account.bank_id))

    def delete_account(self, account_id: str):
        conn = self.db.get_connection()
        with conn:
            conn.execute('''
            DELETE FROM accounts
            WHERE id = ?
            ''', (account_id,))

    def fetch_user_accounts(self, user_id: str):
        conn = self.db.get_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM accounts
            JOIN 
            
            ''')




