
from database import get_existing_db_object
from util import clear_terminal

db = get_existing_db_object()
def promote_marketing_program():
    """prior to logging into the system, the user can enter first and last name to check if they're part of the program"""
    print("Welcome to InCollege, as part of our marketing program, we'd like to check if you're part of our system before you log in or sign up.")
    first = input("Enter your first name: ")
    last = input("Enter your last name: ")
    is_a_member = db.search_first_and_last(first.lower(), last.lower())
    
    clear_terminal()
    
    if is_a_member:
        print("You are a part of the InCollege system.")
    else:
        print("You are not a part of the InCollege system yet.")
        
def send_connection_request(firstname, lastname):
    pass

def connect_with_student(firstname, lastname):
    if db.search_first_and_last(firstname, lastname):
        print(f"You found {firstname.capitalize()} {lastname.capitalize()}.\n")
        send_connection_request(firstname, lastname)
        return True
    else:
        print(f"{firstname.capitalize()} {lastname.capitalize()} is not a member of InCollege.")
        return False

def send_connection_request(from_username, to_username):
    print(f"Connection request sent to {to_username} from {from_username}!")

def find_someone_i_know(username):
    clear_terminal()
    print("Find someone you know by:")
    print("1. Last name")
    print("2. University")
    print("3. Major")
    print("\n0. Go back\n")
    
    choice = input("Make a selection: ")

    criteria = {}
    if choice == '1':
        criteria['lastname'] = input("Enter the last name: ")
    elif choice == '2':
        criteria['university'] = input("Enter the university: ")
    elif choice == '3':
        criteria['major'] = input("Enter the major: ")
    elif choice == '0':
        clear_terminal()
        return
    else:
        clear_terminal()
        print("Invalid choice.")
        return

    results = db.search_students_by_criteria(**criteria)
    
    if not results:
        print("No students found with the provided criteria.")
    else:
        print("\nResults:")
        for idx, student in enumerate(results):
            print(f"{idx + 1}. {student[2]} {student[3]} - {student[1]}")
        print("\nSelect a student to send a connection request or enter 0 to go back.")
        
        connection_choice = input("Your choice: ")
        
        if connection_choice == '0':
            clear_terminal()
            return
        elif 0 < int(connection_choice) <= len(results):
            target_student = results[int(connection_choice) - 1]
            db.send_friend_request(username, target_student[1])
            clear_terminal()
            print("Connection request sent!")
            return
        else:
            clear_terminal()
            print("Invalid choice.")
            return


def show_my_network(username):
    connections = db.get_connections(username)
    while True:
        clear_terminal()
        
        pending_requests = db.get_pending_requests(username)
        if pending_requests:
            print("Pending Requests:")
            for idx, requester in enumerate(pending_requests):
                print(f"{idx + 1}. {requester[0]}")
            print("\nYour choice to accept (a#) or reject (r#). Ex: 'a1' or 'r1'")

        print("Your Network:\n")
        for i, connection in enumerate(connections):
            print(f"{i + 1}. {connection}")
        print("\nMake your selection:")
        print("1. Disconnect from someone")
        print("0. Go back")
        choice = input("\nYour choice: ")

        if choice.startswith('a') or choice.startswith('r'):
            index = int(choice[1:]) - 1
            if 0 <= index < len(pending_requests):
                requester = pending_requests[index][0]
                if choice.startswith('a'):
                    db.accept_friend_request(requester, username)
                    clear_terminal()
                    print(f"You are now connected with {requester}!")
                    return
                else:
                    db.reject_friend_request(requester, username)
                    clear_terminal()
                    print(f"Connection request from {requester} was rejected.")
                    return
                

        elif choice == '0':
            clear_terminal()
            return
        elif choice == '1':
            disconnect_from_someone(username)
        else:
            clear_terminal()
            print("Invalid selection!")
            return

def disconnect_from_someone(username):
    connections = db.get_connections(username)
    clear_terminal()
    print("Select someone to disconnect from:\n")
    for i, connection in enumerate(connections):
        print(f"{i + 1}. {connection}")
    print("\n0. Go back")
    choice = input("\nYour choice: ")
    if choice == '0':
        clear_terminal()
        return
    try:
        selected = int(choice)
        confirm = input(f"Do you really want to disconnect from {connections[selected - 1]}? (yes/no) ")
        if confirm.lower() == 'yes':
            db.remove_connection(username, connections[selected - 1])
            clear_terminal()
            print(f"Disconnected from {connections[selected - 1]}")
            return
        else:
            clear_terminal()
            print("No changes were made.")
            return
    except:
        clear_terminal()
        print("Invalid selection!")
        return