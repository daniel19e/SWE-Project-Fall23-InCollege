import re
from util import clear_terminal
from database import get_existing_db_object

db = get_existing_db_object()

def job_listing(user_info):
    handle_job_deletion(user_info)
    
    while True:
        print("1. List All Jobs/Internships")
        print("2. Applied Jobs")
        print("3. Saved Jobs\n")
        print("0. Go Back\n")

        selection = input("Enter your selection: ")
        if (selection == '0'):
            clear_terminal()
            break
        
        if (selection == '1'):
            clear_terminal()
            view_jobs_interns(user_info)
            continue
        
        if (selection == '2'):
            clear_terminal()
            display_applied_jobs(user_info)
            continue
        
        if (selection == '3'):
            clear_terminal()
            display_saved_jobs(user_info)
            continue
    
        clear_terminal()
        print("Error: Invalid input.\n")

#list of all jobs/interns available
def view_jobs_interns(user_info):
    detail_job = -1
    
    while True:
        all_jobs = db.get_jobs()
        applied_jobs_ids = db.get_applications_of_student(user_info['id'])

        print("List of all Jobs/Interns:\n")
        for job in all_jobs:
            if (job['id'] == int(detail_job)):
                print("------------------------------------------------")
                print(f"Job ID: #{job['id']}") 
                #print(f"Poster's firstname: {job['firstname']}")
                #print(f"Poster's lastname: {job['lastname']}")
                print(f"Title: {job['title']}")
                print(f"Description: {job['description']}")
                print(f"Employer: {job['employer']}")
                print(f"Location: {job['location']}")
                print(f"Salary: {job['salary']}")
                if job['firstname'] == user_info['firstname'] and job['lastname'] == user_info['lastname']:
                    print("Status: You own this job post.")
                elif job['id'] in applied_jobs_ids:
                    print("Status: APPLIED!")
                else:
                    print("Status: Available.")
                print("------------------------------------------------")
                continue
            
            if job['firstname'] == user_info['firstname'] and job['lastname'] == user_info['lastname']:
                application_status = "You own this job post."
                print(f"Job ID: {job['id']}, Job Title: {job['title']}, Status: {application_status}")
                continue
            
            if job['id'] in applied_jobs_ids:
                application_status = "APPLIED!"
            else:
                application_status = "Available."
            
            print(f"Job ID: {job['id']}, Job Title: {job['title']}, Status: {application_status}")
        print("\n=============================================\n")
        
        print("To expand a job's details, enter: [job ID]")
        print("To apply for a job, enter: apply [job ID]")
        print("To add a job to your saved list, enter: save [job ID]")
        print("To go back, enter: 0\n")
        user_input = input("Enter input: ")

        if (user_input == '0'):
            clear_terminal()
            break

        if (re.match(r'^apply \d+$', user_input)):
            job_id = user_input.split()[1]
            apply_jobs_interns(user_info, int(job_id))
            detail_job = -1
            continue

        if (re.match(r'^save \d+$', user_input)):
            job_id = user_input.split()[1]
            db.add_saved_job(job_id, user_info['id'])
            clear_terminal()
            detail_job = -1
            print(f"Sucessfully Saved Job #{job_id}!\n")
            continue
        
        if (re.match(r'^[0-9]+$', user_input)):
            detail_job = user_input
            clear_terminal()
            continue

        clear_terminal()
        print("Error: Invalid input.\n")


#job application
def apply_jobs_interns(student_info, job_id):
    job = db.get_job_by_id(job_id)
    if not job:
        clear_terminal
        print("Error: Invalid Job ID.\n")
        return

    if job['firstname'] == student_info['firstname'] and job['lastname'] == student_info['lastname']:
      clear_terminal()
      print("You cannot apply for your own job post.\n")
      return

    if db.already_applied(student_info['id'], job_id):
        clear_terminal()
        print("You have already applied for this job.\n")
        return

    graduation_date = input("Enter your graduation date (mm/dd/yyyy): ")
    start_date = input("Enter your start date (mm/dd/yyyy): ")
    student_application = input("Explain why you are a good fit for this job: ")

    application = {"job_id": job_id, "student_id": student_info['id'], "graduation_date": graduation_date, "start_date": start_date, "student_application": student_application}
    db.add_applications(application)
    clear_terminal()
    print("Application submitted successfully!\n")
        
