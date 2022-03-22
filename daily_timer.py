""" main script for daily timer """
import json
import time
import argparse
from collections import namedtuple
from datetime import (datetime, timedelta)

import windows

def get_configurations(filename):
    """ Read json configurations to a namedtupple enabeling dot access """
    configs = namedtuple("configs", ["time","warning","participants","sequencial"])
    with open(filename , "r", encoding="utf8") as cfp:
        data = json.load(cfp)
    return configs(data["time"], data["warning"], data["participants"], data["sequencial"])

def main_loop(configs, ticks=0.25):
    """ script main loop. Hadles timer ticks, and keyboard keys"""
    ## Variables
    running = False
    running_color = windows.Terminal.WHITE
    _aux_tick = timedelta(seconds=1)
    next_tick = None
    seconds = 0
    previous_seconds = 0
    ### create timer window
    with windows.Terminal() as terminal:
        _ = terminal.get_key()
        # set color as pause (green)
        terminal.update_color(terminal.GREEN)
        terminal.initiate_timer(seconds)
        while True:
            # terminal.debug_print(f"{running}, {next_tick}")

            key = terminal.get_key()
            if key == terminal.KEY_EXIT:
                break
            if key == terminal.KEY_SPACE:
                # toggle running status
                running = not running
                if running:
                    terminal.update_color(running_color)
                    terminal.update_timer(seconds)
                    next_tick = datetime.utcnow() + _aux_tick
                else:
                    terminal.update_color(terminal.GREEN)
                    terminal.update_timer(seconds)
            if key == terminal.KEY_RIGHT:
                previous_seconds = seconds
                seconds = 0
                running_color = terminal.WHITE
                terminal.update_color(running_color)
                terminal.update_timer(seconds)
                next_tick = datetime.utcnow() + _aux_tick
            if key == terminal.KEY_LEFT:
                seconds = previous_seconds
                running_color = terminal.WHITE
                if seconds >= configs.warning:
                    running_color = terminal.YELLOW
                if seconds >= configs.time:
                    running_color = terminal.RED

                terminal.update_color(running_color)
                terminal.update_timer(seconds)
                next_tick = datetime.utcnow() + _aux_tick

            if running is True:
                if next_tick is None:
                    next_tick = datetime.utcnow() + _aux_tick
                # check tick
                if datetime.utcnow() > next_tick:
                    seconds += 1
                    # check warning/burn threshold
                    if seconds == configs.warning:
                        running_color = terminal.YELLOW
                        terminal.update_color(running_color)
                    if seconds == configs.time:
                        running_color = terminal.RED
                        terminal.update_color(running_color)

                    terminal.update_timer(seconds)
                    next_tick += _aux_tick

            time.sleep(ticks)

_parser = argparse.ArgumentParser(description='Timer for Daiçy Timer.')
_parser.add_argument("-c", "--config", default="team.json",
                    help='path for configuration')

ARGS = _parser.parse_args()

if __name__ == "__main__":
    config = get_configurations(ARGS.config)
    main_loop(config)
