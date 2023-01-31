""" Dailty Timer configurations class """
import json
from dataclasses import dataclass

@dataclass
class Configurations:
    """ General Configuration """
    time: int
    warning: int
    participants: list
    random: bool
    stopwatch: bool

    def __init__(self, filename) -> None:
        # read file
        with open(filename, "r", encoding="utf8") as cfp:
            raw_config = json.load(cfp)
        # Update class fields
        self.time = raw_config["time"]
        self.warning = raw_config["warning"]
        self.participants = raw_config["participants"]
        self.random = raw_config["randomOrder"]
        self.stopwatch = raw_config["stopwatch"]

        if not self.stopwatch:
            # update warning limit in ccountdown mode
            self.warning = self.time - self.warning
