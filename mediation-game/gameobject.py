import pygame
class GameObject:
    color = (255, 0, 0)
    width, height = 50, 50
    x, y = 100,100

    #конструктор
    def __init__(self, x,y,w,h):
        self.x, self.y = x,y
        self.width, self.height = w,h
    #прямокутник для розрахунку колізій
    def rect(self):
        return pygame.Rect(self.x,self.y,self.width,self.height)
    #малювання об'єкту
    def draw(self, screen, offset_x, offset_y):
        pygame.draw.rect(screen, self.color, (self.x+offset_x, self.y+offset_y, self.width, self.height))
