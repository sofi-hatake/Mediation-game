import pygame
from spritesheet import SpriteSheet
from enum import Enum
from gameobject import GameObject

#напрям руху
class Direction(Enum):
    NONE = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4

#клас гравця
class Player(GameObject):
    speed = 8
    animation_frame = 0 #кадр анімації
    direction = Direction.NONE

    def __init__(self):
        GameObject.__init__(self, 165,228,24,24)
        ss = SpriteSheet('characters/girl.png')
        #завантаження кадрів анімації гравця
        self.images_up = ss.images_at(((0, 0, 24, 24), (0, 24, 24, 24),(0, 48, 24, 24)), colorkey=(0, 255, 0))
        self.images_right = ss.images_at(((24, 0, 24, 24), (24, 24, 24, 24), (24, 48, 24, 24)), colorkey=(0, 255, 0))
        self.images_down = ss.images_at(((48, 0, 24, 24), (48, 24, 24, 24), (48, 48, 24, 24)), colorkey=(0, 255, 0))
        self.images_left = ss.images_at(((72, 0, 24, 24), (72, 24, 24, 24), (72, 48, 24, 24)), colorkey=(0, 255, 0))
        self.images_none = ss.images_at(((96, 0, 24, 24), (96, 0, 24, 24), (96, 0, 24, 24)), colorkey=(0, 255, 0))

    #малювання гравця
    def draw(self, screen, offset_x, offset_y):
        if self.direction==Direction.RIGHT:
            screen.blit(self.images_right[self.animation_frame//10], (self.x+offset_x, self.y+offset_y))
        elif self.direction==Direction.DOWN:
            screen.blit(self.images_down[self.animation_frame//10], (self.x+offset_x, self.y+offset_y))
        elif self.direction==Direction.LEFT:
            screen.blit(self.images_left[self.animation_frame//10], (self.x+offset_x, self.y+offset_y))
        elif self.direction==Direction.UP:
            screen.blit(self.images_up[self.animation_frame//10], (self.x+offset_x, self.y+offset_y))
        elif self.direction==Direction.NONE:
            screen.blit(self.images_none[self.animation_frame//10], (self.x+offset_x, self.y+offset_y))
        #else:
        #    pygame.draw.rect(screen, self.color, (self.x+offset_x, self.y+offset_y, self.width, self.height))

        self.animation_frame += 1
        if self.animation_frame>29:
            self.animation_frame = 0