from unittest.mock import MagicMock

import pytest

from src.app.models.bank import Bank
from src.app.repositories.bank_repository import BankRepository


@pytest.fixture
def mock_db():
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db = MagicMock()

    # Simulate the connection returning the mocked cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_db.get_connection.return_value = mock_conn

    return mock_db, mock_conn, mock_cursor

@pytest.fixture
def bank_repository(mock_db):
    return BankRepository(database=mock_db[0])


def test_create_bank(bank_repository,mock_db):
    mock_db,mock_conn, mock_cursor = mock_db[0],mock_db[1], mock_db[2]

    test_bank = Bank(name="Test Bank")

    bank_repository.create_bank(test_bank)

    query, values = mock_conn.execute.call_args[0]
    mock_db.get_connection.assert_called_once()
    mock_conn.execute.assert_called_once()
    assert "INSERT INTO BANKS" in query
    assert


