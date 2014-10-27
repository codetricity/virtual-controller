import pygame
import sys
import math

try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer


def get_angle(pos, control_center):
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
    center = control_center
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


def beam(angle, center):
    """
    :param angle: radians calculated from the virtual controller
    :return: x,y coordinates of the end-point
    Start with the center of the player.  The end of the beam is 100 pixels
    away from the center.  To make a bullet instead of beam, create a class
    for bullet and have the hypoteneuse be an attribute that increases
    in size.  Remember to delete the bullet from the sprite group or list
    when it goes off the screen.
    """
    hypoteneuse = 30.0
    adjacent = math.cos(angle) * hypoteneuse
    x = adjacent + center[0]
    opposite = math.sin(angle) * hypoteneuse
    y = center[1] - opposite
    beam_end = (x, y)
    return beam_end

def move(angle, center):
    hypotenuse = 10.0
    adjacent = math.cos(angle) * hypotenuse
    x = int(adjacent + center[0])
    opposite = math.sin(angle) * hypotenuse
    y = int(center[1] - opposite)
    return ((x, y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, p_pos):
        YELLOW = (250, 223, 65)
        RED = (200, 10, 10)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((6,6))
        pygame.draw.circle(self.image, YELLOW, (3, 3), 3)
        pygame.draw.circle(self.image, RED, (3,3), 1)
        self.rect = self.image.get_rect()
        self.hypotenuse = 30.0
        self.angle = angle
        self.cent = p_pos

    def update(self):
        adjacent = math.cos(self.angle) * self.hypotenuse
        x = adjacent + self.cent[0]
        opposite = math.sin(self.angle) * self.hypotenuse
        y = self.cent[1] - opposite
        self.rect.center = (x, y)
        self.hypotenuse += 5




pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
screen_rect = SCREEN.get_rect()

RED = (100, 10, 10)
BLUE = (68, 204, 230)
GREEN = (113, 134, 84)

FPS =30

clock = pygame.time.Clock()

v_control = pygame.Rect(650, 450, 100, 100)
move_control = pygame.Rect(50, 450, 100, 100)
# print(v_control.center)
player = pygame.Rect(0, 0, 20, 20)
player.center = (400, 300)

bullet_group = pygame.sprite.Group()
bullet_delay = 15
bullet_timer = bullet_delay

ray_gun = mixer.Sound("snd/ray_gun.wav")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pos = pygame.mouse.get_pos()
    SCREEN.fill((0,0,0))
    pygame.draw.circle(SCREEN, RED, v_control.center, 50, 2)
    pygame.draw.circle(SCREEN, RED, v_control.center, 3)
    pygame.draw.circle(SCREEN, GREEN, move_control.center, 50, 2)
    pygame.draw.circle(SCREEN, GREEN, move_control.center, 3)

    pygame.draw.circle(SCREEN, BLUE, player.center, 20, 2)
    if v_control.collidepoint(pos):
        rad = get_angle(pos, v_control.center)
        end_point = beam(rad, player.center)
        pygame.draw.line(SCREEN, BLUE, player.center, end_point,6)

        if bullet_timer > 0:
            bullet_timer -= 1
        else:
            p_pos = player.center
            bullet = Bullet(rad, p_pos)
            bullet_group.add(bullet)
            bullet_timer = bullet_delay
            ray_gun.play()

    if move_control.collidepoint(pos):
        rad = get_angle(pos, move_control.center)
        if player.right < screen_rect.right and player.left > 0 and \
                        player.top > 0 and player.bottom < screen_rect.bottom:
            player_pos = move(rad, player.center)
            player.center = player_pos
        if player.right >= screen_rect.right:
            player.left = player.left - 5
        if player.left <= 0:
            player.right = player.right + 5
        if player.top <= 0:
            player.bottom = player.bottom + 5
        if player.bottom >= screen_rect.bottom:
            player.top = player.top - 5

    for bullet in bullet_group:
        if screen_rect.colliderect(bullet.rect):
            pass
        else:
            bullet_group.remove(bullet)

    bullet_group.update()
    bullet_group.draw(SCREEN)
    clock.tick(FPS)
    pygame.display.update()