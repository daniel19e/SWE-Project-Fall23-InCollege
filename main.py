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


def promote_marketing_program(cursor):
    """prior to logging into the system, the user can enter first and last name to check if they're part of the program"""
    print("Welcome to InCollege, as part of our marketing program, we'd like to check if you're part of our system before you log in or sign up.")
    first = input("Enter your first name: ")
    last = input("Enter your last name: ")
    cursor.execute("SELECT * FROM college_students WHERE firstname = ? AND lastname = ?",
                   (first, last))
    is_a_member = cursor.fetchone()
    if is_a_member:
        print("You are a part of the InCollege system.\n")
    else:
        print("You are not a part of the InCollege system yet.\n")


def driver(connection):
    cursor = connection.cursor()
    # Setup initial variables
    main = 1
    logged_in = False

    promote_marketing_program(cursor)
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
    driver(connection)
