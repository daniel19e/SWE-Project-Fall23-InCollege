import pytest
from jobs import (
    try_posting_job,
    view_jobs_interns,
    my_job_postings,
    try_deleting_job,
    display_applied_jobs,
    try_deleting_job,
    handle_job_deletion,
    display_saved_jobs,
    handle_application_count
)
import database
from unittest.mock import Mock
from unittest.mock import patch, call

db = database.DatabaseObject(":memory:")


# Cleanup function
def clear_mock_db():
    db.get_cursor().execute("DELETE FROM college_students")
    db.get_cursor().execute("DELETE FROM job_posts")


clear_mock_db()


def populate_mock_db(username, firstname, lastname, password):
    db.add_new_student(username, firstname, lastname, password, "testmajor", "testuniv")


def test_add_one_job_to_db():
    clear_mock_db()
    db.add_new_job_post(
        "Test", "test", "Title", "Description", "Employer", "Location", "50000", 1
    )
    assert db.get_number_of_jobs() == 1
    clear_mock_db()


def test_post_one_job(capsys):
    clear_mock_db()
    populate_mock_db("testuser1", "Test", "User", "Test123*")
    with patch(
        "builtins.input",
        side_effect=[
            "Test Job Title",
            "Test Job Description",
            "Test Employer",
            "Test Location",
            "50000",
            "0",
        ],
    ):
        try_posting_job(db, ["test_user1", "Test", "User", "Test123*"])
        out, err = capsys.readouterr()
        assert db.get_number_of_jobs() == 1


def test_try_deleting_another_users_job(capsys):
    clear_mock_db()
    populate_mock_db("testuser1", "Test", "User", "Test123*")
    populate_mock_db("testuser2", "Another", "User", "Test123*")
    db.add_new_job_post(
        "Another", "User", "Title", "Description", "Employer", "Location", "50000", 1
    )
    with patch("builtins.input", side_effect=["1"]):
        try_deleting_job(["testuser1", "Test", "User", "Test123*"])
        out, err = capsys.readouterr()
        assert "Error: Invalid input and/or incorrect job ID.\n" in out
        assert db.get_number_of_jobs() == 1


def test_try_deleting_invalid_job(capsys):
    clear_mock_db()
    populate_mock_db("testuser1", "Test", "User", "Test123*")
    with patch("builtins.input", side_effect=["99"]):
        try_deleting_job(["testuser1", "Test", "User", "Test123*"])
        out, err = capsys.readouterr()
        assert "Error: Invalid input and/or incorrect job ID.\n" in out
        assert db.get_number_of_jobs() == 0


def test_view_jobs_interns(capsys):
    clear_mock_db()
    populate_mock_db("testuser1", "Test", "User", "Test123*")
    user_info = {"id": 1, "firstname": "Test", "lastname": "User"}
    with patch("builtins.input", side_effect=["0"]):
        view_jobs_interns(user_info)
        out, err = capsys.readouterr()
        assert "List of all Jobs/Interns:" in out


@patch("jobs.db.get_job_by_id")
@patch("jobs.db.already_applied")
@patch("jobs.db.add_applications")
def test_apply_jobs_interns(
    mock_add_applications, mock_already_applied, mock_get_job_by_id, capsys
):
    mock_get_job_by_id.return_value = {
        "firstname": "TestEmployer",
        "lastname": "EmployerLastname",
        "id": 1,
    }
    mock_already_applied.return_value = False
    mock_add_applications.return_value = None

    student_info = {"id": 1, "firstname": "TestStudent", "lastname": "StudentLastname"}
    job_id = 1

    with patch(
        "builtins.input",
        side_effect=["01/01/2025", "01/01/2023", "I'm a good fit for the job."],
    ):
        from jobs import apply_jobs_interns

        apply_jobs_interns(student_info, job_id)

    out, err = capsys.readouterr()

    assert "Application submitted successfully!" in out
    mock_add_applications.assert_called_once()


def test_my_job_postings(capsys):
    clear_mock_db()
    populate_mock_db("testuser1", "Test", "User", "Test123*")
    user_info = {"id": 1, "firstname": "Test", "lastname": "User"}
    with patch("builtins.input", side_effect=["0"]):
        my_job_postings(user_info)
        out, err = capsys.readouterr()
        assert "============= My Job Postings ============" in out


