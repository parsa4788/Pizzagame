import random

world = []
height = 32
width = 84


def init():
    for i in range(-1, height + 1):
        world.append([])
        for j in range(-1, width + 1):
            world[i].append("#" if random.random() < 0.03 else " ")


def random_place():
    a = random.randint(0, height - 1)
    b = random.randint(0, width - 1)
    while world[a][b] != " ":
        a = random.randint(0, height - 1)
        b = random.randint(0, width - 1)
    return a, b


init()
x, y = random_place()
print(x, y)
