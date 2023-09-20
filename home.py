from util import clear_terminal, print_404


def display_home_page(username):
  home = 1
  while home == 1:
    print(f"Welcome back, {username}!")
    print("What would you like to do?\n")
    print("A. Search for a job")
    print("B. Find someone I know")
    print("C. Learn a new skill")
    print("D. Logout \n")

    selection = input("Make a selection: ")

    # Search for a job
    if (selection.upper() == 'A'):
      clear_terminal()
      print_404()
      print("Oops! Under construction 🛠️\n")
      input("Enter any input to go back: ")
      clear_terminal()
    
    # Find someone they know
    elif (selection.upper() == 'B'):
      clear_terminal()
      print_404()
      print("Oops! Under construction 🛠️\n")
      input("Enter any input to go back: ")
      clear_terminal()
    
    # Learn a new skill
    elif (selection.upper() == 'C'):
      clear_terminal()
      print("Learn a new skill:\n")
      print("1. Be a billionaire:")
      print("2. Learn to fly")
      print("3. Travel back in time")
      print("4. Meaning of life")
      print("5. Actually understand how Python works\n")
      choice = input("Select a skill to learn (1-5) or " \
                     "enter any other digit to go back: ")
      input_array = ['1', '2', '3', '4', '5']
      if choice in input_array:
        clear_terminal()
        print_404()
        print("Oops! Under construction 🛠️\n")
        input("Enter any input to go back: ")
        clear_terminal()
      else:
        clear_terminal()
        continue
    
    # Exit
    elif (selection.upper() == 'D'):
      clear_terminal()
      home = 0
      break
    
    # Handle Invalid Input
    else:
      clear_terminal()
      print("Error: Invalid choice. Please enter a valid character.\n")