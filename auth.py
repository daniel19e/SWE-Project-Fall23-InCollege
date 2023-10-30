import re
import sqlite3
from database import get_existing_db_object

db = get_existing_db_object()

current_username = ""

def validate_password(password):
  regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[)(}{><_+:@#$%&!?^*]).{8,12}$'
  return bool(re.match(regex, password))


def create_account(db, username, password, firstname, lastname, major, university):
  if not firstname or not lastname:
      raise ValueError("First name and Last name are required according to new InCollege rule")

  if validate_password(password):
    number_accounts = db.get_number_of_accounts()
    if (number_accounts < 10):
      try:
        db.add_new_student(username, firstname, lastname, password, major, university)
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


def login_account(db, username, password):
  login_success = db.is_student_registered(username, password)
  try:
    if (login_success):
      global current_username
      current_username = login_success[1]
      print("You have sucessfully logged in!\n")
    else:
      raise Exception("Invalid Credentials")
  except Exception:
    print("Error: Incorrect username/password. Please try again. \n")

  return login_success

def logout_account():
  global current_username
  current_username = ""

def get_current_username():
  global current_username
  return current_username
