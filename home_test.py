import pytest
from unittest.mock import patch
from home import display_home_page


# Mocking user input for testing menu selections
def mock_input(mocked_inputs):
    return lambda _: mocked_inputs.pop(0)


# Test case for searching for a job
def test_search_for_job(capsys):
    with patch('builtins.input', side_effect=['A', 'X', 'E']):
        display_home_page("TestUser")
        out, _ = capsys.readouterr()
        assert "Oops! Under construction 🛠️\n" in out


# Test case for finding someone they know
def test_find_someone_they_know(capsys):
    with patch('builtins.input', side_effect=['B', 'X', 'E']):
        display_home_page("TestUser")
        out, _ = capsys.readouterr()
        assert "Oops! Under construction 🛠️\n" in out


# Test case for learning a new skill (Options 1-5)
def test_learn_skills(capsys):
    effects = []
    for skill_option in range(1, 6):
        effects.append('C')
        effects.append(str(skill_option))
        effects.append('X')
    effects.append('E')
    with patch('builtins.input', side_effect=effects):
        display_home_page("TestUser")
        out, _ = capsys.readouterr()
    # Assert that message appears 5 times (once for each skill)
    assert out.count('Oops! Under construction') == 5


# Test case for returning to the previous level
def test_return_to_previous_level(capsys):
    with patch('builtins.input', side_effect=['E']):
        display_home_page("TestUser")
        out, _ = capsys.readouterr()
        assert "Welcome back, TestUser!" in out


# Test case for invalid input
def test_invalid_input(capsys):
    with patch('builtins.input', side_effect=['X', 'E']):
        display_home_page("TestUser")
        out, _ = capsys.readouterr()
        assert "Error: Invalid choice. Please enter a valid character.\n" in out


if __name__ == '__main__':
    pytest.main()
