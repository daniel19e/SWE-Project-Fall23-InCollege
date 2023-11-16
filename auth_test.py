import database
import auth
import pytest
from unittest.mock import Mock

# Assuming that the above functions are in a file named auth.py
from auth import create_account

db = database.DatabaseObject("mock_incollege_database.db")


# Cleanup function
def clear_mock_db():
    db.get_cursor().execute("DELETE FROM college_students")


clear_mock_db()


# Setup function
def populate_mock_db(username, firstname, lastname, password):
    db.add_new_student(username, firstname, lastname, password, "testmajor", "testuniv")


# Test if the password is too short (8 characters is minimum)
def test_validate_password_too_short():
    assert auth.validate_password("Test123") is False


# Test if password is too long (12 characters is max)
def test_validate_password_too_long():
    assert auth.validate_password("thispasswordistoolong1234*") is False


# Test if there are special characters needed in the password
def test_validate_password_no_special_character_no_uppercase():
    assert auth.validate_password("test1234") is False


def test_validate_password_no_special_characters():
    assert auth.validate_password("Test1234") is False


# Test if this correct password passes
def test_validate_password():
    assert auth.validate_password("Test123*")


# Creating 15 different accounts to test if only 10 max can be created
def test_create_account(capsys):
    clear_mock_db()
    output = []
    correct_output = [
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    ]

    # Check if max of 10 accounts can be created
    for i in range(1, 16):
        auth.create_account(
            db,
            "test" + str(i),
            "Test123*",
            f"testusername{i}",
            f"testlastname{i}",
            "major",
            "univ",
            "n",
        )
        out, err = capsys.readouterr()
        output.append("successfully" in out)

    # Check if create account needs unique username (these should all cause errors)
    for i in range(1, 6):
        auth.create_account(
            db,
            "test" + str(i),
            "Test123*",
            f"testusername{i}",
            f"testlastname{i}",
            "major",
            "univ",
            "n",
        )
        out, err = capsys.readouterr()
        output.append("successfully" in out)

    assert output == correct_output


# Test login cases
def test_login_account(capsys):
    clear_mock_db()
    output = []
    correct_output = [True, True, True, True, True, False, False, False, False, False]

    for i in range(1, 6):
        populate_mock_db(
            "test" + str(i), f"testusername{i}", f"testlastname{i}", "Test123*"
        )

    # Check if all 5 accounts can be logged into
    for i in range(1, 6):
        auth.login_account(db, "test" + str(i), "Test123*")
        out, err = capsys.readouterr()
        output.append("You have sucessfully logged in" in out)

    # Make sure you can't log in with wrong password for any of the 5 accounts created
    for i in range(1, 6):
        auth.login_account(db, "test" + str(i), "wrongpassword123")
        out, err = capsys.readouterr()
        output.append("Incorrect username/password" not in out)
    assert output == correct_output


@pytest.fixture
def mock_db():
    return Mock()


# checking for legitimacy of firstname, lastname requirement
def test_create_account_requires_firstname_lastname(mock_db):
    mock_db.get_number_of_accounts.return_value = 1
    valid_password = "Karimli11!!"
    invalid_names = [("", "Karimli"), ("Nihat", ""), ("", "")]

    for firstname, lastname in invalid_names:
        try:
            create_account(
                mock_db,
                "nihat_karimli",
                valid_password,
                firstname,
                lastname,
                "major",
                "univ",
                "n",
            )
        except ValueError as e:
            # Assuming the valueError is raised when first or last name is missing
            assert (
                str(e)
                == "First name and Last name are required according to new InCollege rule"
            )
        else:
            pytest.fail("Expected ValueError but none was raised")


# double checking with a predefined valid data
def test_create_account_with_valid_data(mock_db):
    mock_db.get_number_of_accounts.return_value = 1

    # avoid IntegrityError possibility
    create_account(
        mock_db,
        "nihat_karimli",
        "Karimli11!!",
        "Nihat",
        "Karimli",
        "major",
        "univ",
        "n",
    )

    mock_db.add_new_student.assert_called_once_with(
        "nihat_karimli", "Nihat", "Karimli", "Karimli11!!", "major", "univ", False
    )
