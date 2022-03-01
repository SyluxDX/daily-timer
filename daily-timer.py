""" main script for daily timer """
import windows
import curses
import time

def test():
    time.sleep(1)
    with windows.terminal() as terminal:
    # terminal = windows.terminal()
        time.sleep(1)
    # terminal.restorescreen()

if __name__ == "__main__":
    print("Hello")
    test()
