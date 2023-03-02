""" Dailty Timer configurations class """
import json
from dataclasses import dataclass

class ConfigurationExeception(Exception):
    """ Configurations exception class """

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
        try:
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
        except FileNotFoundError as exc:
            raise ConfigurationExeception(
                f"ERROR: Configuration file not found with path: {filename}"
            ) from exc
        except KeyError as error:
            raise ConfigurationExeception(
                f"ERROR: Field {error.args[0]} not defiend in configuration file."
            ) from error

        if not self.stopwatch:
            # update warning limit in countdown mode
            self.warning = self.time - self.warning
