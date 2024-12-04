import sqlite3
import src.app.config.config as config


class DB:
    _conn = None  # Renamed to follow naming conventions (private variable)

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of DB exists."""
        if cls._conn is None:
            cls._conn = super().__new__(cls)
            cls._conn._initialize_connection()  # Initialize connection after object creation
        return cls._conn

    def _initialize_connection(self):
        """Initialize the database connection."""
        if not hasattr(self, 'db_conn'):
            # Only initialize the connection if it's not already done
            self.db_conn = sqlite3.connect(config.DB_ADDR)
            self.db_conn.row_factory = sqlite3.Row

    @classmethod
    def get_connection(cls):
        """Return the singleton DB connection."""
        if cls._conn is None:
            cls()  # Calls __new__ and initializes if necessary
        return cls._conn.db_conn  # Return the connection object

    @classmethod
    def close_connection(cls):
        """Close the DB connection (if open)."""
        if cls._conn and hasattr(cls._conn, 'db_conn'):
            cls._conn.db_conn.close()
            cls._conn = None  # Optionally reset the connection after closing
