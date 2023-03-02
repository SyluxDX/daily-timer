# daily-timer
A Timer for Daily Standup meetings

# Key Mapping
| Key         | Action                              |
|-------------|-------------------------------------|
| Left Arrow  | Select previous participant on list |
| Right Arrow | Select next participant on list     |
| Space       | Toggle timer pause/resume           |
| q           | Exit application                    |

# Configurations
| Name              | Type        | Description                                                     |
|-------------------|-------------|-----------------------------------------------------------------|
| time              | int         | limit of seconds after which enter in overtime                  |
| warning           | int         | Number of seconds when an warning wil be displayed              |
| participants      | list of str | List of team members                                            |
| randomOrder       | bool        | Flag to randomize the participants list before each startup     |
| stopwatch         | bool        | Function mode flag. True: stopwatch, False: countdown           |
| stats.display     | bool        | Flag to display or hide statistics on member list               |
| stats.lastDailies | int         | Number of last dailies to include in the statistic calculations |

# Build from Source
### Linux
- Create a virtual enviroment
- Install the requiments specified in the file `requirements_linux.txt`
- Run PyInstaller on main script:
```sh
$ pyinstaller --onefile daily_timer.py
```

### Windows
- Create a virtual enviroment
- Install the requiments specified in the file `requirements_windows.txt`
- Run PyInstaller on main script:
```sh
$ pyinstaller --onefile --icon NONE daily_timer.py
```

### ToDo:
- Scroll capabilities when there are more than 10 tem members
- Add tooltip for keys at the bottom of screen
