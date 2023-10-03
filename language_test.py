import pytest
from unittest.mock import patch, Mock
import pages

###################################################################################
#Function for Language Selection
user_info = [None, None, None, None, None, 'English']

@pytest.mark.parametrize("option, language", [
    ('1', "english"),
    ('2', "spanish"),
])
def test_show_languages(option, language):
    with patch('pages.input', side_effect=[option, '0']) as mock_input, \
         patch('pages.db.get_user_info', return_value=user_info) as mock_user_info, \
         patch('pages.db.get_cursor') as mock_cursor, \
         patch('pages.db.get_connection') as mock_connection, \
         patch('pages.get_current_username', return_value='test_user') as mock_username:

        mock_cursor.return_value.execute = Mock()
        mock_connection.return_value.commit = Mock()

        pages.show_languages()

        mock_cursor.return_value.execute.assert_called_with(
            f"UPDATE college_students SET language = '{language}' WHERE username = ?",
            ('test_user',)
        )
        mock_connection.return_value.commit.assert_called
###################################################################################