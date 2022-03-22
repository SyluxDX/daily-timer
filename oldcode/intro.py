import curses

print("Preparing to initialize screen...")
screen = curses.initscr()
print("Screen initialized.")
screen.refresh()

curses.napms(2000)
curses.endwin()

print("Window ended.")
