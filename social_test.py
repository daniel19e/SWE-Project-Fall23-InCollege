import pytest
from unittest.mock import Mock, MagicMock, ANY
from unittest.mock import patch
import social
from social import (
    connect_with_student,
    manage_network,
    generate_message_list,
    send_message,
)


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


@patch("social.db.search_first_and_last")
@patch("social.send_connection_request")
# Connection with student test
def test_connect_with_student_found(
    mock_send_connection_request, mock_search_first_and_last
):
    mock_search_first_and_last.return_value = True

    result = connect_with_student("John", "Doe")

    assert result == True

    mock_send_connection_request.assert_called_once_with("John", "Doe")


# Connection with student test(if the student is not found)


@patch("social.db.search_first_and_last")
def test_connect_with_student_not_found(mock_search_first_and_last):
    mock_search_first_and_last.return_value = False
    result = connect_with_student("Jane", "Doe")
    assert result == False


# (NEW TESTS) -------------------------
@patch("social.db.search_students_by_criteria")
def test_find_someone_i_know_lastname(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = [
        (
            1,
            "testusername",
            "testfirst",
            "testlast",
            "pass",
            "major",
            "univ",
            "english",
            1,
            1,
            1,
        )
    ]
    with patch("builtins.input") as mock_input:
        mock_input.side_effect = ["1", "0", "0"]
        social.find_someone_i_know("testuser1")
        out, _ = capsys.readouterr()
        assert "testfirst testlast - testusername" in out
        assert "Select a student to send a connection" in out


@patch("social.db.search_students_by_criteria")
def test_find_someone_i_know_university(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = [
        (
            1,
            "testusername",
            "testfirst",
            "testlast",
            "pass",
            "major",
            "univ",
            "english",
            1,
            1,
            1,
        )
    ]
    with patch("builtins.input") as mock_input:
        mock_input.side_effect = ["2", "0", "0"]
        social.find_someone_i_know("testuser1")
        out, _ = capsys.readouterr()
        assert "testfirst testlast - testusername" in out
        assert "Select a student to send a connection" in out


@patch("social.db.search_students_by_criteria")
def test_find_someone_i_know_major(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = [
        (
            1,
            "testusername",
            "testfirst",
            "testlast",
            "pass",
            "major",
            "univ",
            "english",
            1,
            1,
            1,
        )
    ]
    with patch("builtins.input") as mock_input:
        mock_input.side_effect = ["3", "0", "0"]
        social.find_someone_i_know("testuser1")
        out, _ = capsys.readouterr()
        assert "testfirst testlast - testusername" in out
        assert "Select a student to send a connection" in out


@patch("social.db.search_students_by_criteria")
def test_find_someone_i_know_invalid(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = [
        (
            1,
            "testusername",
            "testfirst",
            "testlast",
            "pass",
            "major",
            "univ",
            "english",
            1,
            1,
            1,
        )
    ]
    with patch("builtins.input") as mock_input:
        mock_input.side_effect = ["5", "0", "0"]
        social.find_someone_i_know("testuser1")
        out, _ = capsys.readouterr()
        assert "Invalid choice" in out


@patch("social.db.search_students_by_criteria")
def test_find_someone_i_know_no_results(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = []
    with patch("builtins.input") as mock_input:
        mock_input.side_effect = ["1", "0", "0"]
        social.find_someone_i_know("testuser1")
        out, _ = capsys.readouterr()
        assert "No students found with the provided criteria" in out


@patch("social.db.search_students_by_criteria")
def test_find_someone_i_know_send_connection(mock_search_student_by_criteria, capsys):
    mock_search_student_by_criteria.return_value = [
        (
            1,
            "testusername",
            "testfirst",
            "testlast",
            "pass",
            "major",
            "univ",
            "english",
            1,
            1,
            1,
        )
    ]
    with patch("social.db.send_friend_request"), patch("builtins.input") as mock_input:
        mock_input.side_effect = ["1", "0", "1"]
        social.find_someone_i_know("testuser1")
        out, _ = capsys.readouterr()
        assert "Connection request sent!" in out


def test_show_my_network_go_back(capsys):
    with patch("builtins.input") as mock_input, patch(
        "social.db.get_pending_requests", return_value=[]
    ), patch("social.db.get_connections", return_value=[]):
        mock_input.side_effect = ["0"]
        social.manage_network("testusername")
        out, _ = capsys.readouterr()
        assert (
            out
            == "\nYour Network:\n\nMake your selection:\n1. Disconnect from someone\n0. Go back\n"
        )


def test_show_my_network_show_pending_requests_and_connections(capsys):
    with patch("builtins.input") as mock_input, patch(
        "social.db.get_pending_requests",
        return_value=[["pending1"], ["pending2"], ["pending3"]],
    ), patch(
        "social.db.get_connections",
        return_value=["connection1", "connection2", "connection3"],
    ):
        mock_input.side_effect = ["0"]
        social.manage_network("testusername")
        out, _ = capsys.readouterr()
        for i in range(1, 4):
            assert f"{i}. pending{i}" in out
            assert f"{i}. connection{i}" in out


def test_show_my_network_disconnect_from_someone_successfully(capsys):
    with patch("builtins.input") as mock_input, patch(
        "social.db.get_pending_requests",
        return_value=[["pending1"], ["pending2"], ["pending3"]],
    ), patch(
        "social.db.get_connections",
        return_value=["connection1", "connection2", "connection3"],
    ):
        mock_input.side_effect = ["1", "1", "yes", "0"]
        social.manage_network("testusername")
        out, _ = capsys.readouterr()
        assert "Select someone to disconnect from" in out
        assert "Disconnected from connection1" in out


def test_show_my_network_disconnect_from_someone_no_changes(capsys):
    with patch("builtins.input") as mock_input, patch(
        "social.db.get_pending_requests",
        return_value=[["pending1"], ["pending2"], ["pending3"]],
    ), patch(
        "social.db.get_connections",
        return_value=["connection1", "connection2", "connection3"],
    ):
        mock_input.side_effect = ["1", "1", "no", "0"]
        social.manage_network("testusername")
        out, _ = capsys.readouterr()
        assert "No changes were made" in out


def test_show_my_network_accept_pending_request(capsys):
    with patch("builtins.input") as mock_input, patch(
        "social.db.get_pending_requests",
        return_value=[["pending1"], ["pending2"], ["pending3"]],
    ), patch(
        "social.db.get_connections",
        return_value=["connection1", "connection2", "connection3"],
    ), patch(
        "social.db.accept_friend_request", return_value=None
    ):
        for i in range(1, 4):
            mock_input.side_effect = [f"a{i}"]
            social.manage_network("testusername")
            out, _ = capsys.readouterr()
            # check we can accept all pending connections
            assert f"You are now connected with pending{i}" in out


# (NEW TESTS) -------------------------
def test_friend_list_display_update_friend_with_profile(capsys):
    """
    Test to check if the friend list is displayed with an option to select a friend's profile
    """
    # friend with a profile
    with patch("builtins.input") as mocked_input, patch(
        "social.db.get_connections", return_value=["john_doe", "jane_doe"]
    ), patch("social.db.profile_exists", return_value=True), patch(
        "student_profile.display_profile"
    ) as mocked_display_profile:
        mocked_input.side_effect = ["p1", "0"]  # press p1 and go back
        manage_network("current_user")
        mocked_display_profile.assert_called_with(ANY, "john_doe")


def test_friend_list_show_profile_option(capsys):
    with patch("builtins.input") as mocked_input, patch(
        "social.db.get_connections", return_value=["john_doe", "jane_doe"]
    ), patch("social.db.profile_exists", return_value=True), patch(
        "student_profile.display_profile"
    ) as mocked_display_profile:
        mocked_input.side_effect = ["p1", "0"]  # press p1 and go back
        manage_network("current_user")
        mocked_display_profile.assert_called_with(ANY, "john_doe")
        out, _ = capsys.readouterr()
        assert "john_doe - View Profile (press p1)" in out
        assert "jane_doe - View Profile (press p2)" in out


def test_friend_list_display_update_friend_with_no_profile(capsys):
    """
    Test to check if the friend list is displayed with an option to select a friend's profile
    """
    # friend with a profile
    with patch("builtins.input") as mocked_input, patch(
        "social.db.get_connections", return_value=["john_doe", "jane_doe"]
    ), patch("social.db.profile_exists", return_value=False), patch(
        "student_profile.display_profile"
    ) as mocked_display_profile:
        mocked_input.side_effect = ["p1", "0"]  # press p1 and go back
        manage_network("current_user")
        out, _ = capsys.readouterr()
        assert "john_doe" in out
        assert "jane_doe" in out
        assert "Invalid profile choice or profile does not exist." in out
        mocked_display_profile.assert_not_called()


def test_profile_display_is_called(capsys):
    """
    Test to check if the correct friend's profile is displayed when selected
    """
    with patch("student_profile.display_profile") as mocked_display_profile, patch(
        "builtins.input"
    ) as mocked_input, patch(
        "social.db.get_connections", return_value=["john_doe"]
    ), patch(
        "social.db.profile_exists", return_value=True
    ), patch(
        "student_profile.display_profile"
    ) as mocked_display_profile:
        mocked_input.side_effect = ["p1", "0"]
        manage_network("current_user")
        mocked_display_profile.assert_called_with(ANY, "john_doe")


# check if the message functions works or not
def test_generate_message_list():
    with patch("social.db") as mock_db:
        mock_db.get_user_info.return_value = {"id": "saheddin1"}
        mock_db.generate_message_list.return_value = [
            {"sender": "saheddin2", "message": "Hello TA", "time": "2023-11-05 19:40"}
        ]
        mock_db.get_user_by_id.return_value = "saheddin2"

        with patch("social.input", return_value="0"), patch(
            "social.print"
        ) as mock_print:
            generate_message_list("testuser")
            mock_print.assert_any_call("Message #1, sent by Saheddin2:")
            mock_print.assert_any_call("Hello TA")


# check if our code can delete the message
def test_delete():
    with patch("social.db") as mock_db:
        # Setup mock data
        mock_db.get_user_info.return_value = {"id": "ben_ten"}
        message_id = "msg001"
        mock_db.generate_message_list.return_value = [
            {
                "id": message_id,
                "sender": "saheddin1",
                "message": "I hope you are having a good day!",
                "time": "2023-11-05 20:07",
            }
        ]
        mock_db.get_user_by_id.return_value = "ben_ten"

        with patch("social.input", side_effect=["delete 1", "0"]), patch(
            "social.print"
        ) as mock_print:
            generate_message_list("testusre")
            mock_db.delete_message_by_id.assert_called_with(message_id)
            mock_print.assert_any_call("Message deleted successfully!\n")


# check whether there is an option to reply the message(respond is the name of requirement in the epic)
def test_reply():
    with patch("social.db") as mock_db:
        # Setup mock data
        mock_db.get_user_info.return_value = {"id": "saheddin2"}
        mock_db.generate_message_list.return_value = [
            {
                "id": "msg002",
                "sender": "kevin_eleven",
                "message": "testing reply here",
                "time": "2023-11-05 20:24",
            }
        ]
        mock_db.get_user_by_id.return_value = "kevin_eleven"

        with patch("social.input", side_effect=["reply 1", "0"]), patch(
            "social.send_message"
        ) as mock_send_message, patch("social.print") as mock_print:
            generate_message_list("testuser")
            mock_send_message.assert_called_with("testuser", "kevin_eleven", True)


# Test to check send_message when receiver is not in the system
def test_send_message_receiver_not_in_system():
    with patch("social.db") as mock_db, patch("social.clear_terminal"), patch(
        "social.print"
    ) as mock_print:
        mock_db.get_user_info.side_effect = [
            True,
            None,
        ]  # User exists, receiver doesn't
        send_message("testuser", "unknown_user", False)
        mock_print.assert_any_call(
            "As a free tier, you must be friends with the person you're trying to message.\n"
        )


# Test to check send_message when a user tries to message themselves
def test_send_message_to_self():
    with patch("social.db") as mock_db, patch("social.clear_terminal"), patch(
        "social.print"
    ) as mock_print:
        mock_db.get_user_info.return_value = True
        send_message("testuser", "testuser", True)
        mock_print.assert_any_call("You cannot send a message to yourself.\n")


# Test to check send_message when non-plus tier user tries to message a non-friend
def test_send_message_non_plus_non_friend():
    with patch("social.db") as mock_db, patch("social.clear_terminal"), patch(
        "social.print"
    ) as mock_print:
        mock_db.get_user_info.return_value = True
        mock_db.get_connections.return_value = ["friend_user"]
        send_message("testuser", "not_a_friend", False)
        mock_print.assert_any_call(
            "As a free tier, you must be friends with the person you're trying to message.\n"
        )


# Test to check generate_message_list with invalid reply format
def test_generate_message_list_invalid_reply():
    with patch("social.db") as mock_db, patch(
        "social.input", side_effect=["reply", "0"]
    ), patch("social.clear_terminal"), patch("social.print") as mock_print:
        mock_db.get_user_info.return_value = {"id": "testuser"}
        generate_message_list("testuser")
        mock_print.assert_any_call("Error: Invalid input.\n")


# Test to check generate_message_list with invalid delete format
def test_generate_message_list_invalid_delete():
    with patch("social.db") as mock_db, patch(
        "social.input", side_effect=["delete", "0"]
    ), patch("social.clear_terminal"), patch("social.print") as mock_print:
        mock_db.get_user_info.return_value = {"id": "testuser"}
        generate_message_list("testuser")
        mock_print.assert_any_call("Error: Invalid input.\n")