# You can define a mock user_info for our tests.
mock_user_info = {"id": "1", "firstname": "John", "lastname": "Doe"}


def test_display_applied_jobs(capsys):
    with patch(
        "database.DatabaseObject.get_jobs",
        return_value=[{"id": 1, "title": "Test Job"}],
    ), patch(
        "database.DatabaseObject.get_applications_of_student", return_value=[1]
    ), patch(
        "builtins.input", return_value="0"
    ):
        display_applied_jobs(mock_user_info)
        out, err = capsys.readouterr()
        assert "Jobs/Interns You Have Applied For:" in out
        assert "Job ID: 1, Job Title: Test Job" in out


def test_handle_job_deletion(capsys):
    with patch("database.DatabaseObject.get_jobs", return_value=[]), patch(
        "database.DatabaseObject.get_applications_of_student", return_value=[1]
    ), patch("database.DatabaseObject.get_saved_jobs", return_value=[]):
        handle_job_deletion(mock_user_info)
        out, err = capsys.readouterr()
        assert (
            "[Notification] - One or more jobs you have applied for or saved, have been deleted."
            in out
        )
        assert "Job ID #1" in out


def test_display_saved_jobs(capsys):
    with patch(
        "database.DatabaseObject.get_jobs",
        return_value=[{"id": 1, "title": "Test Job"}],
    ), patch("database.DatabaseObject.get_saved_jobs", return_value=[1]), patch(
        "builtins.input", return_value="0"
    ):
        display_saved_jobs(mock_user_info)
        out, err = capsys.readouterr()
        assert "Saved Jobs/Interns:" in out
        assert "Job ID: 1, Job Title: Test Job" in out


def test_try_deleting_job(capsys):
    with patch("builtins.input", return_value="X"):
        try_deleting_job(mock_user_info)
        out, err = capsys.readouterr()
        assert "Job deleted sucessfully!" not in out

    with patch("builtins.input", return_value="1"), patch(
        "database.DatabaseObject.get_jobs",
        return_value=[
            {"id": 1, "title": "Test Job", "firstname": "John", "lastname": "Doe"}
        ],
    ):
        try_deleting_job(mock_user_info)
        out, err = capsys.readouterr()
        assert "Job deleted sucessfully!" in out

def test_post_jobs_over_limit(capsys):
    output = ""
    for i in range(11):
        with patch(
            "builtins.input",
            side_effect=[
                "Test Job Title",
                "Test Job Description",
                "Test Employer",
                "Test Location",
                "50000",
                "0",
            ],
        ):
            try_posting_job(db, ["test_user1", "Test", "User", "Test123*"])
            out, err = capsys.readouterr()
            output += out

    # Check if the maximum job posts limit is enforced
    assert db.get_number_of_jobs() == 10
    assert "Error: Maximum job posts limit reached." in output
    clear_mock_db()


@patch("jobs.db.get_job_by_id")
@patch("jobs.db.already_applied")
@patch("jobs.db.add_applications")
def test_apply_for_job(
    mock_add_applications, mock_already_applied, mock_get_job_by_id, capsys
):
    mock_get_job_by_id.return_value = {
        "firstname": "TestEmployer",
        "lastname": "EmployerLastname",
        "id": 1,
    }
    mock_already_applied.return_value = False
    mock_add_applications.return_value = None

    student_info = {"id": 1, "firstname": "TestStudent", "lastname": "StudentLastname"}
    job_id = 1

    with patch(
        "builtins.input",
        side_effect=["01/01/2025", "01/01/2023", "I'm a good fit for the job."],
    ):
        from jobs import apply_jobs_interns

        apply_jobs_interns(student_info, job_id)

    out, err = capsys.readouterr()

    assert "Application submitted successfully!" in out
    mock_add_applications.assert_called_once()


