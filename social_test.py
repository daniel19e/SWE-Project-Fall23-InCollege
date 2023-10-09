import pytest
from unittest.mock import Mock
from unittest.mock import patch
import social
from social import connect_with_student


@pytest.fixture
def mock_db():
    return Mock(search_first_and_last=Mock(return_value=True))
# test case for checking wheteher the code takes firstname and lastname for input


@pytest.fixture
def mock_input(monkeypatch):
    mock = Mock(side_effect=["Abdulla", "Majidov"])
    monkeypatch.setattr("builtins.input", mock)
    return mock

# supposed reaction if the name is a member of InCollege


def test_promote_marketing_program_member(mock_db, mock_input, capsys):
    with patch.object(social, "db", mock_db):
        social.promote_marketing_program()
    captured = capsys.readouterr()
    assert "You are a part of the InCollege system.\n" in captured.out

# supposed reaction if the name is not a member of InCollege


def test_promote_marketing_program_non_member(mock_db, mock_input, capsys):
    mock_db.search_first_and_last.return_value = False
    with patch.object(social, "db", mock_db):
        social.promote_marketing_program()
    captured = capsys.readouterr()
    assert "You are not a part of the InCollege system yet.\n" in captured.out


@patch('social.db.search_first_and_last')
@patch('social.send_connection_request')
# Connection with student test
def test_connect_with_student_found(mock_send_connection_request, mock_search_first_and_last):
    mock_search_first_and_last.return_value = True

    result = connect_with_student('John', 'Doe')

    assert result == True

    mock_send_connection_request.assert_called_once_with('John', 'Doe')
# Connection with student test(if the student is not found)


@patch('social.db.search_first_and_last')
def test_connect_with_student_not_found(mock_search_first_and_last):
    mock_search_first_and_last.return_value = False
    result = connect_with_student('Jane', 'Doe')
    assert result == False


# (NEW TESTS) -------------------------
@patch('social.db.search_students_by_criteria')
def test_find_someone_i_know_lastname(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = [(
        1, 'testusername', 'testfirst', 'testlast', 'pass', 'major', 'univ', 'english', 1, 1, 1)]
    with patch('builtins.input') as mock_input:
        mock_input.side_effect = ['1', '0', '0']
        social.find_someone_i_know('testuser1')
        out, _ = capsys.readouterr()
        assert "testfirst testlast - testusername" in out
        assert "Select a student to send a connection" in out


@patch('social.db.search_students_by_criteria')
def test_find_someone_i_know_university(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = [(
        1, 'testusername', 'testfirst', 'testlast', 'pass', 'major', 'univ', 'english', 1, 1, 1)]
    with patch('builtins.input') as mock_input:
        mock_input.side_effect = ['2', '0', '0']
        social.find_someone_i_know('testuser1')
        out, _ = capsys.readouterr()
        assert "testfirst testlast - testusername" in out
        assert "Select a student to send a connection" in out


@patch('social.db.search_students_by_criteria')
def test_find_someone_i_know_major(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = [(
        1, 'testusername', 'testfirst', 'testlast', 'pass', 'major', 'univ', 'english', 1, 1, 1)]
    with patch('builtins.input') as mock_input:
        mock_input.side_effect = ['3', '0', '0']
        social.find_someone_i_know('testuser1')
        out, _ = capsys.readouterr()
        assert "testfirst testlast - testusername" in out
        assert "Select a student to send a connection" in out


@patch('social.db.search_students_by_criteria')
def test_find_someone_i_know_invalid(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = [(
        1, 'testusername', 'testfirst', 'testlast', 'pass', 'major', 'univ', 'english', 1, 1, 1)]
    with patch('builtins.input') as mock_input:
        mock_input.side_effect = ['5', '0', '0']
        social.find_someone_i_know('testuser1')
        out, _ = capsys.readouterr()
        assert "Invalid choice" in out


@patch('social.db.search_students_by_criteria')
def test_find_someone_i_know_no_results(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = []
    with patch('builtins.input') as mock_input:
        mock_input.side_effect = ['1', '0', '0']
        social.find_someone_i_know('testuser1')
        out, _ = capsys.readouterr()
        assert "No students found with the provided criteria" in out


@patch('social.db.search_students_by_criteria')
def test_find_someone_i_know_send_connection(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = [
        (1, 'testusername', 'testfirst', 'testlast', 'pass', 'major', 'univ', 'english', 1, 1, 1)]
    with patch('social.db.send_friend_request'), patch('builtins.input') as mock_input:
        mock_input.side_effect = ['1', '0', '1']
        social.find_someone_i_know('testuser1')
        out, _ = capsys.readouterr()
        assert "Connection request sent!" in out


def test_show_my_network_go_back(capsys):
    with patch('builtins.input') as mock_input, \
            patch('social.db.get_pending_requests', return_value=[]), \
            patch('social.db.get_connections', return_value=[]):
        mock_input.side_effect = ['0']
        social.show_my_network('testusername')
        out, _ = capsys.readouterr()
        assert out == "Your Network:\n\n\nMake your selection:\n1. Disconnect from someone\n0. Go back\n"


def test_show_my_network_show_pending_requests_and_connections(capsys):
    with patch('builtins.input') as mock_input, \
            patch('social.db.get_pending_requests', return_value=[['pending1'], ['pending2'], ['pending3']]), \
            patch('social.db.get_connections', return_value=['connection1', 'connection2', 'connection3']):
        mock_input.side_effect = ['0']
        social.show_my_network('testusername')
        out, _ = capsys.readouterr()
        for i in range(1, 4):
            assert f"{i}. pending{i}" in out
            assert f"{i}. connection{i}" in out


def test_show_my_network_disconnect_from_someone_successfully(capsys):
    with patch('builtins.input') as mock_input, \
            patch('social.db.get_pending_requests', return_value=[['pending1'], ['pending2'], ['pending3']]), \
            patch('social.db.get_connections', return_value=['connection1', 'connection2', 'connection3']):
        mock_input.side_effect = ['1', '1', 'yes', '0']
        social.show_my_network('testusername')
        out, _ = capsys.readouterr()
        assert "Select someone to disconnect from" in out
        assert "Disconnected from connection1" in out


def test_show_my_network_disconnect_from_someone_no_changes(capsys):
    with patch('builtins.input') as mock_input, \
            patch('social.db.get_pending_requests', return_value=[['pending1'], ['pending2'], ['pending3']]), \
            patch('social.db.get_connections', return_value=['connection1', 'connection2', 'connection3']):
        mock_input.side_effect = ['1', '1', 'no', '0']
        social.show_my_network('testusername')
        out, _ = capsys.readouterr()
        assert "No changes were made" in out


def test_show_my_network_accept_pending_request(capsys):
    with patch('builtins.input') as mock_input, \
            patch('social.db.get_pending_requests', return_value=[['pending1'], ['pending2'], ['pending3']]), \
            patch('social.db.get_connections', return_value=['connection1', 'connection2', 'connection3']), \
            patch('social.db.accept_friend_request', return_value=None):
        for i in range(1, 4):
            mock_input.side_effect = [f'a{i}']
            social.show_my_network('testusername')
            out, _ = capsys.readouterr()
            assert f"You are now connected with pending{i}" in out # check we can accept all pending connections
# (NEW TESTS) -------------------------
