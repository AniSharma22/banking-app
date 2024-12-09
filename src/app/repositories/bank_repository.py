from src.app.models.bank import Bank
from src.app.utils.db.db import DB
from src.app.utils.errors.error import DatabaseError


class BankRepository:
    def __init__(self, database: DB):
        self.db = database

    def create_bank(self, bank: Bank):
        try:
            conn = self.db.get_connection()
            with conn:
                conn.execute('''
                INSERT INTO banks (id, name)
                VALUES (?, ?);
                ''', (bank.id, bank.name))
        except Exception as e:
            raise DatabaseError(str(e))

    # def get_bank_by_id(self, bank_id: str):
    #     try:
    #         conn = self.db.get_connection()
    #         with conn:
    #             cursor = conn.cursor()
    #             cursor.execute('''
    #             SELECT id, name FROM banks
    #             WHERE id = ?
    #             ''', (bank_id,))
    #             result = cursor.fetchone()
    #
    #         if result:
    #             return Bank(
    #                 id=result[0],
    #                 name=result[1],
    #             )
    #         else:
    #             return None
    #     except Exception as e:
    #         raise DatabaseError(str(e))

    def get_all_banks(self):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT id, name FROM banks
                ''')
                results = cursor.fetchall()

            return [Bank(id=bank[0], name=bank[1]) for bank in results] if results else []
        except Exception as e:
            raise DatabaseError(str(e))

    def get_new_banks_for_user(self, user_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT b.id, b.name 
                FROM banks b
                WHERE NOT EXISTS (
                    SELECT 1 
                    FROM accounts a 
                    WHERE a.bank_id = b.id AND a.user_id = ?
                )
                ''', (user_id,))
                results = cursor.fetchall()

            return [Bank(id=bank[0], name=bank[1]) for bank in results] if results else []
        except Exception as e:
            raise DatabaseError(str(e))

    def update_bank_name(self, bank_id: str, new_bank_name: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                UPDATE banks
                SET name = ?
                WHERE id = ?''', (new_bank_name, bank_id))
        except Exception as e:
            raise DatabaseError(str(e))

    def remove_bank(self, bank_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                DELETE FROM banks
                WHERE id = ?''', (bank_id,))
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_user_banks(self, user_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT b.id, b.name
                    FROM banks b
                    INNER JOIN accounts a ON b.id = a.bank_id
                    WHERE a.user_id = ?;    
                ''', (user_id,))
                results = cursor.fetchall()
                return [Bank(id=row[0], name=row[1]) for row in results] if results else []
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_bank_by_id(self, bank_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name
                    FROM banks
                    WHERE id = ?;    
                ''', (bank_id,))
                results = cursor.fetchone()
                return Bank(id=results[0], name=results[1]) if results else None
        except Exception as e:
            raise DatabaseError(str(e))
