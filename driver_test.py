import pytest
from unittest.mock import patch, Mock
from main import driver
from database import DatabaseObject

# Create a mock database object
def create_mock_db():
    db = Mock(spec=DatabaseObject)
    db.get_number_of_accounts.return_value = 0  # Mock the number of accounts to 0
    db.is_student_registered.return_value = False  # Mock student registration
    return db

# Test case for exiting while creating an account 
def test_exit_while_creating_account(capsys):
    # Create a mock database object
    mock_db = create_mock_db()

    # Use patch to replace the actual database with the mock database
    with patch('main.get_existing_db_object', return_value=mock_db):
        with patch('builtins.input', side_effect=['2', 'X', '0']):
            driver()
            out, _ = capsys.readouterr()
            assert "Exited Successfully!" in out



def test_exit_while_logging_in(capsys):
    mock_db = create_mock_db()
    with patch('main.get_existing_db_object', return_value=mock_db):
        with patch('builtins.input', side_effect=['1', 'X', '0']):  # '2' to start account creation, 'X' to cancel, '0' to exit
            driver()
            out, _ = capsys.readouterr()
            assert "Exited Successfully!" in out
           


if __name__ == '__main__':
    pytest.main()