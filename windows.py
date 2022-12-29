""" Class curse warper for display """
import curses
from number_map import number_map

class Terminal():
    """ class warper curses to display """
    # colors
    WHITE = 0
    GREEN = 1
    YELLOW = 2
    RED = 3

    # keys
    KEY_LEFT = curses.KEY_LEFT
    KEY_RIGHT = curses.KEY_RIGHT
    KEY_SPACE = ord(" ")
    KEY_EXIT = ord("q")

    def __init__(self):
        # init screen
        self.screen = curses.initscr()
        # no echoing keys to screen
        curses.noecho()
        # react to keypress without Enter key
        curses.cbreak()
        # translate special keys
        self.screen.keypad(True)
        # set getch() be non-blocking.
        self.screen.nodelay(True)
        # enable terminal color
        curses.start_color()
        # disable blink cursor
        curses.curs_set(0)

        # set curses colors
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        # windows variables
        self.rows, self.columns = self.screen.getmaxyx()
        self.middle_row = int(self.rows / 2)
        self.middle_column = int(self.columns / 2)
        self.written_minutes = 0
        self.written_seconds = 0

        # timer variables
        self.timer_windows = []
        self.color = 0
        self.force_update = False
        ## Initiate timer windows positions and values
        # timer_windows = [:, 1, 2, 3, 4] -> 12:34
        self.timer_windows = [
            curses.newwin(6, 5, 2, self.middle_column-1),
            curses.newwin(6, 9, 2, self.middle_column-19),
            curses.newwin(6, 9, 2, self.middle_column-10),
            curses.newwin(6, 9, 2, self.middle_column+4),
            curses.newwin(6, 9, 2, self.middle_column+13),
        ]

        # users variables
        self.users_nlines = 10
        self.users_ncols = 50
        ## Initiante user window
        # create window
        self.users_window = curses.newwin(
            self.users_nlines,
            self.users_ncols,
            11,
            self.middle_column//2,
        )

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        print("type:", exception_type)
        self.close()

    def close(self):
        """ Cleanup console """
        curses.curs_set(1)
        # needed?
        self.screen.nodelay(False)
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        # destroy screen
        curses.endwin()

    ## Timer related functions
    def update_color(self, color):
        """ Update timer text color """
        self.color = color
        self.force_update = True

    def update_timer(self, seconds, force=False):
        """ Update timer values on screen, only write changes from previous update, use
        argument force=True to for """
        force = force or self.force_update
        minutes = f"{seconds//60:02d}"
        if force:
            # update colon
            self.timer_windows[0].erase()
            self.timer_windows[0].addstr(number_map[':'], curses.color_pair(self.color))
            self.timer_windows[0].refresh()

        if force or self.written_minutes != minutes:
            self.timer_windows[1].erase()
            self.timer_windows[1].addstr(number_map[minutes[0]], curses.color_pair(self.color))
            self.timer_windows[1].refresh()

            self.timer_windows[2].erase()
            self.timer_windows[2].addstr(number_map[minutes[1]], curses.color_pair(self.color))
            self.timer_windows[2].refresh()
            # update last written
            self.written_minutes = minutes

        seconds = f"{seconds%60:02d}"
        if force or self.written_seconds != seconds:
            self.timer_windows[3].erase()
            self.timer_windows[3].addstr(number_map[seconds[0]], curses.color_pair(self.color))
            self.timer_windows[3].refresh()

            self.timer_windows[4].erase()
            self.timer_windows[4].addstr(number_map[seconds[1]], curses.color_pair(self.color))
            self.timer_windows[4].refresh()
            # update last written
            self.written_seconds = seconds

    ## Users list related functions
    def update_users(self, lines: list) -> None:
        """ Update/refresh user list window with line list

        Number of lines and size are limited to window size """
        text = []
        for user in lines[:self.users_nlines]:
            text.append(user[:self.users_ncols])
        self.users_window.erase()
        self.users_window.addstr("\n".join(text))
        self.users_window.refresh()

    ## General Terminal functions
    def get_key(self):
        """ Get keyboard key press """
        key = self.screen.getch()
        return key
