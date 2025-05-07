import pygame
from gameobject import GameObject

class Portrait(GameObject):
    male_faces =  {"neutral": "characters/male.neutral.png", "negative": "characters/male.negativ.png", "positive": "characters/male.happy.png"} #файли портретів
    female_faces = {"neutral": "characters/female.neutral.png", "negative": "characters/female.negativ.png", "positive": "characters/female.happy.png"}  # файли портретів
    gender = "жінка"
    emotion = "neutral"
    sprite = None

    #конструктор
    def __init__(self, x,y,w,h,gender="жінка"):
        GameObject.__init__(self,x,y,w,h)
        self.gender = gender
        self.set_emotion("neutral")

    def set_emotion(self, emotion = "neutral"):
        try:
            if self.gender == "чоловік":
                self.sprite = pygame.image.load(self.male_faces[emotion])
            elif self.gender == "жінка":
                self.sprite = pygame.image.load(self.female_faces[emotion])
            else:
                self.sprite = None
        except:
            self.sprite = None

    def set_gender(self, gender="чоловік"):
        self.gender = gender
        self.set_emotion("neutral")

    def draw(self, screen, offset_x, offset_y):
        if self.gender == "асистент":
            return
        if self.sprite is None:
            pygame.draw.rect(screen, self.color, (self.x + offset_x, self.y + offset_y, self.width, self.height))
        else:
            screen.blit(self.sprite, (self.x, self.y))



