from util import validate_date, input_with_prefill, format_string

def check_exit(command):
    '''Check if the exit command was given.'''
    return command.lower() == 'exit'

def create_or_edit_profile(db, username):
    cursor = db.get_cursor()

    cursor.execute("SELECT * FROM student_profiles WHERE username = ?", (username,))
    existing_profile = cursor.fetchone()

    # Start with a blank profile data dictionary or existing data if available.
    if existing_profile:
        profile_data = dict(zip([desc[0] for desc in cursor.description], existing_profile))
    else:
        profile_data = {"username": username}

    # Define the prompts for user input.
    prompts = [
        ("title", "Enter your title: "),
        ("major", "Enter your major: "),
        ("about", "Enter about: "),
        ("university", "Enter your university: "),
        ("degree", "Enter your degree: "),
        ("years_attended", "Enter your years attended (YYYY-YYYY): ")
    ]

    # Gather user input for the base profile information.
    for field, prompt in prompts:
        prefill = profile_data.get(field, '')
        user_input = input_with_prefill(prompt, prefill)

        # Check for the 'exit' command.
        if check_exit(user_input):
            print("\nSaving and exiting...")
            save_profile(db, profile_data, username)
            return

        if field in ["major", "university"]:  # Adjust this line to include "university"
            user_input = format_string(user_input)

        profile_data[field] = user_input

    # Handle the experience section as a special case.
    for i in range(1, 4):  # Experience entries are 1-indexed.
        print(f"\nEnter details for Experience {i} (leave the title empty to skip):")

        experience = {}
        for field in ["title", "employer", "start", "end", "location", "description"]:
            field_key = f"{field}{i}"  # The key in the profile data.
            prompt = f"{field.capitalize()} date (YYYY-MM-DD): " if "date" in field else f"{field.capitalize()}: "
            prefill = profile_data.get(field_key, '')
            user_input = input_with_prefill(prompt, prefill)

            # Check for the 'exit' command.
            if check_exit(user_input):
                print("\nSaving and exiting...")
                save_profile(db, profile_data, username)
                return

            if field in ["start", "end"] and not validate_date(user_input):
                while not validate_date(user_input):
                    print("Invalid date format. Please follow the YYYY-MM-DD format.")
                    user_input = input(prompt)

            experience[field] = user_input

        # If the title for this experience is empty, we assume no more experiences are forthcoming.
        if not experience["title"]:
            break

        # Save the experience to the profile data.
        for key, value in experience.items():
            profile_data[f"{key}{i}"] = value

    # Save the completed profile.
    save_profile(db, profile_data, username)
    print("\nProfile updated successfully!")

def save_profile(db, profile_data, username):
    cursor = db.get_cursor()
    
    if 'username' in profile_data:
        # Check if we're updating an existing profile or creating a new one.
        cursor.execute("SELECT * FROM student_profiles WHERE username = ?", (username,))
        if cursor.fetchone():
            # Update the existing profile.
            placeholders = ", ".join([f"{key} = ?" for key in profile_data.keys()])
            values = list(profile_data.values())
            sql_query = f"UPDATE student_profiles SET {placeholders} WHERE username = ?"
            cursor.execute(sql_query, values + [username])
        else:
            # Insert a new profile.
            columns = ", ".join(profile_data.keys())
            placeholders = ", ".join(['?'] * len(profile_data))
            sql_query = f"INSERT INTO student_profiles ({columns}) VALUES ({placeholders})"
            cursor.execute(sql_query, list(profile_data.values()))

        db.connection.commit()  # Committing the changes to the database.
    else:
        print("No profile changes to save.")

def display_profile(db, username):
    cursor = db.get_cursor()
    cursor.execute("SELECT * FROM student_profiles WHERE username = ?", (username,))
    profile = cursor.fetchone()

    if profile:
        profile_dict = dict(zip([desc[0] for desc in cursor.description], profile))

        print("\nProfile Details:")
        # Printing general details first, excluding the fields related to experiences.
        general_fields = ["username", "title", "major", "about", "university", "degree", "years_attended"]
        for key in general_fields:
            formatted_key = key.replace("_", " ").capitalize()
            print(f"{formatted_key}: {profile_dict.get(key, '')}")

        # Printing experiences.
        for i in range(1, 4):  # Experience entries are 1-indexed.
            title_key = f"title{i}"
            if profile_dict.get(title_key):
                print(f"\nExperience {i}:")
                exp_keys = ["title", "employer", "start", "end", "location", "description"]
                for exp_key in exp_keys:
                    full_key = f"{exp_key}{i}"
                    # Format the key for printing, capitalizing it and removing underscores.
                    formatted_exp_key = exp_key.capitalize()
                    print(f"{formatted_exp_key}: {profile_dict.get(full_key, '')}")

        # Wait for the user to press Enter to return.
        input("\nPress Enter to return...")
    else:
        print("No profile found!")