def test_display_applied_and_not_applied(capsys):
    with patch(
        "database.DatabaseObject.get_jobs",
        return_value=[
            {"id": 1, "title": "Test Job", "firstname": "Not joe"},
            {"id": 2, "title": "Test Job", "firstname": "Not joe"},
        ],
    ), patch(
        "database.DatabaseObject.get_applications_of_student", return_value=[1]
    ), patch(
        "builtins.input", return_value="0"
    ):
        view_jobs_interns(mock_user_info)
        out, err = capsys.readouterr()
        assert "Job ID: 1" in out
        assert "Status: APPLIED!" in out
        assert "Job ID: 2" in out
        assert "Status: Available." in out


def test_display_specific_job_details(capsys):
    with patch(
        "database.DatabaseObject.get_jobs",
        return_value=[
            {
                "id": 1,
                "title": "Test Job",
                "firstname": "Not joe",
                "description": "Test description",
                "employer": "Employer Name",
                "location": "Florida",
                "salary": "$100,000",
            },
            {
                "id": 2,
                "title": "Test Job",
                "firstname": "Not joe",
                "description": "Test description",
                "employer": "Employer Name",
                "location": "Florida",
                "salary": "$100,000",
            },
        ],
    ), patch(
        "database.DatabaseObject.get_applications_of_student", return_value=[1]
    ), patch(
        "builtins.input"
    ) as mock_input:
        mock_input.side_effect = ["1", "0"]
        view_jobs_interns(mock_user_info)
        out, err = capsys.readouterr()
        assert "Job ID: 1" in out
        assert "Title: Test Job" in out
        assert "Description: Test description" in out
        assert "Employer: Employer Name" in out
        assert "Location: Florida" in out
        assert "Salary: $100,000" in out


db = database.DatabaseObject(":memory:")


# Cleanup function
def clear_mock_db():
    db.get_cursor().execute("DELETE FROM college_students")
    db.get_cursor().execute("DELETE FROM job_posts")


clear_mock_db()


def populate_mock_db(username, firstname, lastname, password):
    db.add_new_student(username, firstname, lastname, password, "testmajor", "testuniv")


def test_add_one_job_to_db():
    clear_mock_db()
    db.add_new_job_post(
        "Test", "test", "Title", "Description", "Employer", "Location", "50000", 1
    )
    assert db.get_number_of_jobs() == 1
    clear_mock_db()


def test_post_one_job(capsys):
    clear_mock_db()
    populate_mock_db("testuser1", "Test", "User", "Test123*")
    with patch(
        "builtins.input",
        side_effect=[
            "Test Job Title",
            "Test Job Description",
            "Test Employer",
            "Test Location",
            "50000",
            "0",
        ],
    ):
        try_posting_job(db, ["test_user1", "Test", "User", "Test123*"])
        out, err = capsys.readouterr()
        assert db.get_number_of_jobs() == 1


def test_post_jobs_over_limit(capsys):
    # Try posting more than 10 jobs
    output = ""
    for i in range(11):
        with patch(
            "builtins.input",
            side_effect=[
                "Test Job Title",
                "Test Job Description",
                "Test Employer",
                "Test Location",
                "50000",
                "0",
            ],
        ):
            try_posting_job(db, ["test_user1", "Test", "User", "Test123*"])
            out, err = capsys.readouterr()
            output += out

    # Check if the maximum job posts limit is enforced
    assert db.get_number_of_jobs() == 10
    assert "Error: Maximum job posts limit reached." in output
    clear_mock_db()

# NEW TESTS ----------------------------------------------------------------------------------------------------------------------------------------------------

def test_job_deleted_notification(capsys):
    clear_mock_db()
    populate_mock_db("testuser1", "Test", "User", "Test123*")
    user_info = {"id": 1, "firstname": "Test", "lastname": "User"}
    with patch('database.DatabaseObject.get_applications_of_student',return_value=[1]):
        handle_job_deletion(user_info)
        out, err = capsys.readouterr()
        assert " One or more jobs you have applied for or saved, have been deleted." in out
    clear_mock_db()

def test_aplied_jobs_notification(capsys):
    clear_mock_db()
    populate_mock_db("testuser1", "Test", "User", "Test123*")
    user_info = {"id": 1, "firstname": "Test", "lastname": "User"}
    with patch('database.DatabaseObject.get_applications_of_student',return_value=[1, 2, 3, 4, 5]):
        handle_application_count(user_info)
        out, err = capsys.readouterr()
        assert "You have applied for 5 job(s)." in out
    clear_mock_db()