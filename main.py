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
from auth import login_account, create_account
from database import get_existing_db_object
from home import display_home_page
from util import clear_terminal, inspect_input
from social import promote_marketing_program
from success_story import display_story
from video import play_video
from ascii_art import aa_logo
from pages import *


def driver():
    # Setup SQLite connection
    db = get_existing_db_object()
    # Setup initial variables
    logged_in = False

    clear_terminal()

    print(aa_logo)
    display_story()
    promote_marketing_program()

    # Main Functionality
    while True:
        print(aa_logo)
        print("1. Log in with an existing account")
        print("2. Create a new account")
        print("3. Watch a video: \"Why should I join InCollege?\"")
        print("4. Useful links")
        print("5. Important links")
        print("\n0. Exit\n")

        start_choice = input("Select an option: ")

        # Login
        if start_choice == '1':
            print("\n(Enter X to cancel)")
            
            username = input("Enter username: ")
            if inspect_input(username): clear_terminal(); continue

            password = input("Enter password: ")
            if inspect_input(password): clear_terminal(); continue

            clear_terminal()

            logged_in = login_account(db, username, password)

            if logged_in:
                display_home_page(username)
                # Logout after leaving home page (when the loop breaks)
                logged_in = False

        # Register
        elif start_choice == '2':
            if sign_up_page() == False:
                continue
            
        # Video
        elif start_choice == '3':
            play_video()
            clear_terminal()
        
        elif start_choice == '4':
            show_useful_links()

        elif start_choice == '5':
            show_incollege_important_links()
        # Exit
        elif start_choice == '0':
            print("\nShutting down program and database . . .")
            db.close_connection()
            
            print("Exited Successfully!")
            break

        # Handle Invalid Input
        else:
            clear_terminal()
            print("Error: Invalid command, please select a valid option.")


if __name__ == '__main__':
    driver()
