""" main script for daily timer """
from ast import While
import time
import json
import argparse
from collections import namedtuple
from datetime import (date, datetime, timedelta)

from click import secho

import windows


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

def main_loop(configs, ticks=0.25):
    """ script main loop. Hadles timer ticks, and keyboard keys"""
    ## Variables
    running = False
    running_color = windows.Terminal.WHITE
    _aux_tick = timedelta(seconds=1)
    next_tick = None #datetime.utcnow()+ _aux_tick
    _seconds = 0
    _previous_seconds = 0
    ### create timer window
    with windows.Terminal() as terminal:
        _ = terminal.get_key()
        # set color as pause (green)
        terminal.update_color(terminal.GREEN)
        terminal.initiate_timer(seconds=_seconds)
        while True:
            terminal.debug_print(f"{running}, {next_tick}")

            key = terminal.get_key()
            # key = terminal.timer_windows[0].getch()
            if key == terminal.KEY_EXIT:
                break
            if key == terminal.KEY_SPACE:
                # toggle running status
                running = not running
                if running:
                    terminal.update_color(running_color)
                    terminal.update_timer(_seconds)
                    next_tick = datetime.utcnow() + _aux_tick
                else:
                    terminal.update_color(terminal.GREEN)
                    terminal.update_timer(_seconds)
            if key == terminal.KEY_RIGHT:
                _previous_seconds = _seconds
                _seconds = 0
                running_color = terminal.WHITE
                terminal.update_color(running_color)
                terminal.update_timer(_seconds)
                next_tick = datetime.utcnow() + _aux_tick
            if running == True:
                if next_tick is None:
                    next_tick = datetime.utcnow() + _aux_tick
                # check tick
                if datetime.utcnow() > next_tick:
                    _seconds += 1
                    # check warning/burn threshold 
                    if _seconds == configs.warning:
                        running_color = terminal.YELLOW
                        terminal.update_color(running_color)
                    if _seconds == configs.time:
                        running_color = terminal.RED
                        terminal.update_color(running_color)

                    terminal.update_timer(_seconds)
                    next_tick += _aux_tick
                
            
            time.sleep(ticks)



_parser = argparse.ArgumentParser(description='Timer for Daiçy Timer.')
_parser.add_argument("-c", "--config", default="team.json",
                    help='path for configuration')

ARGS = _parser.parse_args()

if __name__ == "__main__":
    print("Hello")
    # test()
    config = get_configurations(ARGS.config)
    print(config)
    main_loop(config)
