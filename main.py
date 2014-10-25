import pygame
import sys
import math

def get_angle(pos):
    """
    :param pos: mouse position
    :return: radian angle of mouse position away from center.
    Divide the virtual controller into three sections.
    For the y-axis, the mouse point is either:
    1) above the center of the controller
    2) below the center of the controller
    3) at the same height of the center of the controller
    If the mouse point is above the center of the controller, than check
    for one of three conditions:
    1) x is to the right of the controller
    2) x is to the left of the controller
    3) x is at the same point as the centerx of the controller
    """
    center = v_control.center
    x = pos[0]
    y = pos[1]
    rad = 0.0
    if y < center[1]:

        if x > center[0]:
            opposite = float(center[1] - y)
            adjacent = float(x - center[0])
            rad = math.atan(opposite/adjacent)
        elif x < center[0]:
            opposite = float(center[0] - x)
            adjacent = float(center[1] - y)
            rad = .5 * math.pi + (math.atan(opposite/adjacent))
        else:
            rad = 0.5 * math.pi
    elif y > center[1]:
        if x < center[0]:
            opposite = float(y - center[1])
            adjacent = float(center[0] - x)
            rad = math.pi + (math.atan(opposite/adjacent))
        elif x > center[0]:
            adjacent = float(y - center[1])
            opposite = float(x - center[0])
            rad = (1.5 * math.pi) + math.atan(opposite/adjacent)
        else:
            rad = 1.5 * math.pi
    else:
        if x < center[0]:
            rad = math.pi
    return rad


def beam(angle):
    """
    :param angle: radians calculated from the virtual controller
    :return: x,y coordinates of the end-point
    Start with the center of the player.  The end of the beam is 100 pixels
    away from the center.  To make a bullet instead of beam, create a class
    for bullet and have the hypoteneuse be an attribute that increases
    in size.  Remember to delete the bullet from the sprite group or list
    when it goes off the screen.
    """
    hypoteneuse = 100.0
    center = (400, 300)
    adjacent = math.cos(angle) * hypoteneuse
    x = adjacent + center[0]
    opposite = math.sin(angle) * hypoteneuse
    y = center[1] - opposite
    beam_end = (x, y)
    return beam_end


pygame.init()

SCREEN = pygame.display.set_mode((800, 600))

RED = (100, 10, 10)
BLUE = (68, 204, 230)
v_control = pygame.Rect(650, 450, 100, 100)
player = pygame.Rect(0, 0, 20, 20)
player.center = (400, 300)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pos = pygame.mouse.get_pos()
    SCREEN.fill((0,0,0))
    pygame.draw.circle(SCREEN, RED, v_control.center, 50, 2)
    pygame.draw.circle(SCREEN, RED, v_control.center, 3)
    pygame.draw.circle(SCREEN, BLUE, player.center, 20, 2)
    if v_control.collidepoint(pos):
        rad = get_angle(pos)
        print(rad)
        end_point = beam(rad)
        pygame.draw.line(SCREEN, BLUE, (400, 300), end_point)

    pygame.display.update()