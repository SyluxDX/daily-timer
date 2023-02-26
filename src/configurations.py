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
    stats_display: bool
    stats_number : int

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
        self.stats_display = raw_config["stats"]["display"]
        self.stats_number = raw_config["stats"]["lastDailies"]

        if not self.stopwatch:
            # update warning limit in countdown mode
            self.warning = self.time - self.warning
