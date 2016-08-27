#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

from Matrix import Matrix
import pi3d
import math
import random
import time

DISPLAY = pi3d.Display.create(x=20, y=20, w=1920,h=1080,background=(0.0, 0.0, 0.1, 1.0))
light = pi3d.Light(lightpos=(-10.0, 4.0, 10.0), lightcol=(3.0, 3.0, 2.0), lightamb=(0.5, 0.5, 0.7), is_point=True)
camera = pi3d.Camera()

EDGE_SIZE = 32
SNAKE_LENGTH = 10

RADIUS = 60
TILT = -10

WIDTH = EDGE_SIZE
HEIGHT = EDGE_SIZE
DEPTH = EDGE_SIZE

angle=0.0
delta=0.5

counter = 0.0
counter_delta = 1

matrix = Matrix(WIDTH, HEIGHT, DEPTH)

directions = [(1, 0 , 0),(-1, 0, 0),(0, 1 , 0),(0, -1, 0),(0, 0, 1),(0, 0, -1)]

snake = []
head = 0

direction = 0

def turn_snake():
    global direction
    x,y,z = snake[head]
    bad_choices=[math.floor(direction/2.0)*2, math.floor(direction / 2.0) * 2 + 1]
    if x<(WIDTH/2):
        bad_choices.append(1)
    else:
        bad_choices.append(0)
    if y < (HEIGHT / 2):
        bad_choices.append(3)
    else:
        bad_choices.append(2)
    if z < (DEPTH / 2):
        bad_choices.append(5)
    else:
        bad_choices.append(4)
    options=[]
    for i, d in enumerate(directions):
        if i not in bad_choices:
            options.append(i)
    direction = random.choice(options)


def get_next_pos():
    return tuple(map(sum, zip(snake[head], directions[direction])))


def move_snake():
    global head
    tail_pos = snake[(head+1) % SNAKE_LENGTH]
    head_pos = snake[head]
    matrix.set_point(tail_pos, 0)
    tail_pos = tuple(map(sum, zip(head_pos, directions[direction])))
    tail_pos = (tail_pos[0] % WIDTH, tail_pos[1] % HEIGHT, tail_pos[2] % DEPTH)
    matrix.set_point(tail_pos, 1)
    head = (head+1) % SNAKE_LENGTH
    snake[head] = tail_pos


for i in range(SNAKE_LENGTH):
    snake.append((i,int(HEIGHT/2),int(DEPTH/2)))
    matrix.set_point(snake[i], 1)


while DISPLAY.loop_running():
    matrix.show_corners()
    camera.relocate(point=(math.sin(math.radians(angle))*RADIUS, 10, -math.cos(math.radians(angle))*RADIUS), rot=angle, tilt=TILT)

    matrix.draw_matrix()

    angle += delta

    next_pos = get_next_pos()
    x, y, z = next_pos

    if next_pos in snake or 1 == random.randrange(0, 32):
        turn_snake()

    if x==WIDTH or y==HEIGHT or z==DEPTH or x==-1 or y==-1 or z==-1:
        turn_snake()

    move_snake()

    time.sleep(0.05)