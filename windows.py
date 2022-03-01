""" Class curse warper for display """
import curses
from number_map import number_map

class terminal():
    """ class warper curses to display """
    def __init__(self):
        # init screen
        self.scren = curses.initscr()
        # no echoing keys to screen
        curses.noecho()
        # react to keypress without Enter key
        curses.cbreak()
        # translat special keys
        self.scren.keypad(True)
        # disable blink cursor
        curses.curs_set(0)

        self.rows, self.columns = self.scren.getmaxyx()
        self.middle_row = int(self.rows / 2)
        self.middle_column = int(self.columns / 2)
        self.minutes = 0
        self.seconds = 0
        

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.close()

    def close(self):
        curses.curs_set(1)
        self.scren.keypad(False)
        curses.nocbreak()
        curses.echo()
        # destroy screen
        curses.endwin()

def countup(screen):
    curses.curs_set(0)
    num_rows, num_cols = screen.getmaxyx()
    middle_row = int(num_rows / 2) 
    middle_column = int(num_cols / 2) #-50

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)

    windows = [curses.newwin(6, 5, middle_row-3, middle_column-1),
        curses.newwin(6, 9, middle_row-3, middle_column-19),
        curses.newwin(6, 9, middle_row-3, middle_column-10),
        curses.newwin(6, 9, middle_row-3, middle_column+4),
        curses.newwin(6, 9, middle_row-3, middle_column+13)]
    # dot_window = curses.newwin(6, 2, middle_row, middle_column-1)
    # number2_window = curses.newwin(6, 9, middle_row-3, middle_column-10)
    # number1_window = curses.newwin(6, 9, middle_row-3, middle_column-19)
    # number3_window = curses.newwin(6, 9, middle_row-3, middle_column+1)
    # number4_window = curses.newwin(6, 9, middle_row-3, middle_column+10)
    
    # my_window.addstr(line, curses.color_pair(1))
    try:
        windows[0].addstr(number_map[':'])
    except curses.error:
        pass
    
    windows[0].refresh()

    # for wind in windows[1:]:
    #     wind.addstr(number_map['0'])
    #     wind.refresh()

    for i in range(10):
        for wind in windows[1:]:
            wind.erase()
            # wind.clear()
            wind.addstr(number_map[str(i)])
            wind.refresh()
        curses.napms(500)


    _ = windows[0].getch()


if __name__ == '__main__':
    curses.wrapper(countup)