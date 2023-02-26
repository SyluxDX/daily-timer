""" Module to read, write and process team time statistics """
import os
from math import ceil
from datetime import datetime

def read_last_dailies(filename:str, dailies_to_import:int) -> dict:
    """ Read last dailies and calculate max, min and average for each team member """
    statistics = {}

    daily = None
    dailies = []
    team = {}
    ## check if file exists
    if not os.path.exists(filename):
        return statistics

    ## read file
    skip_line = True
    with open(filename, "r", encoding="utf8") as ifp:
        for lines in ifp:
            # skip header line
            if skip_line:
                skip_line = False
                continue

            date, member, seconds = lines.strip().split(",")
            if daily is None:
                daily = date

            if date != daily:
                dailies.append(team)
                if len(dailies) > dailies_to_import:
                    _ = dailies.pop(0)
                team = {}
                daily = date

            team[member] = int(seconds)

        # add last
        dailies.append(team)
        if len(dailies) > dailies_to_import:
            _ = dailies.pop(0)

    # calculate statistics
    team = {}
    for elem in dailies:
        for member, seconds in elem.items():
            if member in team:
                team[member].append(seconds)
            else:
                team[member] = [seconds]
    for member, times in team.items():
        avg_s = ceil(sum(times)/len(times))
        max_s = max(times)
        statistics[member] = f"avg: {avg_s//60:02d}:{avg_s%60:02d}, max: {max_s//60:02d}:{max_s%60:02d}"
    return statistics

def write_daily_times(filepath:str, times:list) -> None:
    """ Write daily menber times to statistics file """
    if not os.path.exists(filepath):
        # create file and write header
        with open(filepath, "w", encoding="utf8") as ofp:
            ofp.write("daily,name,time\n")

    # write daily times
    daily = datetime.now().isoformat()
    with open(filepath, "a", encoding="utf8") as ofp:
        for name, seconds in times:
            ofp.write(f"{daily},{name.strip()},{seconds}\n")

if __name__ == "__main__":
    stat = read_last_dailies("team_stats.csv", 3)
    print(stat)
