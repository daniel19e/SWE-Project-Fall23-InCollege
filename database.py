import sqlite3


def setupSQLite(databaseName):
  global connection, cursor
  connection = sqlite3.connect(databaseName)
  cursor = connection.cursor()

  cursor.execute('''CREATE TABLE IF NOT EXISTS college_students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, pass TEXT)''')
  connection.commit()

  return connection