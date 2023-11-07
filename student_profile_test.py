import pytest
from unittest.mock import Mock, MagicMock, patch, call
from student_profile import create_or_edit_profile, save_profile, display_profile
import database

mock_db = Mock()
mock_db.get_cursor = MagicMock()


def test_create_new_profile(monkeypatch, capsys):
    mock_input_values = iter(
        ['Test Title', 'Test Major', 'Test About', 'Test University', 'Test Degree', '2020-2021'])
    monkeypatch.setattr(
        'builtins.input', lambda _: next(mock_input_values, ''))

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None  # No existing profile

    mock_db = MagicMock()
    mock_db.get_cursor.return_value = mock_cursor

    create_or_edit_profile(mock_db, 'newuser')
    calls = mock_cursor.execute.call_args_list
    out, _ = capsys.readouterr()
    expected_call = call(
        'INSERT INTO student_profiles (username, title, major, about, university, degree, years_attended) VALUES (?, ?, ?, ?, ?, ?, ?)',
        ['newuser', 'Test Title', 'Test Major', 'Test About',
            'Test University', 'Test Degree', '2020-2021']
    )
    assert expected_call in calls, f"Expected call: {expected_call}\nActual calls: {calls}"
    assert "Profile updated successfully!" in out


def test_edit_saving_and_exiting(monkeypatch, capsys):
    mock_input_values = iter(
        ['New Title', 'exit', '', '', '', '', ''])  # Only change title
    monkeypatch.setattr(
        'builtins.input', lambda _: next(mock_input_values, ''))

    existing_profile_data = ('existinguser', 'Old Title', 'Old Major',
                             'Old About', 'Old University', 'Old Degree', '2019-2020')
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = existing_profile_data

    mock_db = MagicMock()
    mock_db.get_cursor.return_value = mock_cursor

    create_or_edit_profile(mock_db, 'existinguser')
    calls = mock_cursor.execute.call_args_list
    out, _ = capsys.readouterr()
    assert "Saving and exiting" in out


def test_edit_profile_updated_successfully(monkeypatch, capsys):
    mock_input_values = iter(
        ['New Title', '', '', '', '', '', ''])  # Only change title
    monkeypatch.setattr(
        'builtins.input', lambda _: next(mock_input_values, ''))
    existing_profile_data = ('existinguser', 'Old Title', 'Old Major',
                             'Old About', 'Old University', 'Old Degree', '2019-2020')
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = existing_profile_data
    mock_db = MagicMock()
    mock_db.get_cursor.return_value = mock_cursor
    create_or_edit_profile(mock_db, 'existinguser')
    out, _ = capsys.readouterr()
    assert "Profile updated successfully" in out


def test_exit_command_during_profile_creation(monkeypatch):
    mock_input_values = iter(['exit'])  # User exits immediately
    monkeypatch.setattr(
        'builtins.input', lambda _: next(mock_input_values, ''))

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None  # No existing profile

    mock_db = MagicMock()
    mock_db.get_cursor.return_value = mock_cursor

    create_or_edit_profile(mock_db, 'exitinguser')

    expected_call = call(
        'INSERT INTO student_profiles (username) VALUES (?)',
        ['exitinguser']
    )

    calls = mock_cursor.execute.call_args_list
    assert expected_call in calls, f"Expected call: {expected_call}\nActual calls: {calls}"

    assert len(calls) == 3, f"Expected 3 calls, got {len(calls)}: {calls}"


def test_display_profile(capsys):
    existing_profile_data = ('testuser', 'Existing Title', 'Existing Major',
                             'Existing About', 'Existing University', 'Existing Degree', '2020-2023')
    mock_description = [
        ('username',),
        ('title',),
        ('major',),
        ('about',),
        ('university',),
        ('degree',),
        ('years_attended',)
    ]
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = existing_profile_data
    mock_cursor.description = mock_description
    mock_db.get_cursor.return_value = mock_cursor

    with patch('builtins.input', side_effect=['A']):
        display_profile(mock_db, 'testuser')
        out, _ = capsys.readouterr()
        expected_output = [
            "\nProfile Details:",
            "Username: testuser",
            "Title: Existing Title",
            "Major: Existing Major",
            "About: Existing About",
            "University: Existing University",
            "Degree: Existing Degree",
            "Years attended: 2020-2023\n",
        ]
        assert out == "\n".join(expected_output)


def test_update_and_save_existing_profile_partial():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_db.get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = True

    profile_data = {'username': 'existinguser', 'title': 'New Title'}
    username = 'existinguser'

    save_profile(mock_db, profile_data, username)

    mock_cursor.execute.assert_called_with(
        "UPDATE student_profiles SET username = ?, title = ? WHERE username = ?",
        ['existinguser', 'New Title', 'existinguser']
    )


