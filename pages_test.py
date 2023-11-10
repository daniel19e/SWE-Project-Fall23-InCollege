import pytest
from unittest.mock import patch, Mock
import pages


###################################################################################
# Test the General Links
def test_help_center_page(capsys):
    with patch("builtins.input", return_value="2"):
        pages.help_center_page()
    captured = capsys.readouterr()
    assert "We're here to help" in captured.out


def test_about_page(capsys):
    with patch("builtins.input", return_value="3"):
        pages.about_page()
    captured = capsys.readouterr()
    assert "In College: Welcome to In College," in captured.out


def test_press_page(capsys):
    with patch("builtins.input", return_value="4"):
        pages.press_page()
    captured = capsys.readouterr()
    assert "In College Pressroom: Stay on top of the latest news," in captured.out


def test_blog_page(capsys):
    with patch("builtins.input", return_value="5"):
        pages.blog_page()
    captured = capsys.readouterr()
    assert "Oops! Under construction 🛠️" in captured.out


def test_careers_page(capsys):
    with patch("builtins.input", return_value="6"):
        pages.careers_page()
    captured = capsys.readouterr()
    assert "Oops! Under construction 🛠️" in captured.out


def test_developers_page(capsys):
    with patch("builtins.input", return_value="7"):
        pages.developers_page()
    captured = capsys.readouterr()
    assert "Oops! Under construction 🛠️" in captured.out


def test_sign_up_page(capsys):
    with patch("builtins.input", return_value="x"):
        pages.sign_up_page()
    captured = capsys.readouterr()
    assert "Sign Up (Enter X to cancel)" in captured.out


###################################################################################


###################################################################################
# Test cases Important Links
def test_show_copyright_notice(capsys):
    with patch("builtins.input", return_value="1. A Copyright Notice"):
        pages.show_copyright_notice()
    captured = capsys.readouterr()
    assert "© 2023 InCollege, Inc. All rights reserved." in captured.out


# This test case was an exception, it gives an error unless full sentence is used
# "About\nIn College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide.\n"
def test_show_about(capsys):
    with patch("builtins.input", return_value="2. About"):
        pages.show_about()
    captured = capsys.readouterr()
    assert (
        "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide."
        in captured.out
    )


def test_show_accessibility(capsys):
    with patch("builtins.input", return_value="3. Accessibility"):
        pages.show_accessibility()
    captured = capsys.readouterr()
    assert (
        "InCollege, Inc. is committed to ensuring that our website is accessible to everyone,"
        in captured.out
    )


def test_show_user_agreement(capsys):
    with patch("builtins.input", return_value="4. User Agreement"):
        pages.show_user_agreement()
    captured = capsys.readouterr()
    assert (
        "By using the InCollege website and its associated services, you agree to comply with all applicable laws and our terms of service."
        in captured.out
    )


def test_show_privacy_policy(capsys):
    with patch("builtins.input", return_value="5. Privacy Policy"):
        pages.show_privacy_policy()
    captured = capsys.readouterr()
    assert "InCollege, Inc. values and respects your privacy." in captured.out


def test_show_cookie_policy(capsys):
    with patch("builtins.input", return_value="6. Cookie Policy"):
        pages.show_cookie_policy()
    captured = capsys.readouterr()
    assert (
        "InCollege, Inc. utilizes cookies to enhance your browsing experience and deliver personalized content."
        in captured.out
    )


def test_show_copyright_policy(capsys):
    with patch("builtins.input", return_value="7. Copyright Policy"):
        pages.show_copyright_policy()
    captured = capsys.readouterr()
    assert (
        "All content, designs, graphics, and other materials published by InCollege, Inc. on our website are protected by copyright law."
        in captured.out
    )


def test_show_brand_policy(capsys):
    with patch("builtins.input", return_value="8. Brand Policy"):
        pages.show_brand_policy()
    captured = capsys.readouterr()
    assert (
        "Copyright © 2023 InCollege, Inc.; all content is protected by law,"
        in captured.out
    )


def test_unauth_guest_controls(capsys):
    with patch("builtins.input", return_value="9. Guest Controls"):
        pages.show_guest_controls()
    captured = capsys.readouterr()
    assert "This is only available to logged in users.\n" in captured.out


def test_unauth_languages(capsys):
    with patch("builtins.input", return_value="10. Languages"):
        pages.show_languages()
    captured = capsys.readouterr()
    assert (
        "Once you have created an account, you will be able to choose which one you want to use."
        in captured.out
    )


