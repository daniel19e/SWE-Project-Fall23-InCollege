from util import clear_terminal
from social import connect_with_student, find_someone_i_know, show_my_network
from database import get_existing_db_object
from ascii_art import aa_error404
from pages import *
from auth import logout_account, get_current_username
from student_profile import create_or_edit_profile, display_profile


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
      if (number_jobs < 10):
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

#list of all jobs/interns available
def view_jobs_interns(db):
  number_jobs = db.get_number_of_jobs()
  if(number_jobs):
    all_jobs = db.get_jobs()  
    for job in all_jobs:
        print("\nJob Details:")
        print(f"Job ID: #{job['id']}") 
        #print(f"Poster's firstname: {job['firstname']}")
        #print(f"Poster's lastname: {job['lastname']}")
        print(f"Title: {job['title']}")
        print(f"Description: {job['description']}")
        print(f"Employer: {job['employer']}")
        print(f"Location: {job['location']}")
        print(f"Salary: {job['salary']}") 
  else:
    clear_terminal()
    print("There are no jobs to show.\n")

#job application
def apply_jobs_interns(db, student_info, job_id):
    job = db.get_job_by_id(job_id)
    if not job:
        print("Invalid Job ID!")
        return

    if job['firstname'] == student_info['firstname'] and job['lastname'] == student_info['lastname']:
      print("You cannot apply for your own job post.")
      return

    if db.already_applied(student_info['id'], job_id):
        print("You have already applied for this job.")
        return

    graduation_date = input("Enter your graduation date (mm/dd/yyyy): ")
    start_date = input("Enter your start date (mm/dd/yyyy): ")
    student_application = input("Explain why you are a good fit for this job: ")

    application = {"job_id": job_id, "student_id": student_info['id'], "graduation_date": graduation_date, "start_date": start_date, "student_application": student_application}
    db.add_applications(application)
    print("Application submitted successfully!")

#generated list of applied/not-applied jobs + enter job ID
def application_status(db, student_info):
    all_jobs = db.get_jobs()
    applied_jobs_ids = db.get_applications_of_student(student_info['id'])

    print("Generated list of Job/Intern Application(s):")
    for job in all_jobs:
        if job['firstname'] == student_info['firstname'] and job['lastname'] == student_info['lastname']:
            application_status = "You can not apply here, this is your own job post."
            print(f"\nJob ID: {job['id']}, Status: {application_status}")
            continue
        
        if job['id'] in applied_jobs_ids:
            application_status = "APPLIED!"
        else:
            application_status = "Available"
        print(f"\nJob ID: {job['id']}, Status: {application_status}")
    
    job_id = input("Enter the ID of the job to apply for or '0' to go back: ")
    if job_id != '0':
        apply_jobs_interns(db, student_info, int(job_id))

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
    print("A. Job Search/Internship and Application")
    print("B. Post a job")
    print("C. Find someone I know")
    print("D. Learn a new skill")
    print("E. Connect with other students")
    print("F. Useful Links")
    print("G. Important Links")
    print("H. Show My Network")
    print("J. Friend Requests")
    print("I. Profile")
    print("\n0. Logout and go back\n")

    selection = input("Make a selection: ")
    # Search for a job
    if (selection.upper() == 'A'):
      clear_terminal()
      print("Press 1 for list of Jobs/Internships:")
      print("Press 2 for applying Jobs/Internships:")
      print("Press any key to return back:")
      xxx = input()
      if(xxx == '1'):
        clear_terminal()
        view_jobs_interns(db)
        continue
      elif(xxx == '2'):
        clear_terminal()
        application_status(db, user_info)
        continue
      else:
        clear_terminal()
        continue
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

    elif selection.upper() == 'I':
      print("1.Create/Edit Profile")
      print("2.View Profile")
      print("Press any key to return back")
      selection = input("Choose your option: ")
      if selection == '1':
        create_or_edit_profile(db, username)
      elif selection == '2':
        display_profile(db, username)
      else:
        break
    # Exit
    elif (selection.upper() == '0'):
      clear_terminal()
      logout_account()
      break
    
    # Handle Invalid Input
    else:
      clear_terminal()
      print("Error: Invalid choice. Please enter a valid character.\n")