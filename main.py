"""
***********************************************************************
*               InCollege Application - Team California               *
***********************************************************************
*  Description:    Simple program that simulates a social media platform
*                  similar to LinkedIn, but for college students.
*
*  Developed By:   Daniel Escalona Gonzalez
*                  Eloy Fernandes Ballesteros
*                  Jason Greb
*                  Massimo Giannini
*                  Shahaddin Gafarov
_______________________________________________________________________
"""

import sqlite3

from auth import create_account, login_account
from database import setupSQLite
from home import display_home_page
from util import clear_terminal, print_logo

# Setup SQLite connection
connection = setupSQLite("incollege_database.db")


def driver(connection):
  cursor = connection.cursor()
  # Setup initial variables
  main = 1
  logged_in = False

  # Main Functionality
  while main == 1:
    print_logo()
    print("1. Log in with an existing account")
    print("2. Create a new account")
    print("3. Exit\n")

    start_choice = input("Select an option: ")

    # Login
    if start_choice == '1':
      username = input("Enter username: ")
      password = input("Enter password: ")

      clear_terminal()

      logged_in = login_account(cursor, username, password)

      if logged_in:
        display_home_page(username)

        # Logout after leaving home page (when the loop breaks)
        logged_in = False

    # Register
    elif start_choice == '2':
      username = input("Enter new username: ")
      password = input("Enter new password: ")

      clear_terminal()

      create_account(connection, cursor, username, password)

    # Exit
    elif start_choice == '3':
      clear_terminal()

      print("Shutting down program and database...")
      connection.close()
      main = 0

      print("Exited Successfully!")
      break

    # Handle Invalid Input
    else:
      clear_terminal()
      print("Error: Invalid command, please select a valid option.")


if __name__ == '__main__':
  driver(connection)
