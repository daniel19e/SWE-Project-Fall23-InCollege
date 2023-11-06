import pytest
from unittest.mock import Mock, MagicMock, ANY
from unittest.mock import patch
from social import generate_message_list

#check if the message functions works or not
def test_generate_message_list():
    with patch('social.db') as mock_db:
        mock_db.get_user_info.return_value = {'id': 'saheddin1'}
        mock_db.generate_message_list.return_value = [{'sender': 'saheddin2', 'message': 'Hello TA', 'time': '2023-11-05 19:40'}]
        mock_db.get_user_by_id.return_value = 'saheddin2'

        with patch('social.input', return_value='0'), patch('social.print') as mock_print:
            generate_message_list('testuser')
            mock_print.assert_any_call("Message #1, sent by Saheddin2:")
            mock_print.assert_any_call("Hello TA")

#check if our code can delete the message
def test_delete():
    with patch('social.db') as mock_db:
        # Setup mock data
        mock_db.get_user_info.return_value = {'id': 'ben_ten'}
        message_id = 'msg001'
        mock_db.generate_message_list.return_value = [{'id': message_id, 'sender': 'saheddin1', 'message': 'I hope you are having a good day!', 'time': '2023-11-05 20:07'}]
        mock_db.get_user_by_id.return_value = 'ben_ten'

        with patch('social.input', side_effect=['delete 1', '0']), patch('social.print') as mock_print:
            generate_message_list('testusre')
            mock_db.delete_message_by_id.assert_called_with(message_id)
            mock_print.assert_any_call("Message deleted successfully!\n")

#check whether there is an option to reply the message(respond is the name of requirement in the epic)
def test_reply():
    with patch('social.db') as mock_db:
        # Setup mock data
        mock_db.get_user_info.return_value = {'id': 'saheddin2'}
        mock_db.generate_message_list.return_value = [{'id': 'msg002', 'sender': 'kevin_eleven', 'message': 'testing reply here', 'time': '2023-11-05 20:24'}]
        mock_db.get_user_by_id.return_value = 'kevin_eleven'

        with patch('social.input', side_effect=['reply 1', '0']), patch('social.send_message') as mock_send_message, patch('social.print') as mock_print:
            generate_message_list('testuser')
            mock_send_message.assert_called_with('testuser', 'kevin_eleven', True)