
from database import get_existing_db_object

db = get_existing_db_object()
def promote_marketing_program():
    """prior to logging into the system, the user can enter first and last name to check if they're part of the program"""
    print("Welcome to InCollege, as part of our marketing program, we'd like to check if you're part of our system before you log in or sign up.")
    first = input("Enter your first name: ")
    last = input("Enter your last name: ")
    is_a_member = db.search_first_and_last(first, last)
    if is_a_member:
        print("You are a part of the InCollege system.\n")
    else:
        print("You are not a part of the InCollege system yet.\n")
        
def send_connection_request(firstname, lastname):
    pass

def connect_with_student(firstname, lastname):
    if db.search_first_and_last(firstname, lastname):
        print(f"\nYou found {firstname.capitalize()} {lastname.capitalize()}.\n")
        send_connection_request(firstname, lastname)
        return True  ###############
    else:
        print(f"{firstname.capitalize()} {lastname.capitalize()} is not a member of InCollege.")
        return False  ###################
