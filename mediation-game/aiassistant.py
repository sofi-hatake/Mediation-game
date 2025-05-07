import random
import pygame
from aicharacter import *

class AIAssistant(AICharacter):
    def generate(self):
        self.gender = "асистент"
        self.age = random.randint(10, 65)
        if self.gender == "асистент":
            self.name = random.choice(("Ґандальф", "Олорін", "Мітрандір", "Таркун", "Буревісник", "Інканус"))
        else:
            self.name = random.choice(female_names)
        self.description = "Ти віртуальний помічник гри з основ медіації. Суть гри полягає в тому, що гравець має владнати конфлікт між віртуальними персонажами. У кожного персонажа два головних показники: рівень довіри і рівень готовності до компромісу. Вони можуть змінюватися в залежності від дій гравця."
        self.manner_of_speech = "Ти говориш доброзичливо, намагаєшся допогти гравцеві зрозуміти правила гри."
    def get_prompt(self):
        return "Ти персонаж рольової гри." + \
            "Ім'я: " + self.name + \
            ". Вік: " + str(self.age) + \
            ". Гендер: " + self.gender + \
            ". Особистість: " + self.description + \
            " Манера говорити: " + self.manner_of_speech

    #змінити рівень довіри
    def change_trust(self, trust):
        self.trust = 0 #щоб не рахувалося в загальну статистику
    #змінити готовність до компромісу
    def change_consent(self, consent):
        self.consent = 0

    #малювання персонажа
    def draw(self, screen, offset_x, offset_y):
        if self.tile=="":
            pygame.draw.rect(screen, self.color, (self.x+offset_x, self.y+offset_y, self.width, self.height))
        else:
            screen.blit(self.sprite, (self.x+offset_x, self.y+offset_y))

        pygame.draw.ellipse(screen, (255, 255, 255), (self.x + 8 + offset_x, self.y + offset_y - 22, 20, 20,))
        pygame.draw.rect(screen, (100,100, 255), (self.x + self.width/2 - 1 + offset_x, self.y + offset_y - 20, 2, 10, ))
        pygame.draw.ellipse(screen, (100, 100, 255), (self.x + self.width/2 - 2 + offset_x, self.y + offset_y - 8, 4, 4, ))