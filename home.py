from util import clear_terminal
from social import connect_with_student, find_someone_i_know, show_my_network
from database import get_existing_db_object
from ascii_art import aa_error404
from pages import *
from auth import logout_account, get_current_username

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
  
def try_posting_job(db, user_info):
      number_jobs = db.get_number_of_jobs()
      if (number_jobs < 5):
        print("Please fill in this job's information")
        title = input("Enter a title: ")
        description = input("Enter a description: ")
        employer = input("Enter an employer: ")
        location = input("Enter a location: ")
        salary = input("Enter a salary: ")

        if (user_info):
          firstname = user_info[2]
          lastname = user_info[3]

          db.add_new_job_post(firstname, lastname, title, description, employer, location, salary)

          clear_terminal()
          print("Job posted Sucessfully!\n")
      else:
        clear_terminal()
        print("Error: Maximum job posts limit reached.\n")

def display_home_page(username):
  user_info = db.get_user_info(username)
  pending_requests = db.get_pending_requests(get_current_username())

  if pending_requests:
      print("----------------------------------\n")
      print("[Notification] - You have " + str(len(pending_requests)) + " pending friend request(s). Go to the 'Friend Requests' tab to accept/reject.\n")
      print("----------------------------------")
      
  print(f"Welcome back, {get_current_username()}!")
  while True:
    print("What would you like to do?\n")
    print("A. Search for a job")
    print("B. Post a job")
    print("C. Find someone I know")
    print("D. Learn a new skill")
    print("E. Connect with other students")
    print("F. Useful Links")
    print("G. Important Links")
    print("H. Show My Network")
    print("J. Friend Requests")
    print("\n0. Logout and go back\n")

    selection = input("Make a selection: ")
    # Search for a job
    if (selection.upper() == 'A'):
      clear_terminal()
      print(aa_error404)
      print("Oops! Under construction 🛠️\n")
      input("Enter any input to go back: ")
      clear_terminal()

    # Post a job
    if (selection.upper() == 'B'):
      clear_terminal()
      try_posting_job(db, user_info)
    
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
      show_my_network(username)

    elif selection.upper() == 'J':
      show_friend_requests()
      
    # Exit
    elif (selection.upper() == '0'):
      clear_terminal()
      logout_account()
      break
    
    # Handle Invalid Input
    else:
      clear_terminal()
      print("Error: Invalid choice. Please enter a valid character.\n")