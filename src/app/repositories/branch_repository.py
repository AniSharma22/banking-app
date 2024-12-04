from typing import Union, List

from src.app.models.branch import Branch
from src.app.utils.db.db import DB
from src.app.utils.errors.error import DatabaseError


class BranchRepository:
    def __init__(self, database: DB):
        self.db = database

    def fetch_bank_branches(self, bank_id: str) -> Union[List[Branch], None]:
        conn = self.db.get_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT id, bank_id, name, address FROM branches
            WHERE bank_id = ?
            ''', (bank_id,))

            result = cursor.fetchall()
            if result is None:
                return None
            else:
                return [Branch(id=result[0], bank_id=result[1], name=result[2], address=result[3]) for branch in result]

    def create_branch(self, branch: Branch):
        try:
            conn = self.db.get_connection()
            with conn:
                conn.execute('''
                INSERT INTO branches(id,bank_id, name, address)
                VALUES (?,?,?,?);
                ''', (branch.id, branch.bank_id, branch.name, branch.address))
        except Exception as e:
            raise DatabaseError(str(e))

    def update_branch(self, branch_id: str, new_branch_name: str, new_branch_address: str):
        try:
            conn = self.db.get_connection()
            with conn:
                conn.execute('''
                UPDATE branches
                SET name = ?,address = ?
                WHERE id = ?
                ''', (branch_id, new_branch_name, new_branch_address))
        except Exception as e:
            raise DatabaseError(str(e))

    def delete_branch(self, branch_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                conn.execute('''
                DELETE FROM branches
                WHERE id = ?
                ''', (branch_id,))
        except Exception as e:
            raise DatabaseError(str(e))
