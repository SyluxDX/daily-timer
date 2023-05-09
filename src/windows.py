""" Class curse warper for display """
import curses
from src.number_map import number_map

class Terminal():
    """ class warper curses to display """
    # colors
    WHITE: int = 0
    GREEN: int = 1
    YELLOW: int = 2
    RED: int = 3

    # keys
    KEY_LEFT: int = curses.KEY_LEFT
    KEY_RIGHT: int = curses.KEY_RIGHT
    KEY_SPACE: int = ord(" ")
    KEY_EXIT: int = ord("q")
    KEY_HELP: int = ord("h")

    def __init__(self):
        # init screen
        self.screen: curses.window = curses.initscr()
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
        self.written_minutes: int = 0
        self.written_seconds: int = 0

        # timer variables
        self.timer_windows = []
        self.color: int = 0
        self.force_update: bool = False
        ## Initiate timer windows positions and values
        # timer_windows = [:, 1, 2, 3, 4] -> 12:34
        self.timer_windows = [
            curses.newwin(6, 5, 2, self.middle_column-1),
            curses.newwin(6, 9, 2, self.middle_column-19),
            curses.newwin(6, 9, 2, self.middle_column-10),
            curses.newwin(6, 9, 2, self.middle_column+4),
            curses.newwin(6, 9, 2, self.middle_column+13),
        ]

        self.debug_window = curses.newwin(1,100,0,0)
        # users variables
        self.users_nlines = 10
        self.users_ncols = 50
        self.users_current = 0
        self.users_start = 0
        self.users_end = self.users_nlines -1
        ## Initiante user window
        # create window
        self.users_window = curses.newwin(
            self.users_nlines,
            self.users_ncols,
            11,
            self.middle_column//2,
        )

        self.help_line = curses.newwin(2, 22, 22, self.middle_column-10)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, _exception_value, _exception_traceback) -> None:
        print("type:", exception_type)
        self.close()

    def close(self) -> None:
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
    def update_color(self, color: int) -> None:
        """ Update timer text color """
        self.color = color
        self.force_update = True

    def update_timer(self, seconds: int, force: bool =False) -> None:
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
            self.written_minutes = int(minutes)

        str_seconds = f"{seconds%60:02d}"
        if force or self.written_seconds != seconds:
            self.timer_windows[3].erase()
            self.timer_windows[3].addstr(number_map[str_seconds[0]], curses.color_pair(self.color))
            self.timer_windows[3].refresh()

            self.timer_windows[4].erase()
            self.timer_windows[4].addstr(number_map[str_seconds[1]], curses.color_pair(self.color))
            self.timer_windows[4].refresh()
            # update last written
            self.written_seconds = int(seconds)

    ## Users list related functions
    def update_users(self, lines: list, current:int) -> None:
        """ Update/refresh user list window with line list

        Number of lines and size are limited to window size """

        # number of lines fewer or equal than window size
        if len(lines) <= self.users_nlines:
            self.users_window.erase()
            self.users_window.addstr("\n".join(lines))
            self.users_window.refresh()
            return

        # scroll window
        direction = current - self.users_current
        if direction > 0:
            if abs(direction) == len(lines) -1:
                # jump from start to end
                self.users_end = len(lines) - 1
                self.users_start = self.users_end - (self.users_nlines -1)
            elif current == self.users_end - 1 and self.users_end+1 != len(lines):
            # near window right limit
                self.users_start += 1
                self.users_end += 1
        
        if direction < 0:
            if abs(direction) == len(lines) - 1:
                # jump from start to end
                self.users_start = 0
                self.users_end = self.users_nlines -1
            elif current == self.users_start + 1 and self.users_start -1 != -1:
            # near window left limit
                self.users_start -= 1
                self.users_end -= 1

        self.users_current = current
        self.users_window.erase()
        self.users_window.addstr("\n".join(lines[self.users_start:self.users_end+1]))
        self.users_window.refresh()
    
    def write_help_footer(self) -> None:
        """ Write help and exit keys footer """
        self.help_line.erase()
        self.help_line.addstr("Press h for help menu\nPress q to exit")
        self.help_line.refresh()

    def write_help_menu(self) -> None:
        """ Write/hide help keys menu """
        self.update_users([
            "Left Arrow", "  Select previous participant",
            "Right Arrow", "  Select next participant",
            "Space", "  Toggle timer pause/resume",
            "h", "  Display/Hide help menu",
            "q", "  Exit application",
        ], 0)

    ## General Terminal functions
    def get_key(self) -> int:
        """ Get keyboard key press """
        key = self.screen.getch()
        return key
