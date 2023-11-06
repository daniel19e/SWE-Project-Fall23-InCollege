
from database import get_existing_db_object
from util import clear_terminal, inspect_input
import student_profile
from util import convert_24_hour_to_12_hour, format_date
import re


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


def connect_with_student(firstname, lastname):
    if db.search_first_and_last(firstname, lastname):
        print(f"You found {firstname.capitalize()} {lastname.capitalize()}.\n")
        send_connection_request(firstname, lastname)
        return True
    else:
        print(
            f"{firstname.capitalize()} {lastname.capitalize()} is not a member of InCollege.")
        return False


def send_connection_request(from_username, to_username):
    print(f"Connection request sent to {to_username} from {from_username}!")
    # this is not implemented yet


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
        clear_terminal()
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


def show_pending_requests(pending_requests):
    # Display pending requests
    if pending_requests:
        print("Pending Requests:")
        for idx, requester in enumerate(pending_requests):
            print(f"{idx + 1}. {requester[0]}")
        print("\nYour choice to accept (a#) or reject (r#). Ex: 'a1' or 'r1'")


def show_network(connections):
    # Display friends list with profile option if they have one
    print("\nYour Network:")
    for i, connection in enumerate(connections):
        # Using profile_exists to check if friend has a profile
        if db.profile_exists(connection):
            print(
                f"{i + 1}. {connection} - View Profile (press p{i+1}) - Send Message (press m{i+1})")
        else:
            print(f"{i + 1}. {connection}")


def manage_network(username):
    clear_terminal()
    connections = db.get_connections(username)
    while True:
        pending_requests = db.get_pending_requests(username)
        show_pending_requests(pending_requests)
        show_network(connections)
        print("\nMake your selection:")
        print("1. Disconnect from someone")
        print("0. Go back")
        choice = input("\nYour choice: ")

        if choice == '0':
            clear_terminal()
            return
        elif choice == '1':
            disconnect_from_someone(username)

        elif choice.startswith('a'):
            try:
                index = int(choice[1:]) - 1
            except Exception:
                index = -1
            if 0 <= index < len(pending_requests):
                requester = pending_requests[index][0]
                db.accept_friend_request(requester, username)
                clear_terminal()
                print(f"You are now connected with {requester}!")
                return
            clear_terminal()
            print("Invalid request choice.")
            continue
        elif choice.startswith('r'):
            try:
                index = int(choice[1:]) - 1
            except:
                index = -1
            if 0 <= index < len(pending_requests):
                db.reject_friend_request(requester, username)
                clear_terminal()
                print(f"Connection request from {requester} was rejected.")
                return
            clear_terminal()
            print("Invalid request choice.")
            continue
        elif choice.startswith('p'):  # If user wants to view a friend's profile
            try:
                index = int(choice[1:]) - 1
            except:
                index = -1
            if 0 <= index < len(connections) and db.profile_exists(connections[index]):
                student_profile.display_profile(db, connections[index])
                clear_terminal()
            else:
                clear_terminal()
                print("Invalid profile choice or profile does not exist.")
                continue
        else:
            clear_terminal()
            print("Invalid selection!")


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
        confirm = input(
            f"Do you really want to disconnect from {connections[selected - 1]}? (yes/no) ")
        if confirm.lower() == 'yes':
            db.remove_connection(username, connections[selected - 1])
            clear_terminal()
            print(f"Disconnected from {connections[selected - 1]}")
        else:
            clear_terminal()
            print("No changes were made.")
        return
    except Exception:
        clear_terminal()
        print("Invalid selection!")
        return


def send_message(username, receiver, is_plus_tier):
    connections = db.get_connections(username)
    if not db.get_user_info(receiver):
        clear_terminal()
        print("The person you're trying to message is not in the InCollege system.\n")
        return
    if receiver == username:
        clear_terminal()
        print("You cannot send a message to yourself.\n")
        return
    if not is_plus_tier and receiver not in connections:
        clear_terminal()
        print("As a free tier, you must be friends with the person you're trying to message.\n")
        return
    #otherwise, either plus tier, or receiver is in connections
    message = input("Enter the message you want to send (X to cancel): ")
    if inspect_input(message):
        clear_terminal()
        return
    receiver_id = db.get_user_info(receiver)['id']
    sender_id = db.get_user_info(username)['id']
    db.send_message(sender_id, receiver_id, message)
    clear_terminal()
    print("Message sent successfully!\n")


def generate_message_list(username):
    clear_terminal()
    while True:
        user_id = db.get_user_info(username)['id']
        message_list = db.generate_message_list(user_id)
        print("Inbox: \n")
        print("======================================")
        if not message_list:
            print("Your inbox is empty.")
            print("======================================")
        for i, message in enumerate(message_list):
            sender_name = db.get_user_by_id(message['sender'])
            print(f"Message #{i + 1}, sent by {sender_name.capitalize()}:")
            print(f"{message['message']}")
            print("--------------------------------------")
            date, time = message['time'].split()
            formatted_date = format_date(date)
            formatted_time = convert_24_hour_to_12_hour(time)
            print(f"\t{formatted_date} {formatted_time}.")
            print("======================================")
        
        print("\nTo reply to a message, enter: reply [message #]")
        print("To delete a message from your inbox, enter: delete [message #]")
        print("To go back, enter: 0\n")
        user_input = input("Enter your input: ")
        
        if user_input == '0':
            clear_terminal()
            break

        if (re.match(r'^reply \d+$', user_input)):
            message_num = user_input.split()[1]
            message = message_list[int(message_num) - 1]
            receiver = db.get_user_by_id(message['sender'])
            send_message(username, receiver, True)
            continue

        if (re.match(r'^delete \d+$', user_input)):
            message_num = user_input.split()[1]
            message = message_list[int(message_num) - 1]
            db.delete_message_by_id(str(message['id']))
            clear_terminal()
            print("Message deleted successfully!\n")
            continue

        clear_terminal()
        print("Error: Invalid input.\n")



def inbox(username):
    clear_terminal()
    while True:
        user_info = db.get_user_info(username)
        user_id = user_info['id']
        message_list = db.generate_message_list(user_id)

        print("Inbox:\n")
        if message_list:
            print(f"You have {len(message_list)} message(s).")
            print(f"------------------------")
        print("1. View Messages")
        print("2. Send a Message")
        print("\n0. Go back")
        choice = input("\nMake your selection: ")

        if choice == '0':
            clear_terminal()
            break
        
        if choice == '1':
            generate_message_list(username)
        
        elif choice == '2':
            print("--------------------------------------")
            print("Available Users: ")
            generate_student_list(not user_info['plus_tier'], username)
            print("--------------------------------------")
            if not user_info['plus_tier']:
                print("* Want to reach more people? Consider subscribing to InCollege+ *")
            receiver = input("Enter the username(not the firstname you see above) of the person you want to message (X to cancel): ")
            if inspect_input(receiver):
                clear_terminal()
                continue
            send_message(username, receiver, user_info['plus_tier'])
        
        clear_terminal()
        print("Error: Invalid input.\n")

# Generate list of student accounts in system.
def generate_student_list(friends_only=False, username=None):
    if friends_only and username:
        students = db.get_connections(username)
        for i, student in enumerate(students):
            print(f"{i + 1}. {student}")
        return
    
    students = db.search_students_by_criteria()
    for i, student in enumerate(students):
        print(f"{i + 1}. {student['firstname']}")