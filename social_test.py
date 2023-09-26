import pytest
from unittest.mock import Mock
from unittest.mock import patch
import social
from social import connect_with_student

@pytest.fixture
def mock_db():
    return Mock(search_first_and_last=Mock(return_value=True))
#test case for checking wheteher the code takes firstname and lastname for input (NEW TEST CASE)
@pytest.fixture
def mock_input(monkeypatch):
    mock = Mock(side_effect=["Abdulla", "Majidov"])
    monkeypatch.setattr("builtins.input", mock)
    return mock

#supposed reaction if the name is a member of InCollege (NEW TEST CASE)
def test_promote_marketing_program_member(mock_db, mock_input, capsys):
    with patch.object(social, "db", mock_db):
        social.promote_marketing_program()
    captured = capsys.readouterr()
    assert "You are a part of the InCollege system.\n" in captured.out

#supposed reaction if the name is not a member of InCollege
def test_promote_marketing_program_non_member(mock_db, mock_input, capsys):
    mock_db.search_first_and_last.return_value = False
    with patch.object(social, "db", mock_db):
        social.promote_marketing_program()
    captured = capsys.readouterr()
    assert "You are not a part of the InCollege system yet.\n" in captured.out
    

@patch('social.db.search_first_and_last')
@patch('social.send_connection_request')
#Connection with student test (new test case)
def test_connect_with_student_found(mock_send_connection_request, mock_search_first_and_last):
    mock_search_first_and_last.return_value = True

    result = connect_with_student('John', 'Doe')

    assert result == True

    mock_send_connection_request.assert_called_once_with('John', 'Doe')
#Connection with student test(if the student is not found) ()
@patch('social.db.search_first_and_last')
def test_connect_with_student_not_found(mock_search_first_and_last):
    mock_search_first_and_last.return_value = False
    
    result = connect_with_student('Jane', 'Doe')
    
    assert result == False
