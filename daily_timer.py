""" main script for daily timer """
import argparse
from time import sleep
from datetime import (datetime, timedelta)
from random import shuffle

import configurations
import windows

class _usertimer:
    def __init__(self, user: str, seconds: int) -> None:
        self.user = user
        self.seconds = seconds

class UsersTimer:
    """ Dataclass for users timers """
    def __init__(self, users_list: list) -> None:
        # get max len of user name
        max_name = 0
        ## find max lenght of names
        for name in users_list:
            max_name = max(max_name, len(name))

        # Create usertimer with trailing whitespaces as padding
        self.users = [
            _usertimer( user+" "*(max_name-len(user) ), 0) for user in users_list
            ]
        self.current = 0

    def set_current_timer(self, seconds: int) -> None:
        """ Set/update current user timer """
        self.users[self.current].seconds = seconds

    def next_timer(self) -> int:
        """ Get next user timer value and update current user to that user """
        self.current += 1
        if self.current == len(self.users):
            self.current = 0
        return self.users[self.current].seconds

    def previous_timer(self) -> int:
        """ Get previous user timer value and update current user to that user """
        self.current -= 1
        if self.current < 0:
            self.current = len(self.users)-1
        return self.users[self.current].seconds

    def str_list(self) -> list:
        """ Get all users names, timer and current user as list of strings """
        text = []
        for i, user in enumerate(self.users):
            prefix = "  "
            if i == self.current:
                prefix = "->"
            text.append(f"{prefix} {user.user} {user.seconds//60:02d}:{user.seconds%60:02d}")
        return text

def set_color(configs, windows_controller: windows.Terminal, timer_value: int) -> int:
    """ Returns new timer color based on the timer value (seconds) and function mode """
    # if configs.stopwatch
    # placeholder configuration
    stopwatch = True
    color = windows_controller.WHITE
    if stopwatch:
        if timer_value >= configs.warning:
            color = windows_controller.YELLOW
        if timer_value >= configs.time:
            color = windows_controller.RED
    return color

def main_loop(configs, ticks=0.25):
    """ script main loop. Handles timer ticks, and keyboard keys"""
    ## Variables
    running = False
    running_color = windows.Terminal.WHITE
    _aux_tick = timedelta(seconds=1)
    next_tick = None

    if configs.random:
        shuffle(configs.participants)
    users = UsersTimer(configs.participants)
    seconds = 0

    ### create timer window
    with windows.Terminal() as terminal:
        # force first refresh
        _ = terminal.get_key()
        # set color as pause (green)
        terminal.update_color(terminal.GREEN)
        # write timer and user list
        terminal.update_timer(seconds)
        terminal.update_users(users.str_list())
        while True:
            ## Get key press
            key = terminal.get_key()

            ## Pressed exit key
            if key == terminal.KEY_EXIT:
                ### ToDo: Write statictis to file here ###
                break

            ## Pressed start/pause key
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

            ## Press next person key
            if key == terminal.KEY_RIGHT:
                # update current user
                users.set_current_timer(seconds)
                # get next user
                seconds = users.next_timer()
                # set timer color
                running_color = set_color(configs, terminal, seconds)

                # update timer
                if running:
                    terminal.update_color(running_color)
                terminal.update_timer(seconds)
                terminal.update_users(users.str_list())
                next_tick = datetime.utcnow() + _aux_tick

            ## Press previous person key
            if key == terminal.KEY_LEFT:
                # update current user
                users.set_current_timer(seconds)
                # get next user
                seconds = users.previous_timer()
                # set timer color
                running_color = set_color(configs, terminal, seconds)
                # update timer
                if running:
                    terminal.update_color(running_color)
                terminal.update_timer(seconds)
                terminal.update_users(users.str_list())
                next_tick = datetime.utcnow() + _aux_tick

            ## Timer loop
            if running is True:
                if next_tick is None:
                    next_tick = datetime.utcnow() + _aux_tick
                # check tick
                if datetime.utcnow() > next_tick:
                    seconds += 1
                    # check warning/burn threshold
                    new_color = set_color(configs, terminal, seconds)
                    if running_color != new_color:
                        running_color = new_color
                        terminal.update_color(running_color)
                    terminal.update_timer(seconds)
                    next_tick += _aux_tick

            sleep(ticks)

_parser = argparse.ArgumentParser(description='Timer for Daily Timer.')
_parser.add_argument("-c", "--config", default="team.json", help='path for configuration')

ARGS = _parser.parse_args()

if __name__ == "__main__":
    # config = get_configurations(ARGS.config)
    try:
        config = configurations.Configurations(ARGS.config)
        main_loop(config)
    except KeyError as error:
        print(f"ERROR: Field {error.args[0]} not defiend in configuration file.")
    except FileNotFoundError as error:
        print(f"ERROR: Configuration file not found with path: {ARGS.config}")