def my_job_postings(user_info):
    while True:
        all_jobs = db.get_jobs()
        job_num = 0

        print("============= My Job Postings ============\n")
        for job in all_jobs:
            if job['firstname'] == user_info['firstname'] and job['lastname'] == user_info['lastname']:
                job_num += 1
                print(f"Job ID: {job['id']}, Job Title: {job['title']}")

        if (job_num == 0):
            print("You haven't posted any jobs yet.")

        print("\n=========================================\n")
        print("1. Post New Job")
        print("2. Delete Job by ID\n")
        print("0. Go back\n")
        
        selection = input("Enter your selection: ")
        if(selection == '1'):
            try_posting_job(db, user_info)
            continue
            
        if(selection == '2'):
            try_deleting_job(user_info)
            continue

        if(selection == '0'):
            clear_terminal()
            break

        clear_terminal()
        print("Error: Invalid Input.\n")

def try_deleting_job(user_info):
    select = input("Enter the ID of the job you would like to remove (or X to cancel): ")

    if (select.upper == 'X'):
        clear_terminal()
        return
    
    if (re.match(r'^[0-9]+$', select)):
        all_jobs = db.get_jobs()

        for job in all_jobs:
            if job['id'] == int(select) and job['firstname'] == user_info['firstname'] and job['lastname'] == user_info['lastname']:
                db.remove_job_post(select)
                clear_terminal()
                print("Job deleted sucessfully!\n")
                return
        
    clear_terminal()
    print("Error: Invalid input and/or incorrect job ID.\n")
                

def try_posting_job(db, user_info):
      number_jobs = db.get_number_of_jobs()
      if (number_jobs < 10):
        print("Please fill in this job's information (or enter X to cancel)")
        title = input("Enter a title: ")
        if (title.upper() == 'X'):
            clear_terminal()
            return
        description = input("Enter a description: ")
        if (description.upper() == 'X'):
            clear_terminal()
            return
        employer = input("Enter an employer: ")
        if (employer.upper() == 'X'):
            clear_terminal()
            return
        location = input("Enter a location: ")
        if (location.upper() == 'X'):
            clear_terminal()
            return
        salary = input("Enter a salary: ")
        if (salary.upper() == 'X'):
            clear_terminal()
            return

        if (user_info):
          firstname = user_info[2]
          lastname = user_info[3]

          db.add_new_job_post(firstname, lastname, title, description, employer, location, salary)

          clear_terminal()
          print("Job posted Sucessfully!\n")
      else:
        clear_terminal()
        print("Error: Maximum job posts limit reached.\n")

def display_applied_jobs(user_info):
    all_jobs = db.get_jobs()
    applied_jobs_ids = db.get_applications_of_student(user_info['id'])

    print("Jobs/Interns You Have Applied For:\n")
    for job in all_jobs:
        if job['id'] in applied_jobs_ids:
            print(f"Job ID: {job['id']}, Job Title: {job['title']}")
    print("\n=============================================\n")
    
    input("Enter any key to go back: ")
    clear_terminal()

def display_saved_jobs(user_info):
    while True:
        all_jobs = db.get_jobs()
        saved_jobs_ids = db.get_saved_jobs(user_info['id'])

        print("Saved Jobs/Interns:\n")
        for job in all_jobs:
            if job['id'] in saved_jobs_ids:
                print(f"Job ID: {job['id']}, Job Title: {job['title']}")
        print("\n=============================================\n")
        
        print("To remove a job from your saved list, enter: remove [job_id]")
        print("To go back, enter: 0\n")
        user_input = input("Enter an input: ")

        if (user_input == '0'):
            clear_terminal()
            break

        if (re.match(r'^remove \d+$', user_input)):
            job_id = user_input.split()[1]
            db.remove_saved_job(job_id, user_info['id'])
            clear_terminal()
            print(f"Sucessfully removed job #{job_id} from saved list.\n")
            continue

        clear_terminal()
        print("Error: Invalid input.\n")

def handle_job_deletion(user_info):
    all_jobs = db.get_jobs()
    applied_jobs_ids = db.get_applications_of_student(user_info['id'])
    saved_jobs_ids = db.get_saved_jobs(user_info['id'])

    deleted_jobs = []

    for job_id in applied_jobs_ids:
        job = db.get_job_by_id(job_id)
        if not job:
            deleted_jobs.append(job_id)
            db.remove_application(job_id, user_info['id'])
    
    for job_id in saved_jobs_ids:
        job = db.get_job_by_id(job_id)
        if not job:
            if not(job_id in deleted_jobs):
                deleted_jobs.append(job_id)
            db.remove_saved_job(job_id, user_info['id'])
    
    if (len(deleted_jobs) > 0):
        print("----------------------------------")
        print('[Notification] - One or more jobs you have applied for or saved, have been deleted.')
        for job_id in deleted_jobs:
            print(f"Job ID #{job_id}")
        print("----------------------------------\n")