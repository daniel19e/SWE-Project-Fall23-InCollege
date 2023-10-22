import pytest
from unittest.mock import Mock, MagicMock, patch, call
from student_profile import create_or_edit_profile, save_profile, display_profile

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
