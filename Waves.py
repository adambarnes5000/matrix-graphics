from Matrix import Matrix, SPHERE, CUBE
import pi3d
import math
import random
import time

display = pi3d.Display.create(x=20, y=20, w=1920,h=1080,background=(0.0, 0.0, 0.1, 1.0))
pi3d.Light(lightpos=(-10.0, 4.0, 10.0), lightcol=(3.0, 3.0, 2.0), lightamb=(0.5, 0.5, 0.7), is_point=True)
camera = pi3d.Camera()

EDGE_SIZE = 24

RADIUS = 60
TILT = -10

WIDTH = EDGE_SIZE
HEIGHT = EDGE_SIZE
DEPTH = EDGE_SIZE

angle=0.0
delta=0.5

counter = 5.0
direction = 1

matrix = Matrix(WIDTH, HEIGHT, DEPTH, shape=SPHERE)

while display.loop_running():
    #matrix.show_corners()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            for z in range(DEPTH):
                dx = (WIDTH / 2.0) - x
                dy = (HEIGHT / 2.0) - y
                dz = (DEPTH / 2.0) - z
                d = math.sqrt(dx * dx + dy * dy + dz * dz)
                matrix.set_point((x,y,z),int(math.sqrt(dx*dx+dy*dy+dz*dz))==counter)
    camera.relocate(point=(math.sin(math.radians(angle))*RADIUS, 10, -math.cos(math.radians(angle))*RADIUS), rot=angle, tilt=TILT)

    matrix.draw_matrix()

    angle += delta

    counter += direction

    if counter>=math.sqrt(HEIGHT*HEIGHT+WIDTH*WIDTH+DEPTH*DEPTH)/4 or counter<=1:
        direction = 0 - direction

    time.sleep(0.05)