import re
import sqlite3


def validate_password(password):
  regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[)(}{><_+:@#$%&!?^*]).{8,12}$'
  return bool(re.match(regex, password))


def create_account(connection, cursor, username, password, firstname, lastname):
  if validate_password(password):
    cursor.execute("SELECT COUNT(*) FROM college_students")
    number_accounts = cursor.fetchone()[0]
    if (number_accounts < 5):
      try:
        cursor.execute(
            "INSERT INTO college_students (username, firstname, lastname, pass) VALUES (? , ?, ?, ?)",
            (username, firstname, lastname, password))
        connection.commit()
        print("You have successfully created an account!\n")
      except sqlite3.IntegrityError:
        print("Error: User already exists. Please try another username.\n")
    else:
      print(
          "Error: All permitted accounts have been created. Please come back later.\n"
      )
  else:
    print("Error: Invalid password.\n" \
          "Your password must meet the following criteria:\n" \
          "- Be between 8 and 12 characters long.\n" \
          "- Contain at least one uppercase letter.\n" \
          "- Contain at least one digit.\n" \
          "- Contain at least one special character.\n")


def login_account(cursor, username, password):
  cursor.execute("SELECT * FROM college_students WHERE username = ? AND pass = ?",
                 (username, password))

  login_success = cursor.fetchone()

  try:
    if (login_success):
      print("You have sucessfully logged in!\n")
    else:
      raise Exception("Invalid Credentials")
  except Exception:
    print("Error: Incorrect username/password. Please try again. \n")

  return login_success
