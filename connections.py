from database import get_existing_db_object
from social import send_connection_request
from util import clear_terminal

db = get_existing_db_object()


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
            send_connection_request(username, target_student[1])
        else:
            print("Invalid choice.")


def show_my_network(username):
    connections = db.get_connections(username)
    while True:
        clear_terminal()
        print("Your Network:\n")
        for i, connection in enumerate(connections):
            print(f"{i + 1}. {connection}")
        print("1. Disconnect from someone")
        print("\n0. Go back")
        choice = input("Your choice: ")
        if choice == '0':
            clear_terminal()
            return
        elif choice == '1':
            disconnect_from_someone(username)
        else:
            try:
                selected = int(choice)
                print(f"Selected {connections[selected - 1]}")
                input("Press any key to continue...")
            except:
                print("Invalid selection!")
                input("Press any key to continue...")

def disconnect_from_someone(username):
    connections = db.get_connections(username)
    clear_terminal()
    print("Select someone to disconnect from:\n")
    for i, connection in enumerate(connections):
        print(f"{i + 1}. {connection}")
    print("\n0. Go back")
    choice = input("Your choice: ")
    if choice == '0':
        clear_terminal()
        return
    try:
        selected = int(choice)
        confirm = input(f"Do you really want to disconnect from {connections[selected - 1]}? (yes/no) ")
        if confirm.lower() == 'yes':
            db.remove_connection(username, connections[selected - 1])
            print(f"Disconnected from {connections[selected - 1]}")
            input("Press any key to continue...")
        else:
            print("No changes were made.")
            input("Press any key to continue...")
    except:
        print("Invalid selection!")
        input("Press any key to continue...")
