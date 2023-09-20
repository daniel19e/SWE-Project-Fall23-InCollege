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
from database import setupSQLite, get_existing_db_object
from home import display_home_page
from util import clear_terminal, print_logo
from social import promote_marketing_program

# Setup SQLite connection
db = get_existing_db_object()
connection = db.get_connection()

def driver():
    cursor = db.get_cursor()
    # Setup initial variables
    main = 1
    logged_in = False
    print_logo()
    promote_marketing_program()
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
                display_home_page(username, cursor)

                # Logout after leaving home page (when the loop breaks)
                logged_in = False

        # Register
        elif start_choice == '2':
            firstname = input("Enter your first name: ")
            lastname = input("Enter your last name: ")
            username = input("Enter new username: ")
            password = input("Enter new password: ")

            clear_terminal()

            create_account(connection, cursor, username,
                           password, firstname, lastname)

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
    driver()
