""" Daily timer """
import argparse
import json
import re
from typing import NamedTuple, Sequence

# C-like structures
class Config(NamedTuple):
    time: int
    warning: int
    participants: list
    sequencial: bool


def read_config_file(filepath, config):
    """ Read Configuration file, overwrites with read fields """
    with open(filepath, 'r') as cfp:
        jdata = json.load(cfp)
    if 'time' in jdata:
        config.time = jdata['time']
    if 'warning' in jdata:
        config.warning = jdata['warning']
    if 'participants' in jdata:
        config.participants = jdata['participants']
    if 'sequencial' in jdata:
        config.sequencial = jdata['sequencial']

def get_configurations():
    """ Process input arguments and generate script configurations """
    time = None
    warning = None
    participants = None
    sequencial = False

    if ARGS.config:
        # read json file
        with open(ARGS.config, 'r') as cfp:
            jdata = json.load(cfp)
            if 'time' in jdata:
                time = jdata['time']
            if 'warning' in jdata:
                warning = jdata['warning']
            if 'participants' in jdata:
                participants = jdata['participants']
            if 'sequencial' in jdata:
                sequencial = jdata['sequencial']
    # Argparse overwrite
    if ARGS.time:
        time = ARGS.time
    if ARGS.warning:
        warning = ARGS.warning
    if ARGS.participants:
        participants = ''.join(ARGS.participants)
    if ARGS.sequencial:
        sequencial = ARGS.sequencial

    timeparser = re.compile(r'((?P<min>\d+)m)?(?P<sec>\d+)s?')
    # parse time
    if time and type(time) == str:
        aux = 0
        match = timeparser.match(time).groupdict()
        if match['min']:
            aux = 60*int(match['min'])
        time = aux + int(match['sec'])
    # parse warning
    if warning and type(warning) == str:
        aux = 0
        match = timeparser.match(warning).groupdict()
        if match['min']:
            aux = 60*int(match['min'])
        warning = aux + int(match['sec'])
    # parse participants
    if participants and type(participants) == str:
        participants = participants.split(',')

    return Config(time, warning, participants, sequencial)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Daily standup Timer')
    # add arguments
    parser.add_argument('-c', '--config', help='Path to configuration json override')
    parser.add_argument('time', nargs='?', help='Time limit for each participant, if not provided will operate as stopwatch')
    parser.add_argument('-w', '--warning', help='Warning time, if not profided defaults to 1/3 of time limit')

    parser.add_argument('-p', '--participants', nargs='+', help='List of participants')
    parser.add_argument('-sp', '--seperator-participants', default=',', help='Seperator of thf participant list')
    parser.add_argument('-s', '--sequencial', action='store_true', help='Use participants in sequencial order (don\'t shuffle participants)')

    ARGS = parser.parse_args()
    print(ARGS.participants)
    CONFIG = get_configurations()
    print("asdasd")
    print(CONFIG)