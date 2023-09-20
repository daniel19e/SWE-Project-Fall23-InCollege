import database
import auth
import sys
import pytest

connection = database.setupSQLite("mock_incollege_database.db")
cursor = connection.cursor()


#Cleanup function
def clear_mock_db():
  cursor.execute("DELETE FROM college_students")


#Setup function
def populate_mock_db(username, password):
  cursor.execute("INSERT INTO college_students (name, pass) VALUES (? , ?)",
                 (username, password))
  connection.commit()


#Test if the password is too short (8 characters is minimum)
def test_validate_password_too_short():
  assert auth.validate_password("Test123") is False


#Test if password is too long (12 characters is max)
def test_validate_password_too_long():
  assert auth.validate_password("thispasswordistoolong1234*") is False


#Test if there are special characters needed in the password
def test_validate_password_no_special_character_no_uppercase():
  assert auth.validate_password("test1234") is False


def test_validate_password_no_special_characters():
  assert auth.validate_password("Test1234") is False


#Test if this correct password passes
def test_validate_password():
  assert auth.validate_password("Test123*")


#Creating 10 different accounts to test if only 5 max can be created
def test_create_account(capsys):
  clear_mock_db()
  output = []
  correct_output = [
      True, True, True, True, True, False, False, False, False, False, False,
      False, False, False, False
  ]

  #Check if max of 5 accounts can be created
  for i in range(1, 11):
    auth.create_account(connection, cursor, "test" + str(i), "Test123*")
    out, err = capsys.readouterr()
    output.append('successfully' in out)

  #Check if create account needs unique username (these should all cause errors)
  for i in range(1, 6):
    auth.create_account(connection, cursor, "test" + str(i), "Test123*")
    out, err = capsys.readouterr()
    output.append('successfully' in out)

  assert output == correct_output


#Test login cases
def test_login_account(capsys):
  clear_mock_db()
  output = []
  correct_output = [
      True, True, True, True, True, False, False, False, False, False
  ]

  for i in range(1, 6):
    populate_mock_db("test" + str(i), "Test123*")

  #Check if all 5 accounts can be logged into
  for i in range(1, 6):
    auth.login_account(cursor, "test" + str(i), "Test123*")
    out, err = capsys.readouterr()
    output.append('You have sucessfully logged in' in out)

  #Make sure you can't log in with wrong password for any of the 5 accounts created
  for i in range(1, 6):
    auth.login_account(cursor, "test" + str(i), "wrongpassword123")
    out, err = capsys.readouterr()
    output.append('Incorrect username/password' not in out)

  assert output == correct_output