def test_insert_new_profile():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_db.get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    profile_data = {'username': 'newuser', 'title': 'New Title'}
    username = 'newuser'

    save_profile(mock_db, profile_data, username)

    mock_cursor.execute.assert_called_with(
        "INSERT INTO student_profiles (username, title) VALUES (?, ?)",
        ['newuser', 'New Title']
    )


def test_no_username(capsys):
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_db.get_cursor.return_value = mock_cursor

    profile_data = {'title': 'New Title'}  # 'username' key is missing
    username = 'someuser'

    save_profile(mock_db, profile_data, username)
    out, _ = capsys.readouterr()
    assert "No profile changes to save." in out
    mock_cursor.execute.assert_not_called()


def test_create_complete_profile(monkeypatch, capsys):
    mock_input_values = iter(
        [
            'Jason Profile', 'Computer Science', 'This is a test about section.', 'University of South Florida', 'Bachelor', '2020-2024',
            'Job title 1', 'Employer 1', '2001-01-01', '2001-01-01', 'Location 1', 'Description 1',
            'Job title 2', 'Employer 2', '2001-01-01', '2001-01-01', 'Location 2', 'Description 2',
            'Job title 3', 'Employer 3', '2001-01-01', '2001-01-01', 'Location 3', 'Description 3',
        ])
    
    monkeypatch.setattr(
        'builtins.input', lambda _: next(mock_input_values, ''))

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None

    mock_db = MagicMock()
    mock_db.get_cursor.return_value = mock_cursor

    create_or_edit_profile(mock_db, 'testuser')
    out, _ = capsys.readouterr()
    assert "Profile updated successfully!" in out

def test_display_complete_profile(capsys):
    existing_profile_data = (
        'testuser', 'Jason Profile', 'Computer Science', 'This is a test about section.', 'University of South Florida', 'Bachelor', '2020-2024',
            'Job title 1', 'Employer 1', '2001-01-01', '2001-01-01', 'Location 1', 'Description 1',
            'Job title 2', 'Employer 2', '2001-01-01', '2001-01-01', 'Location 2', 'Description 2',
            'Job title 3', 'Employer 3', '2001-01-01', '2001-01-01', 'Location 3', 'Description 3',
    )
    mock_description = [
        ('username',),
        ('title',),
        ('major',),
        ('about',),
        ('university',),
        ('degree',),
        ('years_attended',),
        ('title1',),
        ('employer1',),
        ('start1',),
        ('end1',),
        ('location1',),
        ('description1',),
        ('title2',),
        ('employer2',),
        ('start2',),
        ('end2',),
        ('location2',),
        ('description2',),
        ('title3',),
        ('employer3',),
        ('start3',),
        ('end3',),
        ('location3',),
        ('description3',),
    ]
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = existing_profile_data
    mock_cursor.description = mock_description
    mock_db.get_cursor.return_value = mock_cursor

    with patch('builtins.input', side_effect=['A']):
        display_profile(mock_db, 'testuser')
        out, _ = capsys.readouterr()
        expected_output = [
            "\nProfile Details:",
            "Username: testuser",
            "Title: Jason Profile",
            "Major: Computer Science",
            "About: This is a test about section.",
            "University: University of South Florida",
            "Degree: Bachelor",
            "Years attended: 2020-2024\n",
            "Experience 1:",
            "Title: Job title 1",
            "Employer: Employer 1",
            "Start: 2001-01-01",
            "End: 2001-01-01",
            "Location: Location 1",
            "Description: Description 1\n",
            "Experience 2:",
            "Title: Job title 2",
            "Employer: Employer 2",
            "Start: 2001-01-01",
            "End: 2001-01-01",
            "Location: Location 2",
            "Description: Description 2\n",
            "Experience 3:",
            "Title: Job title 3",
            "Employer: Employer 3",
            "Start: 2001-01-01",
            "End: 2001-01-01",
            "Location: Location 3",
            "Description: Description 3\n",
        ]
        assert out == "\n".join(expected_output)


@patch('pages.input', side_effect=['John', 'Doe', 'johndoe', 'password123', 'Computer Science', 'University', 'n'])
@patch('pages.print')
def test_plus_membership_offer_message(mock_print, mock_input):
    # You would replace 'your_module' with the actual name of the module where sign_up_page is defined.
    from pages import sign_up_page
    
    # Call the sign_up_page function, which should now use the mocked input to simulate user input.
    sign_up_page()

    # Check if the specific message was printed.
    mock_print.assert_any_call("\n* InCollege now offers a Plus Membership! Plus members get access to a variety of exclusive features for only $10/month. *")