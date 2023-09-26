import sqlite3

class DatabaseObject:
  def __init__(self, databaseName):
    self.connection = sqlite3.connect(databaseName)
    self.cursor = self.connection.cursor()
    self.cursor.execute('''CREATE TABLE IF NOT EXISTS college_students (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, firstname TEXT, lastname TEXT, pass TEXT)''')
    self.cursor.execute('''CREATE TABLE IF NOT EXISTS job_posts (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, title TEXT, description TEXT, employer TEXT, location TEXT, salary TEXT)''')
    self.connection.commit()

  def get_connection(self):
    return self.connection
  
  def get_cursor(self):
    return self.cursor
  
  def search_first_and_last(self, firstname, lastname):
    self.cursor.execute("SELECT * FROM college_students WHERE firstname = ? AND lastname = ?",
                    (firstname, lastname))
    return self.cursor.fetchone()
  
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
  
  def add_new_student(self, username, firstname, lastname, password):
    self.cursor.execute(
      "INSERT INTO college_students (username, firstname, lastname, pass) VALUES (? , ?, ?, ?)",
      (username.lower(), firstname.lower(), lastname.lower(), password))
    self.connection.commit()

  def add_new_job_post(self, firstname, lastname, title, description, employer, location, salary):
    self.cursor.execute(
      "INSERT INTO job_posts (firstname, lastname, title, description, employer, location, salary) VALUES (? , ?, ?, ?, ? , ?, ?)",
      (firstname.lower(), lastname.lower(), title.lower(), description.lower(), employer.lower(), location.lower(), salary.lower()))
    self.connection.commit()
    
  def is_student_registered(self, username, password):
    self.cursor.execute("SELECT * FROM college_students WHERE username = ? AND pass = ?",
                 (username.lower(), password))
    return self.cursor.fetchone()
  
  def close_connection(self):
    self.connection.close()

    
  
  
db = DatabaseObject("incollege_database.db")
def get_existing_db_object():
  return db

def setupSQLite(databaseName):
  global connection, cursor
  connection = sqlite3.connect(databaseName)
  cursor = connection.cursor()

  cursor.execute('''CREATE TABLE IF NOT EXISTS college_students (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, firstname TEXT, lastname TEXT, pass TEXT)''')
  connection.commit()

  return connection