from typing import Optional
from src.app.models.user import User
from src.app.utils.db.db import DB
from src.app.utils.errors.error import DatabaseError


class UserRepository:

    def __init__(self, database: DB):
        self.db = database

    def save_user(self, user: User) -> None:
        """Saves a new user to the database."""
        try:
            conn = self.db.get_connection()
            with conn:
                conn.execute('''
                    INSERT INTO users (id, name, email, password, phone_no, address, role)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                ''', (user.id, user.name, user.email, user.password, user.phone_no, user.address, user.role))
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_user_by_email(self, email: str) -> Optional[User]:
        """Fetches a user from the database by their email."""
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, email, password, phone_no, address, role
                    FROM users
                    WHERE email = ?;
                ''', (email,))
                result = cursor.fetchone()

            if result:
                return User(
                    id=result[0],
                    name=result[1],
                    email=result[2],
                    password=result[3],
                    phone_no=result[4],
                    address=result[5],
                    role=result[6]
                )
            return None
        except Exception as e:
            raise DatabaseError(str(e))
