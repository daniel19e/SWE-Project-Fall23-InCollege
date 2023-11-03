import sqlite3


class DatabaseObject:
    def __init__(self, databaseName):
        self.connection = sqlite3.connect(databaseName)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS college_students (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, firstname TEXT, lastname TEXT, pass TEXT, major TEXT, university TEXT, language TEXT CHECK(language IN ('english', 'spanish')) default 'english', receive_emails BOOL default 1, receive_sms BOOL default 1, targeted_ads BOOL default 1)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS connections (user1 TEXT, user2 TEXT, PRIMARY KEY(user1, user2))")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS pending_connections (requester TEXT, requestee TEXT, PRIMARY KEY(requester, requestee))")
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS job_posts (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, title TEXT, description TEXT, employer TEXT, location TEXT, salary TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS job_applications (id INTEGER PRIMARY KEY AUTOINCREMENT, job_id INTEGER, student_id TEXT, graduation_date TEXT, start_date TEXT, student_application TEXT, FOREIGN KEY (job_id) REFERENCES job_posts(id) ON DELETE SET NULL)''')
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS job_saved (job_id INTEGER, student_id TEXT, FOREIGN KEY (job_id) REFERENCES job_posts(id) ON DELETE SET NULL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS student_profiles (username TEXT PRIMARY KEY, title TEXT, major TEXT, about TEXT, title1 TEXT, employer1 TEXT, start1 TEXT, end1 TEXT, location1 TEXT, description1 TEXT, title2 TEXT, employer2 TEXT, start2 TEXT, end2 TEXT, location2 TEXT, description2 TEXT, title3 TEXT, employer3 TEXT, start3 TEXT, end3 TEXT, location3 TEXT, description3 TEXT, university TEXT, degree TEXT, years_attended TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender INTEGER, receiver INTEGER, message TEXT, time DATETIME DEFAULT CURRENT_TIMESTAMP, read INTEGER, FOREIGN KEY (sender) REFERENCES college_students(id), FOREIGN KEY (receiver) REFERENCES college_students(id))''')
        self.connection.commit()

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor

    def search_first_and_last(self, firstname, lastname):
        self.cursor.execute("SELECT * FROM college_students WHERE firstname = ? AND lastname = ?",
                            (firstname, lastname))
        return self.cursor.fetchone()

    def search_students_by_criteria(self, lastname=None, university=None, major=None):
        criteria = []
        query = "SELECT * FROM college_students WHERE "

        if lastname:
            query += "lastname = ? AND "
            criteria.append(lastname.lower())

        if university:
            query += "university = ? AND "
            criteria.append(university.lower())

        if major:
            query += "major = ? AND "
            criteria.append(major.lower())

        query = query[:-4]

        self.cursor.execute(query, tuple(criteria))
        return self.cursor.fetchall()

    def add_connection(self, user1, user2):
        try:
            self.cursor.execute(
                "INSERT INTO connections (user1, user2) VALUES (?, ?)", (user1, user2))
            self.cursor.execute(
                "INSERT INTO connections (user1, user2) VALUES (?, ?)", (user2, user1))
            self.connection.commit()
        except:
            print("An error occured, please try again.")

    def remove_connection(self, user1, user2):
        self.cursor.execute(
            "DELETE FROM connections WHERE user1 = ? AND user2 = ?", (user1, user2))
        self.cursor.execute(
            "DELETE FROM connections WHERE user1 = ? AND user2 = ?", (user2, user1))
        self.connection.commit()

    def get_connections(self, username):
        self.cursor.execute(
            "SELECT user2 FROM connections WHERE user1 = ?", (username,))
        return [item[0] for item in self.cursor.fetchall()]

    def send_friend_request(self, requester, requestee):
        self.cursor.execute(
            "INSERT INTO pending_connections (requester, requestee) VALUES (?, ?)", (requester, requestee))
        self.connection.commit()

    def get_pending_requests(self, username):
        self.cursor.execute(
            "SELECT requester FROM pending_connections WHERE requestee = ?", (username,))
        return self.cursor.fetchall()

    def get_full_pending_requests(self, username):
        self.cursor.execute(
            "SELECT * FROM pending_connections WHERE requestee = ?", (username,))
        return self.cursor.fetchall()

    def accept_friend_request(self, requester, requestee):
        self.add_connection(requester, requestee)
        self.remove_pending_request(requester, requestee)

    def reject_friend_request(self, requester, requestee):
        self.remove_pending_request(requester, requestee)

    def remove_pending_request(self, requester, requestee):
        self.cursor.execute(
            "DELETE FROM pending_connections WHERE requester = ? AND requestee = ?", (requester, requestee))
        self.connection.commit()

    def get_user_info(self, username):
        self.cursor.execute("SELECT * FROM college_students WHERE username = ?",
                            (username,))
        return self.cursor.fetchone()

    def get_number_of_accounts(self):
        self.cursor.execute("SELECT COUNT(*) FROM college_students")
        return self.cursor.fetchone()[0]

    def get_number_of_jobs(self):
        self.cursor.execute("SELECT COUNT(*) FROM job_posts")
        return self.cursor.fetchone()[0]

    def already_applied(self, student_id, job_id):
        self.cursor.execute(
            '''SELECT COUNT(*) FROM job_applications WHERE student_id = ? AND job_id = ?''', (student_id, job_id))
        return self.cursor.fetchone()[0] > 0

    def add_applications(self, application):
        self.cursor.execute('''INSERT INTO job_applications (job_id, student_id, graduation_date, start_date, student_application) VALUES (?, ?, ?, ?, ?)''', (
            application['job_id'], application['student_id'], application['graduation_date'], application['start_date'], application['student_application']))
        self.connection.commit()

    def get_applications_of_student(self, student_id):
        self.cursor.execute(
            "SELECT job_id FROM job_applications WHERE student_id = ?", (student_id,))
        return [job[0] for job in self.cursor.fetchall()]

    def remove_application(self, job_id, student_id):
        self.cursor.execute(
            "DELETE FROM job_applications WHERE job_id = ? AND student_id = ?", (job_id, student_id,))
        self.connection.commit()

    def add_new_student(self, username, firstname, lastname, password, major, university):
        self.cursor.execute(
            "INSERT INTO college_students (username, firstname, lastname, pass, major, university) VALUES (? , ?, ?, ?, ?, ?)",
            (username.lower(), firstname.lower(), lastname.lower(), password, major.lower(), university.lower()))
        self.connection.commit()

    def get_jobs(self):
        self.cursor.execute("SELECT * FROM job_posts")
        return self.cursor.fetchall()

    def get_job_by_id(self, job_id):
        self.cursor.execute("SELECT * FROM job_posts WHERE id = ?", (job_id,))
        return self.cursor.fetchone()

    def add_new_job_post(self, firstname, lastname, title, description, employer, location, salary):
        self.cursor.execute(
            "INSERT INTO job_posts (firstname, lastname, title, description, employer, location, salary) VALUES (? , ?, ?, ?, ? , ?, ?)",
            (firstname.lower(), lastname.lower(), title.lower(), description.lower(), employer.lower(), location.lower(), salary.lower()))
        self.connection.commit()

    def remove_job_post(self, job_id):
        self.cursor.execute("DELETE FROM job_posts WHERE id = ?", (job_id,))
        self.connection.commit()

    def add_saved_job(self, job_id, student_id):
        self.cursor.execute(
            '''INSERT INTO job_saved (job_id, student_id) VALUES (?, ?)''', (job_id, student_id))
        self.connection.commit()

    def get_saved_jobs(self, student_id):
        self.cursor.execute(
            "SELECT job_id FROM job_saved WHERE student_id = ?", (student_id,))
        return [job[0] for job in self.cursor.fetchall()]

    def remove_saved_job(self, job_id, student_id):
        self.cursor.execute(
            "DELETE FROM job_saved WHERE job_id = ? AND student_id = ?", (job_id, student_id))
        self.connection.commit()

    def is_student_registered(self, username, password):
        self.cursor.execute("SELECT * FROM college_students WHERE username = ? AND pass = ?",
                            (username.lower(), password))
        return self.cursor.fetchone()

    def profile_exists(self, username):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM student_profiles WHERE username = ?", (username,))
        return bool(cursor.fetchone())

    def close_connection(self):
        self.connection.close()

    def send_message(self, sender_id, receiver_id, message):
        self.cursor.execute(
            "INSERT INTO messages (sender, receiver, message, read) VALUES (?, ?, ?, ?)", (sender_id, receiver_id, message, 0))
        self.connection.commit()

    def generate_message_list(self, receiver_id):
        self.cursor.execute(
            "SELECT * FROM messages WHERE receiver = ? ORDER BY time DESC", (receiver_id,))
        messages = self.cursor.fetchall()
        self.cursor.execute("UPDATE messages SET read = ?", (1,))
        self.connection.commit()
        return messages

    def get_unread_messages(self, receiver_id):
        self.cursor.execute("SELECT * FROM messages WHERE read = ? AND receiver = ?", (0, receiver_id))
        return self.cursor.fetchall()

    def get_user_by_id(self, user_id):
        self.cursor.execute(
            "SELECT username FROM college_students WHERE id = ?", (user_id,))
        return self.cursor.fetchone()['username']


db = DatabaseObject("incollege_database.db")


def get_existing_db_object():
    return db


def setupSQLite(databaseName):
    global connection, cursor
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS college_students (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, firstname TEXT, lastname TEXT, pass TEXT, major TEXT, university TEXT, language TEXT CHECK(language IN ('english', 'spanish')) default 'english', receive_emails BOOL default 1, receive_sms BOOL default 1, targeted_ads BOOL default 1)")
    connection.commit()
    return connection