###################################################################################


###################################################################################
# Testing Guest Control Options
user_info = [None, None, None, None, None, None, True, True, True]


@pytest.mark.parametrize(
    "option, sql_update",
    [
        ("1", "UPDATE college_students SET receive_emails = ? WHERE username = ?"),
        ("2", "UPDATE college_students SET receive_sms = ? WHERE username = ?"),
        ("3", "UPDATE college_students SET targeted_ads = ? WHERE username = ?"),
    ],
)
def test_show_guest_controls(option, sql_update):
    with patch("pages.input", side_effect=[option, "0"]) as mock_input, patch(
        "pages.db.get_user_info", return_value=user_info
    ) as mock_user_info, patch("pages.db.get_cursor") as mock_cursor, patch(
        "pages.db.get_connection"
    ) as mock_connection, patch(
        "pages.get_current_username", return_value="test_user"
    ) as mock_username:
        mock_cursor.return_value.execute = Mock()

        pages.show_guest_controls()

        mock_cursor.return_value.execute.assert_called_with(
            sql_update, (False, "test_user")
        )
        mock_connection.return_value.commit.assert_called_once()


###################################################################################


###################################################################################
# Test Useful Links
def test_general_link(capsys):
    with patch("builtins.input", return_value="0"):
        pages.general_link()
    captured = capsys.readouterr()
    assert "General links" in captured.out


def test_browse_incollege_link(capsys):
    with patch("builtins.input", return_value="2"):
        pages.browse_incollege_link()
    captured = capsys.readouterr()
    assert "Oops! Under construction 🛠️" in captured.out


def test_business_solutions_link(capsys):
    with patch("builtins.input", return_value="3"):
        pages.business_solutions_link()
    captured = capsys.readouterr()
    assert "Oops! Under construction 🛠️" in captured.out


def test_directories_link(capsys):
    with patch("builtins.input", return_value="4"):
        pages.directories_link()
    captured = capsys.readouterr()
    assert "Oops! Under construction 🛠️" in captured.ou

t
###################################################################################

# (NEW TESTS) ====================================


# Show Pending Resquests Page with no Pending Requests
def test_show_pending_requests_no_requests(capsys):
    with patch("builtins.input") as mock_input, patch(
        "pages.db.get_full_pending_requests", return_value=[]
    ):
        mock_input.side_effect = ["0"]
        pages.show_friend_requests()
        out, _ = capsys.readouterr()
        assert "You don't have any more pending friend requests." in out


# Show Pending Resquests Page with Pending Requests
def test_show_pending_requests(capsys):
    with patch("builtins.input") as mock_input, patch(
        "pages.db.get_full_pending_requests",
        return_value=[["testpending1"], ["testpending2"], ["testpending3"]],
    ):
        mock_input.side_effect = ["0"]
        pages.show_friend_requests()
        out, _ = capsys.readouterr()
        assert "You have the following friends requests:" in out
        assert "testpending1" in out
        assert "testpending2" in out
        assert "testpending3" in out


# Accept Pending Request
def test_accept_pending_request(capsys):
    with patch("builtins.input") as mock_input, patch(
        "pages.db.get_full_pending_requests", return_value=[["testpending1"]]
    ), patch("pages.db.accept_friend_request", return_value=None):
        mock_input.side_effect = ["a1", "0"]
        pages.show_friend_requests()
        out, _ = capsys.readouterr()
        assert "You successfully accepted the friend request" in out


# Reject Pending Request
def test_reject_pending_request(capsys):
    with patch("builtins.input") as mock_input, patch(
        "pages.db.get_full_pending_requests", return_value=[["testpending1"]]
    ), patch("pages.db.accept_friend_request", return_value=None):
        mock_input.side_effect = ["r1", "0"]
        pages.show_friend_requests()
        out, _ = capsys.readouterr()
        assert "You successfully rejected the friend request" in out


# Invalid Input in Pending Requests
def test_pending_request_invalid_input(capsys):
    with patch("builtins.input") as mock_input, patch(
        "pages.db.get_full_pending_requests",
        return_value=[["testpending1"], ["testpending2"], ["testpending3"]],
    ):
        mock_input.side_effect = ["x", "a0", "r0", "0"]
        pages.show_friend_requests()
        out, _ = capsys.readouterr()
        assert "Invalid input. Try again." in out


# ================================================
