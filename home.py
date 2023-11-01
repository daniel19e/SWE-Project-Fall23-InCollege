from util import clear_terminal
from social import connect_with_student, find_someone_i_know, manage_network, send_message_to_friend, generate_message_list
from database import get_existing_db_object
from ascii_art import aa_error404
from pages import *
from auth import logout_account, get_current_username
from student_profile import create_or_edit_profile, display_profile
from jobs import job_listing, my_job_postings


db = get_existing_db_object()


def display_skills_page():
    print("Learn a new skill:\n")
    print("1. Be a billionaire:")
    print("2. Learn to fly")
    print("3. Travel back in time")
    print("4. Meaning of life")
    print("5. Actually understand how Python works")
    print("\n0. Go back\n")
    choice = input("Select a skill to learn (1-5): ")
    if choice == '0':
        clear_terminal()
        return True

    input_array = ['1', '2', '3', '4', '5']
    if choice in input_array:
        clear_terminal()
        print(aa_error404)
        print("Oops! Under construction 🛠️\n")
        input("Enter any input to go back: ")
        clear_terminal()
        return True
    else:
        print("Skill not available.")
        clear_terminal()
        return False


def display_home_page(username):
    user_info = db.get_user_info(username)
    pending_requests = db.get_pending_requests(get_current_username())

    if pending_requests:
        print("----------------------------------")
        print("[Notification] - You have " + str(len(pending_requests)) +
              " pending friend request(s). Go to the 'Friend Requests' tab to accept/reject.\n")
        print("----------------------------------\n")

    print(f"Welcome back, {get_current_username()}!")
    while True:
        print("What would you like to do?\n")
        print("A. Job Search/Internship")
        print("B. My Job Postings")
        print("C. Find Someone I Know")
        print("D. Learn a New Skill")
        print("E. Connect With Other Students")
        print("F. Useful Links")
        print("G. Important Links")
        print("H. Show My Network")
        print("I. Profile")
        print("J. Friend Requests")
        print("K. Inbox")
        print("\n0. Logout and go back\n")

        selection = input("Make a selection: ")

        # Search for a job
        if (selection.upper() == 'A'):
            clear_terminal()
            job_listing(user_info)
            continue

        # Post/Delete a job
        if (selection.upper() == 'B'):
            clear_terminal()
            my_job_postings(user_info)

        # Find someone they know
        elif (selection.upper() == 'C'):
            clear_terminal()
            find_someone_i_know(username)

        # Learn a new skill
        elif (selection.upper() == 'D'):
            clear_terminal()
            if not display_skills_page():
                continue

        # connect with other students
        elif (selection.upper() == 'E'):
            clear_terminal()
            print("Who do you want to connect with?")
            first = input("Enter their first name: ")
            last = input("Enter their last name: ")
            connect_with_student(first, last)
            input("Enter any input to go back: ")
            clear_terminal()

        elif (selection.upper() == 'F'):
            show_useful_links()

        elif (selection.upper() == 'G'):
            show_incollege_important_links()

        elif selection.upper() == 'H':
            manage_network(username)

        elif selection.upper() == 'J':
            show_friend_requests()

        elif selection.upper() == 'I':
            clear_terminal()
            print("1.Create/Edit Profile")
            print("2.View Profile")
            print("Press any key to return back")
            selection = input("Choose your option: ")
            if selection == '1':
                create_or_edit_profile(db, username)
            elif selection == '2':
                display_profile(db, username)
            else:
                print("Send a Message")

        elif selection.upper() == 'K':
            generate_message_list(username)

        # Exit
        elif (selection.upper() == '0'):
            clear_terminal()
            logout_account()
            break

        # Handle Invalid Input
        else:
            clear_terminal()
            print("Error: Invalid choice. Please enter a valid character.\n")
