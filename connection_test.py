import pytest
from social import connect_with_student
from unittest.mock import patch

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