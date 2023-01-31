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
| Name         | Type        | Description                                                 |
|--------------|-------------|-------------------------------------------------------------|
| time         | int         | limit of seconds after which enter in overtime              |
| warning      | int         | Number of seconds when an warning wil be displayed          |
| participants | list of str | List of team menbers                                        |
| randomOrder  | bool        | Flag to randomize the participants list before each startup |
| stopwatch    | bool        | Function mode flag. True: stopwatch, False: countdown       |

## Roadmap
### Release 0
 - Stopwatch
 - Keyboard interations
 - Warning colors

### Release 1:
 - Participants list

### Release 2:
 - Timer Mode

### Release 3:
 - Participants Statistics

### ToDo:
 - Add Type hints to every function
