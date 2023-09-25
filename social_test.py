import pytest
from unittest.mock import Mock
from unittest.mock import patch
import social

@pytest.fixture
def mock_db():
    return Mock(search_first_and_last=Mock(return_value=True))
#test case for checking wheteher the code takes firstname and lastname for input
@pytest.fixture
def mock_input(monkeypatch):
    mock = Mock(side_effect=["Abdulla", "Majidov"])
    monkeypatch.setattr("builtins.input", mock)
    return mock

#supposed reaction if the name is a member of InCollege
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
