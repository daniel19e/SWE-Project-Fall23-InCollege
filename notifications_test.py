import pytest
from unittest.mock import Mock, MagicMock, ANY
from unittest.mock import patch, call
from  notifications import Notifications
from datetime import datetime, timedelta
import database

db = database.DatabaseObject(":memory:")

# NEW TESTS ----------------------------------------------------------------------------------------------------------------------------------------------------

def test_student_join_test(capsys):
    #If there is a new student registration, print accordingly (student info etc)
    with patch('database.DatabaseObject.get_student_who_joined_for_notification', return_value=[('Felix', 'Kjellberg'), ('Nihat', 'Karimli')]):
        instance_of_notification = Notifications("current_user", 1, db)
        instance_of_notification._Notifications__student_joined_notif()
        captured = capsys.readouterr()
        assert "[Notification] - New students in InCollege:" in captured.out
        assert "Student Felix Kjellberg has joined InCollege" in captured.out
        assert "Student Nihat Karimli has joined InCollege" in captured.out

    #if there is no need, simply print empty(null)
    with patch('database.DatabaseObject.get_student_who_joined_for_notification', return_value=[]):
        instance_of_notification = Notifications("current_user", 1, db)
        instance_of_notification._Notifications__student_joined_notif()
        captured = capsys.readouterr()
        assert (captured.out == "")

def test_job_graduation_notification(capsys):
    #if the user already applied for a job within the time frame, no output needed
    with patch('database.DatabaseObject.get_time_of_job_applications', return_value=[{"time_applied": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")}]):
        instance_of_notification = Notifications("current_user", 1, db)
        instance_of_notification._Notifications__not_applied_for_a_job_notif()
        captured = capsys.readouterr()
        assert (captured.out == "")

    #if the user already has not applied for a job within the time frame
    with patch('database.DatabaseObject.get_time_of_job_applications', return_value=[{"time_applied": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")}]):
        instance_of_notification = Notifications("current_user", 1, db)
        instance_of_notification._Notifications__not_applied_for_a_job_notif()
        captured = capsys.readouterr()
        assert "[Notification] - Remember - you're going to want to have a job when you graduate" in captured.out

def test_not_created_profile_notification(capsys):
    #simple test case that chedks the given output
    with patch('database.DatabaseObject.profile_exists', return_value=False):
        instance_of_notification = Notifications("current_user", 1, db)
        instance_of_notification._Notifications__not_created_profile_notif()
        captured = capsys.readouterr()
        assert "[Notification] - Don't forget to create a profile" in captured.out

def test_new_job_posted_notification(capsys):
    #expected output when a job is posted
    with patch('database.DatabaseObject.get_notifications', return_value=[{"message": "A new job has been posted."}]):
        instance_of_notification = Notifications("current_user", 1, db)
        instance_of_notification._Notifications__notifications_from_db()
        captured = capsys.readouterr()
        assert "[Notification] - A new job has been posted" in captured.out

def test_pending_requests_notification(capsys):
    with patch('database.DatabaseObject.get_pending_requests', return_value=[1, 2, 3]):
        instance_of_notification = Notifications("current_user", 1, db)
        instance_of_notification._Notifications__pending_requests_notif()
        captured = capsys.readouterr()
        assert "[Notification] - You have 3 pending friend request(s). Go to the 'Friend Requests' tab to accept/reject" in captured.out

def test_unread_messages_notification(capsys):
    with patch('database.DatabaseObject.get_unread_messages', return_value=[1, 2, 3]):
        instance_of_notification = Notifications("current_user", 1, db)
        instance_of_notification._Notifications__unread_messages_notif()
        captured = capsys.readouterr()
        assert "[Notification] - You have 3 unread message(s). Go to the 'Messages' tab." in captured.out