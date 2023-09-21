import sqlite3

class DatabaseObject:
  def __init__(self, databaseName):
    self.connection = sqlite3.connect(databaseName)
    self.cursor = self.connection.cursor()
    self.cursor.execute('''CREATE TABLE IF NOT EXISTS college_students (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, firstname TEXT, lastname TEXT, pass TEXT)''')
    self.connection.commit()

  def get_connection(self):
    return self.connection
  
  def get_cursor(self):
    return self.cursor
  
  def search_first_and_last(self, firstname, lastname):
    self.cursor.execute("SELECT * FROM college_students WHERE firstname = ? AND lastname = ?",
                    (firstname, lastname))
    return self.cursor.fetchone()
  
  def get_number_of_accounts(self):
    self.cursor.execute("SELECT COUNT(*) FROM college_students")
    return self.cursor.fetchone()[0]
  
  def add_new_student(self, username, firstname, lastname, password):
    self.cursor.execute(
      "INSERT INTO college_students (username, firstname, lastname, pass) VALUES (? , ?, ?, ?)",
      (username.lower(), firstname.lower(), lastname.lower(), password))
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