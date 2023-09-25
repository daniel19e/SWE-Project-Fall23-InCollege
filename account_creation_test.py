import pytest
from unittest.mock import Mock

# Assuming that the above functions are in a file named auth.py
from auth import create_account

@pytest.fixture
def mock_db():
    return Mock()

#checking for legitimacy of firstname, lastname requirement
def test_create_account_requires_firstname_lastname(mock_db):
    mock_db.get_number_of_accounts.return_value = 1
    valid_password = "Karimli11!!"
    invalid_names = [("", "Karimli"), ("Nihat", ""), ("", "")]
    
    for firstname, lastname in invalid_names:
        try:
            create_account(mock_db, "nihat_karimli", valid_password, firstname, lastname)
        except ValueError as e:
            # Assuming the valueError is raised when first or last name is missing
            assert str(e) == "First name and Last name are required according to new InCollege rule"
        else:
            pytest.fail("Expected ValueError but none was raised")

#double checking with a predefined valid data
def test_create_account_with_valid_data(mock_db):
    mock_db.get_number_of_accounts.return_value = 1

    #avoid IntegrityError possibility
    create_account(mock_db, "nihat_karimli", "Karimli11!!", "Nihat", "Karimli")

    mock_db.add_new_student.assert_called_once_with("nihat_karimli", "Nihat", "Karimli", "Karimli11!!")
