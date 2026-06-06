import curses
import random

global player_l, player_c


def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.curs_set(0)
    stdscr.nodelay(False)
    height, width = stdscr.getmaxyx()
    global player_l, player_c
    player_l = player_c = 0
    height -= 1
    width -= 1
    world = []

    def random_place():
        a = random.randint(0, height - 1)
        b = random.randint(0, width - 1)
        while world[a][b] != " ":
            a = random.randint(0, height - 1)
            b = random.randint(0, width - 1)
        return a, b

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def in_range(num, min, max):
        if num > max:
            num = max
        if num < min:
            num = min
        return num

    def init():
        for i in range(-1, height + 1):
            world.append([])
            for j in range(-1, width + 1):
                world[i].append("#" if random.random() < 0.02 else " ")
        player_l, player_c = random_place()
        stdscr.addch(player_l, player_c, "P", curses.color_pair(1))

    def draw():
        for i in range(height):
            for j in range(width):
                stdscr.addch(i, j, world[i][j], curses.color_pair(2))
        stdscr.addch(player_l, player_c, "P", curses.color_pair(1))

    def move(c):
        global player_l, player_c
        """Get one of [WASD] and move towards that direction"""
        if c == "w" and world[player_l - 1][player_c] != "#":
            player_l -= 1
        elif c == "s" and world[player_l + 1][player_c] != "#":
            player_l += 1
        elif c == "a" and world[player_l][player_c - 1] != "#":
            player_c -= 1
        elif c == "d" and world[player_l][player_c + 1] != "#":
            player_c += 1
        player_l = in_range(player_l, 0, height - 1)
        player_c = in_range(player_c, 0, width - 1)

    init()
    draw()
    playing = True
    while playing:
        try:
            char = stdscr.getkey()
        except:
            char = ""
        if char == "q":
            playing = False
        elif char in "wasd":
            move(char)
        draw()
    stdscr.refresh()


curses.wrapper(main)
