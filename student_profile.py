def format_string(s):
    '''Returns the string with each word's first letter capitalized.'''
    return ' '.join(word.capitalize() for word in s.split())

def create_or_edit_profile(db, username):
    cursor = db.get_cursor()
    title = input("Enter your title: ")
    major = format_string(input("Enter your major: "))
    about = input("Enter about yourself: ")

    experiences = []

    for i in range(3):
        print(f"\nEnter details for Experience {i + 1} (Press enter in order to skip):")
        experience_title = input("Title: ")
        if not experience_title:
            #for the other developer, this line deletes the previous record of the experience you have now skipped, if you want the code to keep the previous experience's record, delete these 2 lines and use break
            experiences.append({f"title{i+1}": "", f"employer{i+1}": "", f"start{i+1}": "", f"end{i+1}": "", f"location{i+1}": "", f"description{i+1}": ""})
            continue
        employer = input("Employer: ")
        start_date = input("Date started (YYYY-MM-DD): ")
        end_date = input("Date ended (YYYY-MM-DD): ")
        location = input("Location: ")
        description = input("Description: ")
        experiences.append({f"title{i+1}": experience_title, f"employer{i+1}": employer, f"start{i+1}": start_date, f"end{i+1}": end_date, f"location{i+1}": location, f"description{i+1}": description})

    university = format_string(input("\nEnter University name: "))
    degree = format_string(input("Degree: "))
    years_attended = input("Years attended: ")

    profile_data = {"username": username,
        "title": title,
        "major": major,
        "about": about,
        "university": university,
        "degree": degree,
        "years_attended": years_attended}

    for i, exp in enumerate(experiences):
        profile_data.update(exp)

    cursor.execute("SELECT * FROM student_profiles WHERE username = ?", (username,))
    existing_profile = cursor.fetchone()

    #base code for updating and inserting the database, i have removed data_tuples here as professor said so(it worked)
    if existing_profile:
        placeholder = ", ".join([f"{col} = ?" for col in profile_data.keys()])
        incollege_sqlite = f"UPDATE student_profiles SET {placeholder} WHERE username = ?"
        cursor.execute(incollege_sqlite, list(profile_data.values()) + [username])
        #print("Database Updated")
        db.connection.commit()
    else:
        columns = ", ".join(profile_data.keys())
        placeholders = ", ".join(['?'] * len(profile_data))
        incollege_sqlite = f"INSERT INTO student_profiles ({columns}) VALUES ({placeholders})"
        cursor.execute(incollege_sqlite, list(profile_data.values()))
        #print("Database Inserted")
        db.connection.commit()


def display_profile(db, username):
    cursor = db.get_cursor()
    cursor.execute("SELECT * FROM student_profiles WHERE username = ?", (username,))
    profile = cursor.fetchone()

    if profile:
        print("\nProfile Details:")
        print("Title:", profile[1])
        print("Major:", profile[2])
        print("About:", profile[3])

        count = 4
        for i in range(3):
            if profile[count]:
                print(f"\nExperience {i + 1}:")
                print("Title:", profile[count])
                print("Employer:", profile[count+1])
                print("Start Date:", profile[count+2])
                print("End Date:", profile[count+3])
                print("Location:", profile[count+4])
                print("Description:", profile[count+5])
                count = count + 6
        print("\nEducation:")
        print("University:", profile[22])
        print("Degree:", profile[23])
        print("Years Attended:", profile[24])

    else:
        print("No profile found!")

