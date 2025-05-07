import pygame
from gameobject import GameObject

class Obstacle(GameObject):
    tile = "" #ім'я файлу з зображенням
    sprite = None
    #конструктор
    def __init__(self, x,y,w,h,tile=""):
        GameObject.__init__(self,x,y,w,h)
        self.tile = tile
        if tile!="":
            self.sprite = pygame.image.load(tile)
    #малювання перешкоди
    def draw(self, screen, offset_x, offset_y):
        if self.tile=="":
            pygame.draw.rect(screen, self.color, (self.x+offset_x, self.y+offset_y, self.width, self.height))
        else:
            screen.blit(self.sprite, (self.x+offset_x, self.y+offset_y))
