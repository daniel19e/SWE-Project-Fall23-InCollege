import pytest
import home
import database
from unittest.mock import Mock
from unittest.mock import patch

db = database.DatabaseObject(":memory:")

#Cleanup function
def clear_mock_db():
  db.get_cursor().execute("DELETE FROM college_students")
  db.get_cursor().execute("DELETE FROM job_posts")

clear_mock_db()

def populate_mock_db(username, firstname, lastname, password):
  db.add_new_student(username, firstname, lastname, password)

def test_add_one_job_to_db():
    clear_mock_db()
    db.add_new_job_post("Test", "test", "Title", "Description", "Employer", "Location", "50000")
    assert db.get_number_of_jobs() == 1
    clear_mock_db()

def test_post_one_job(capsys):
    clear_mock_db()
    populate_mock_db("testuser1", "Test", "User", "Test123*")
    with patch("builtins.input", side_effect=["Test Job Title", "Test Job Description", "Test Employer", "Test Location", "50000", "0"]):
        home.try_posting_job(db, ["test_user1", "Test", "User", "Test123*"])
        out, err = capsys.readouterr()
        assert db.get_number_of_jobs() == 1


def test_post_jobs_over_limit(capsys):
    # Try posting more than 5 jobs
    output = ""
    for i in range(6):
        with patch("builtins.input", side_effect=["Test Job Title", "Test Job Description", "Test Employer", "Test Location", "50000", "0"]):
            home.try_posting_job(db, ["test_user1", "Test", "User", "Test123*"])
            out, err = capsys.readouterr()
            output += out

    
    # Check if the maximum job posts limit is enforced
    assert db.get_number_of_jobs() == 5
    assert "Error: Maximum job posts limit reached." in output
    clear_mock_db()
