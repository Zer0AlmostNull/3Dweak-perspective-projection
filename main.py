import pygame as pg
import numpy as np

from math import cos, sin, pi

WND_WIDTH, WND_HEIGHT = 500, 500

CAM_POS = np.array([0,0,-45])
FOCAL_LENGTH = 500

verticies  = np.array([
    [1.0, 1.0, 1.0],
    [1.0, -1.0, 1.0],
    [-1.0, -1.0, 1.0],
    [-1.0, 1.0, 1.0],
    [1.0, 1.0,  -1.0],
    [1.0,-1.0, -1.0],
    [-1.0,-1.0, -1.0],
    [-1.0, 1.0, -1.0],
    ]) * 10

edges = [[0,1],
        [1,2],
        [2,3],
        [3,0],
        [4,5],
        [5,6], 
        [6,7],
        [7,4],
        [0,4],
        [1,5],
        [2,6],
        [3,7]]

def project_point(point: np.array):
    relative_postion = (point - CAM_POS) + np.array([0,0,0.0001])

    x_proj = (relative_postion[0] * FOCAL_LENGTH) / relative_postion[2]
    y_proj = (relative_postion[1] * FOCAL_LENGTH) / relative_postion[2]

    return x_proj, y_proj

def rotate_x(matrix, t):
    rotation_matrix = np.array([
        [1,       0,      0],
        [0,  cos(t), sin(t)],
        [0, -sin(t), cos(t)],
    ])

    return matrix.dot(rotation_matrix)

def rotate_y(matrix, t):
    
    rotation_matrix = np.array([
        [cos(t), 0, -sin(t)],
        [0,      1,       0],
        [sin(t), 0,  cos(t)],
    ])

    return matrix.dot(rotation_matrix)

def rotate_z(matrix, t):
    rotation_matrix = np.array([
        [cos(t),  sin(t), 0],
        [-sin(t), cos(t), 0],
        [0,            0, 1],
    ])

    return matrix.dot(rotation_matrix)

# pygame stuff
pg.init()
screen = pg.display.set_mode((WND_WIDTH, WND_HEIGHT))
clock = pg.time.Clock()
deltaTime = 1e-10

# main loop
while True:

    # pulling events
    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
    
    #project points
    rendered_points = [project_point(point) for point in verticies]

    #render lines
    for (a,b) in edges:
        a = rendered_points[a]
        b = rendered_points[b]
        pg.draw.line(screen, (255, 255, 255),
                     (WND_WIDTH//2 + a[0], WND_HEIGHT//2 - a[1]),
                     (WND_WIDTH//2 + b[0], WND_HEIGHT//2 - b[1]),
                     5)

    
    # draw verticies
    for point in rendered_points:
        pg.draw.circle(screen, (255, 255, 255), (WND_WIDTH//2 + point[0], WND_HEIGHT//2 - point[1]), 5)

    # rotate points
    verticies = rotate_y(verticies, pi/4*deltaTime)
    verticies = rotate_x(verticies, pi/3*deltaTime)
    #verticies = rotate_z(verticies, pi/2*deltaTime)


    # update screen
    pg.display.update()

    # reset background
    screen.fill((0,0,0))

    # tick the clock - fps control
    deltaTime = (clock.tick(0)/1000)
    