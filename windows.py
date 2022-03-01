""" Class curse warper for display """
import curses
from number_map import number_map

class Terminal():
    """ class warper curses to display """
    WHITE = 0
    RED = 1
    YELLO = 2

    def __init__(self):
        # init screen
        self.screen = curses.initscr()
        # no echoing keys to screen
        curses.noecho()
        # react to keypress without Enter key
        curses.cbreak()
        # translate special keys
        self.screen.keypad(True)
        # enable terminal color
        curses.start_color()
        # disable blink cursor
        curses.curs_set(0)

        # set curses colors
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)


        self.rows, self.columns = self.screen.getmaxyx()
        self.middle_row = int(self.rows / 2)
        self.middle_column = int(self.columns / 2)
        self.written_minutes = 0
        self.written_seconds = 0

        self.timer_windows = None
        self.color = 0
        self.force_update = False

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        print("type:", exception_type)
        self.close()

    def close(self):
        """ Cleanup console """
        curses.curs_set(1)
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        # destroy screen
        curses.endwin()

    def initiate_timer(self, seconds=0):
        """ Initiate timer windows positions and values """
        # timer_windows = [:, 1, 2, 3, 4] -> 12:34
        self.timer_windows = [curses.newwin(6, 5, self.middle_row-3, self.middle_column-1),
                              curses.newwin(6, 9, self.middle_row-3, self.middle_column-19),
                              curses.newwin(6, 9, self.middle_row-3, self.middle_column-10),
                              curses.newwin(6, 9, self.middle_row-3, self.middle_column+4),
                              curses.newwin(6, 9, self.middle_row-3, self.middle_column+13)]

        self.update_timer(seconds, True)

# TODO: Redesign this function to only update only once, preferably on the next update
    def update_color(self, color):
        """ asd """
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
