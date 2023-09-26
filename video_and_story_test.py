import time
from unittest.mock import patch
from video import play_video
from io import StringIO
import sys
import pytest
from success_story import display_story

def test_play_video(capsys):
    sys.stdout = StringIO()

    with patch('builtins.input', side_effect=['3']):
        play_video()

    captured_output = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = sys.__stdout__

    # Check if the expected messages are displayed
    expected_output = [
        "Video is now playing",
        "Video is now playing .",
        "Video is now playing . .",
        "Video is now playing . . .",
        "Video is now playing . . . .",
        "Video is now playing . . . . ."
    ]

    for message in expected_output:
        assert message in captured_output

    # Check if the video visual is displayed (at least once)
    assert "Video is now playing . . . . .\n" in captured_output

    # Check if the function waits for 6 seconds (6 iterations of the loop)
    time.sleep(6)


# List of potential success stories
potential_stories = [
"""
❝ Meet Sarah, a college freshman who used InCollege to connect with alumni in her field of study. She landed an internship
  at a top company thanks to valuable advice and connections she made through the app. ❞
""",
"""
❝ John, a struggling college student, discovered numerous scholarship opportunities on InCollege. With the app's guidance,
  he applied for and won a scholarship that covered his tuition, easing his financial burden. ❞
""",
"""
❝ Emily found it challenging to study alone. InCollege helped her form a study group with classmates who shared her course.
  Together, they aced their exams and improved their grades. ❞
""",
"""
❝ Matt used InCollege to build a standout resume. He showcased his achievements and skills, attracting the attention of recruiters.
  He secured a prestigious summer internship that kick-started his career. ❞
""",
"""
❝ After graduation, Lisa was struggling to find a job. She tapped into InCollege's job search feature and found a
  position perfectly aligned with her degree. The app's notifications made her job hunt effortless. ❞
""",
"""
❝ Tom, a junior, sought career guidance. InCollege connected him with a mentor who shared his passion.
  With personalized advice, he gained clarity on his career path and made informed decisions. ❞
""",
"""
❝ InCollege's event calendar helped Jessica discover networking events, workshops, and career fairs happening on campus.
  Attending these events led her to secure multiple job interviews and expand her professional network. ❞
""",
"""
❝ David, a sophomore, wanted to explore different career options. InCollege's internship database allowed him to research
  and apply for various internships, helping him gain valuable experience in his desired field. ❞
""",
"""
❝ Emma had a brilliant startup idea but lacked a team. InCollege's project collaboration feature allowed her to connect
  with like-minded students. Together, they launched a successful business that now thrives. ❞
""",
"""
❝ Alex, a shy student, used InCollege to improve his communication skills. Through online discussions and forums, he gradually gained
  confidence. Eventually, he became the president of a student organization, showcasing his newfound leadership abilities. ❞
"""
]

def test_display_story(capsys):
    with patch('builtins.input', side_effect=["0"]):
        display_story()
        captured = capsys.readouterr()
        displayed_story = captured.out.strip()  # Remove leading/trailing whitespace

        # Check if the displayed story is in the list of potential stories
        assert any(story.strip() == displayed_story for story in potential_stories)

if __name__ == "__main__":
    import pytest
    pytest.main()
