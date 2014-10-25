import pygame
import sys
import math

def get_angle(pos):
    center = v_control.center
    x = pos[0]
    y = pos[1]
    rad = 0.0
    if y < center[1]:
        opposite = float(center[1] - y)
        if x > center[0]:
            adjacent = float(x - center[0])
            rad = math.atan(opposite/adjacent)
        elif x < center[0]:
            adjacent = float(center[0] - x)
            rad = math.pi - (math.atan(opposite/adjacent))
        else:
            rad = 0.5 * math.pi
    elif y > center[1]:
        opposite = float(y - center[1])
        if x < center[0]:
            adjacent = float(center[0] - x)
            rad = math.pi + (math.atan(opposite/adjacent))
        elif x > center[0]:
            adjacent = float(x - center[0])
            rad = (2 * math.pi) - math.atan(opposite/adjacent)
        else:
            rad = 1.5 * math.pi
    else:
        if x < center[0]:
            rad = math.pi
    return rad


def beam(angle):
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