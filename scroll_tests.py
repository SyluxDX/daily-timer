""" test scroll implementation """

class Window:
    nlines: int
    start: int
    end: int
    last_position: int

    def __init__(self, lines, current):
        self.nlines = lines
        self.start = 0
        self.end = lines - 1
        self.last_position = current

    def print_users(self, user_list:list, current:int) -> None:
        ## window/scroll
        # calculate move direction
        direction = current - self.last_position
        print("direction:", direction)
        if direction > 0:
            # check right limit
            if current == self.end -1:
                # near window right limit
                if self.end+1 != len(user_list):
                    self.start += 1
                    self.end += 1
        if direction < 0:
            # check left limit
            if current == self.start + 1:
                # near window left limit
                if self.start -1 != -1:
                    self.start -= 1
                    self.end -= 1
        
        # jumps
        if abs(direction) == len(user_list) -1:
            if direction < 0:
                # jump from end to start
                self.start = 0
                self.end = self.nlines - 1
            else:
                print(self.nlines)
                # jump from start to end
                self.end = len(user_list) -1
                self.start = self.end - (self.nlines - 1)
        
        # update last position
        self.last_position = current

        ## debug print all with window
        text = []
        for i, line in enumerate(user_list):
            if i == self.start:
                text.append("------")
                text.append(line)
            elif i == self.end:
                text.append(line)
                text.append("------")
            else:
                text.append(line)

        print("\n".join(text))

        text = user_list[self.start:self.end+1]
        print("window")
        print("\n".join(text))

def prep_list(users: list, current:int) -> list:
    """ Get all users names, timer and current user as list of strings """
    text = []
    for i, user in enumerate(users):
        prefix = "  "
        if i == current:
            prefix = "->"
        text.append(f"{prefix} {user}")
    return text

def mainloop() -> None:
    users = [
        "Olivia",
        "William",
        "Emma",
        "Amelia",
        "Mia",
        "Benjamin",
        "Thomas",
        "Henry",
    ]
    current = 2
    window = Window(5, current)

    window.print_users(prep_list(users, current), current)

    while True:
        key = input(">")
        if key == "q":
            break
        if key == "a":
            current -= 1
            if current < 0:
                current = len(users)-1
        if key == "d":
            current += 1
            if current == len(users):
                current = 0

        # update
        print()
        window.print_users(prep_list(users, current), current)
        
        

if __name__ == "__main__":
    mainloop()
