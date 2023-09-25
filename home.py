from util import clear_terminal, inspect_input
from social import connect_with_student
from ascii_art import aa_error404

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
  while True:
    print(f"Welcome back, {username}!")
    print("What would you like to do?\n")
    print("A. Search for a job")
    print("B. Find someone I know")
    print("C. Learn a new skill")
    print("D. Connect with other students")
    print("\n0. Logout and go back\n")

    selection = input("Make a selection: ")
    # Search for a job
    if (selection.upper() == 'A'):
      clear_terminal()
      print(aa_error404)
      print("Oops! Under construction 🛠️\n")
      input("Enter any input to go back: ")
      clear_terminal()
    
    # Find someone they know
    elif (selection.upper() == 'B'):
      clear_terminal()
      print(aa_error404)
      print("Oops! Under construction 🛠️\n")
      input("Enter any input to go back: ")
      clear_terminal()
    
    # Learn a new skill
    elif (selection.upper() == 'C'):
      clear_terminal()
      if not display_skills_page():
        continue

    # connect with other students
    elif (selection.upper() == 'D'):
      clear_terminal()
      print("Who do you want to connect with?")
      first = input("Enter their first name: ")
      last = input("Enter their last name: ")

      connect_with_student(first, last)
      input("Enter any input to go back: ")
      clear_terminal()
      
    # Exit
    elif (selection.upper() == '0'):
      clear_terminal()
      break
    
    # Handle Invalid Input
    else:
      clear_terminal()
      print("Error: Invalid choice. Please enter a valid character.\n")