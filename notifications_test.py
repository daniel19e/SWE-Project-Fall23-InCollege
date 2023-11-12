import pytest
from unittest.mock import Mock, MagicMock, ANY
from unittest.mock import patch
from  notifications import Notifications
from datetime import datetime, timedelta

@pytest.fixture
def mock_db(mocker):
    # Mock the get_student_who_joined_for_notification method
    mock = mocker.patch('database.DatabaseObject.get_student_who_joined_for_notification')
    mock.side_effect = [[('Felix', 'Kjellberg'), ('Nihat', 'Karimli')], []]
    return mock

def test_student_join_test(capsys, mock_db):
    instance_of_notification = Notifications("current_user", 1, mock_db)
    #If there is a new student registration, print accordingly (student info etc)
    instance_of_notification._Notifications__student_joined_notif()
    captured = capsys.readouterr()
    assert "----------------------------------" in captured.out
    assert "[Notification] - New students in InCollege:" in captured.out
    assert "----------------------------------" in captured.out
    assert "Student Felix Kjellberg has joined InCollege" not in captured.out
    assert "Student Nihat Karimli has joined InCollege" not in captured.out

    #if there is no need, simply print empty(null)
    instance_of_notification._Notifications__student_joined_notif()
    captured = capsys.readouterr()
    assert "" in captured.out

@pytest.fixture
def mock_db(mocker):
    # Mock the get_time_of_job_applications method
    mock = mocker.patch('database.DatabaseObject.get_time_of_job_applications')
    return mock

def is_inside_seven_days(date_time):
    return datetime.now() - date_time <= timedelta(days=7)

def test_job_graduation_notification(capsys, mock_db):
    instance_of_notification = Notifications("current_user", 1, mock_db)
    mock_db.side_effect = [[{"time_applied": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")}]]
    
    instance_of_notification._Notifications__not_applied_for_a_job_notif()
    captured = capsys.readouterr()
    #if the user already applied for a job within the time frame, no output needed
    assert "" in captured.out

    mock_db.side_effect = []

    instance_of_notification._Notifications__not_applied_for_a_job_notif()
    captured = capsys.readouterr()
    #else put the default output for the code
    assert "----------------------------------" in captured.out
    assert "[Notification] - Remember - you're going to want to have a job when you graduate." in captured.out
    assert "----------------------------------" in captured.out

def test_not_created_profile_notification(capsys, mock_db):
    notifications_instance = Notifications("current_user",1, mock_db)
    mock_db.profile_exists.return_value = False

    notifications_instance._Notifications__not_created_profile_notif()
    #simple test case that chedks the given output
    captured = capsys.readouterr()
    assert "----------------------------------" in captured.out
    assert "[Notification] - Don't forget to create a profile" in captured.out
    assert "----------------------------------" in captured.out

def test_new_job_posted_notification(capsys, mock_db):
    mock_notifications = [{"message": "A new job has been posted."}]

    mock_db.get_notifications.return_value = mock_notifications
    notifications_instance = Notifications("current_username", "current_user_id", mock_db)
    notifications_instance._Notifications__notifications_from_db()

    #expected output when a job is posted
    captured = capsys.readouterr()
    assert "----------------------------------" in captured.out
    assert "[Notification] - A new job has been posted." in captured.out
    assert "----------------------------------" in captured.out

    #ensures all notifications are indeed read after run
    mock_db.mark_all_notifications_as_read.assert_called_with("current_user_id")