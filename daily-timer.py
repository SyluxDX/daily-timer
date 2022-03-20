""" main script for daily timer """

import time
import json
import argparse
import windows
from collections import namedtuple

def get_configurations(filename):
    """ Read json configurations to a namedtupple enabeling dot access """
    config = namedtuple("configs", ["time","warning","participants","sequencial"])
    with open(filename , "r") as cfp:
        data = json.load(cfp)
    return config(data["time"], data["warning"], data["participants"], data["sequencial"])

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



_parser = argparse.ArgumentParser(description='Timer for Daiçy Timer.')
_parser.add_argument("-c", "--config", default="team.json",
                    help='path for configuration')

ARGS = _parser.parse_args()

if __name__ == "__main__":
    print("Hello")
    # test()
    config = get_configurations(ARGS.config)
    print(config)
    
