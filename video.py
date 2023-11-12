import time
from util import clear_terminal


def play_video():
    video = """
╔────────────────────────────────────────╗
│                                        │
│                 │`.                    │
│                 │  `.                  │
│                 │    >                 │
│                 │  .'                  │
│                 │.'                    │
│                                        │
╚────────────────────────────────────────╝
"""
    t = 6
    while t:
        clear_terminal()

        print(video)

        if t % 6 == 0:
            print("Video is now playing")
        if t % 6 == 5:
            print("Video is now playing .")
        if t % 6 == 4:
            print("Video is now playing . .")
        if t % 6 == 3:
            print("Video is now playing . . .")
        if t % 6 == 2:
            print("Video is now playing . . . .")
        if t % 6 == 1:
            print("Video is now playing . . . . .")

        t -= 1

        time.sleep(1)
