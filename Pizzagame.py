import curses
import random
import time


def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.curs_set(0)
    stdscr.nodelay(False)
    height, width = stdscr.getmaxyx()
    global player_l, player_c, score, playing
    playing = True
    score = 0
    player_l = player_c = 0
    height -= 1
    width -= 1
    world = []
    food = []
    enemy = []

    def random_place():
        a = random.randint(0, height - 1)
        b = random.randint(0, width - 1)
        while world[a][b] != " ":
            a = random.randint(0, height - 1)
            b = random.randint(0, width - 1)
        return a, b

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    def eat_food():
        global score
        for i in range(len(food)):
            fl, fc, fa = food[i]
            if fl == player_l and fc == player_c:
                score += 10
                nfl, nfc = random_place()
                nfa = random.randint(1000, 10000)
                food[i] = (nfl, nfc, nfa)

    def on_enemy():
        global playing
        for i in range(len(enemy)):
            el, ec = enemy[i]
            if el == player_l and ec == player_c:
                stdscr.addstr(height // 2, (width // 2) - 7, "YOU DIDE, SIR.")
                stdscr.refresh()
                time.sleep(3)
                playing = False

    def check_score():
        global score

    def in_range(num, min, max):
        if num > max:
            num = max
        if num < min:
            num = min
        return num

    def init():
        global player_l, player_c
        for i in range(0, height + 1):
            world.append([])
            for j in range(-1, width + 1):
                world[i].append("#" if random.random() < 0.03 else " ")
        player_l, player_c = random_place()
        stdscr.addch(player_l, player_c, "P", curses.color_pair(1))
        for i in range(10):
            fl, fc = random_place()
            fa = random.randint(1000, 10000)
            food.append((fl, fc, fa))
        for i in range(random.randint(10, 25)):
            el, ec = random_place()
            enemy.append((el, ec))

    def draw():
        for i in range(height):
            for j in range(width):
                stdscr.addch(i, j, world[i][j], curses.color_pair(2))
        stdscr.addstr(0, 0, f"score = {score}")
        stdscr.addch(player_l, player_c, "P", curses.color_pair(1))
        for f in food:
            fl, fc, fa = f
            stdscr.addch(fl, fc, "*", curses.color_pair(3))
        for e in enemy:
            el, ec = e
            stdscr.addch(el, ec, "%", curses.color_pair(4))

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
    while playing:
        try:
            key = stdscr.getkey()
        except:
            key = ""
        if key == "q":
            playing = False
        elif key in "wasd":
            move(key)
            on_enemy()
            eat_food()

        draw()
    stdscr.refresh()


curses.wrapper(main)
