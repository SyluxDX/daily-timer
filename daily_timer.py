""" main script for daily timer """
import argparse

from dataclasses import dataclass
from datetime import (datetime, timedelta)
from time import sleep
from random import shuffle

import src.configurations as cfgs
from src import windows
from src import team_statistics as stats

@dataclass
class _usertimer:
    def __init__(self, user: str, seconds: int) -> None:
        self.user = user
        self.seconds = seconds

class UsersTimer:
    """ Dataclass for users timers """
    def __init__(self, users_list: list, statistics: dict) -> None:
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

        # initiate stats with current users:
        self.stats = {}
        for user in users_list:
            if user in statistics:
                self.stats[user] = statistics[user]
            else:
                self.stats[user] = ""

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
            sline = f"        {self.stats[user.user.strip()]}"
            text.append(f"{prefix} {user.user} {user.seconds//60:02d}:{user.seconds%60:02d}{sline}")
        return text

    def get_list(self) -> list:
        """ Return list of tuples with users and current timer value, in seconds """
        return [(user.user, user.seconds) for user in self.users]

def set_color(configs: cfgs.Configurations, terminal: windows.Terminal, time_value: int) -> int:
    """ Returns new timer color based on the timer value (seconds) """
    color = terminal.WHITE
    if time_value >= configs.warning:
        color = terminal.YELLOW
    if time_value >= configs.time:
        color = terminal.RED

    return color

def update_timer(configs: cfgs.Configurations, terminal: windows.Terminal, time_value: int) -> None:
    """ Calculate display timer based on function mode """
    ## # calculate countdown display
    if not configs.stopwatch:
        time_value = abs(configs.time - time_value)

    # Update display time
    terminal.update_timer(time_value)

def timer_main_loop(configs: cfgs.Configurations, stats_path: str, ticks: float=0.25) -> None:
    """ script main loop. Handles timer ticks, and keyboard keys"""
    ## Variables
    running = False
    running_color = windows.Terminal.WHITE
    _aux_tick = timedelta(seconds=1)
    next_tick = None

    if configs.random:
        shuffle(configs.participants)

    user_stats = {}
    if configs.stats_display:
        user_stats = stats.read_last_dailies(stats_path, config.stats_number)

    users = UsersTimer(configs.participants, user_stats)
    seconds = 0

    ### create timer window
    with windows.Terminal() as terminal:
        # force first refresh and set color as pause (green)
        _ = terminal.get_key()
        terminal.update_color(terminal.GREEN)

        # write timer and user list
        update_timer(configs, terminal, seconds)
        terminal.update_users(users.str_list())

        while True:
            ## Get key press
            key = terminal.get_key()

            ## Pressed exit key
            if key == terminal.KEY_EXIT:
                # update last active user timer
                users.set_current_timer(seconds)
                stats.write_daily_times(stats_path, users.get_list())
                break

            ## Pressed start/pause key
            if key == terminal.KEY_SPACE:
                # toggle running status
                running = not running
                if running:
                    terminal.update_color(running_color)
                    next_tick = datetime.utcnow() + _aux_tick
                else:
                    terminal.update_color(terminal.GREEN)

            ## Press next person key
            if key == terminal.KEY_RIGHT:
                # update current user and get seconds of the next user
                users.set_current_timer(seconds)
                seconds = users.next_timer()

                # set timer color and update timer
                running_color = set_color(configs, terminal, seconds)
                if running:
                    terminal.update_color(running_color)
                terminal.update_users(users.str_list())

                # reset next_tick
                next_tick = datetime.utcnow() + _aux_tick

            ## Press previous person key
            if key == terminal.KEY_LEFT:
                # update current user and get seconds from previous user
                users.set_current_timer(seconds)
                seconds = users.previous_timer()

                # set timer color and update timer
                running_color = set_color(configs, terminal, seconds)
                if running:
                    terminal.update_color(running_color)
                terminal.update_users(users.str_list())

                # reset next_tick
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
                    next_tick += _aux_tick

            update_timer(configs, terminal, seconds)
            sleep(ticks)

_parser = argparse.ArgumentParser(description='Timer for Daily Timer.')
_parser.add_argument("-c", "--config", default="team.json", help='path for configuration')

ARGS = _parser.parse_args()

if __name__ == "__main__":
    try:
        config = cfgs.Configurations(ARGS.config)
        stat_filename = f"{ARGS.config[:-5]}_stats.csv"
        timer_main_loop(config, stat_filename)
    except cfgs.ConfigurationExeception as error:
        print(error, end="\n\n")
        input("Press Enter to exit")
