""" main script for daily timer """
import windows
import time


def test():
    time.sleep(1)
    with windows.Terminal() as terminal:
    # terminal = windows.terminal()
        terminal.initiate_timer()
        # terminal.update_timer(12,34)
        # time.sleep(1)
        # terminal.update_timer(34,12, True, 1)
        # time.sleep(1)
        _ = terminal.timer_windows[0].getch()
        for x in range(100):
            if x == 60:
                terminal.update_color(terminal.RED)
            terminal.update_timer(x)
            
            time.sleep(0.25)


    # terminal.restorescreen()

if __name__ == "__main__":
    print("Hello")
    test()
