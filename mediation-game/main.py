import pygame
import sys
import pygame_gui #бібліотека інтерфейсу користувача
import google.generativeai as genai
import csv
import pygame.freetype  # бібліотека для виводу текстових написів

from aicharacter import AICharacter
from aiassistant import AIAssistant
from obstacle import Obstacle
from player import Player, Direction
from conflict import Conflict
from portrait import Portrait
from start import show_start_screen

show_start_screen()

api_key="AIzaSyBoO2T8EOjpv7bgmsuWlrR0QRYPUGdIPVU"

pygame.init()

WIDTH, HEIGHT = 800, 600 #розмір вікна
WORLD_WIDTH, WORLD_HEIGHT = 1600, 960 #розмір світу

offset_x, offset_y = 0,0 #положення камери

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #ігровий екран
pygame.display.set_caption("Mediation Game")

manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/themes/console_theme.json')
background = pygame.Surface((WIDTH, HEIGHT))
background.fill(manager.ui_theme.get_colour('dark_bg'))

#клас діалогової консолі, що ховає вікно при закритті
class MyConsoleWindow(pygame_gui.windows.UIConsoleWindow):
    def on_close_window_button_pressed(self):
        self.hide()

#вікно консолі
console_window = MyConsoleWindow(rect=pygame.rect.Rect((50, 20), (WIDTH-100, HEIGHT/2-50)),manager=manager)
console_window.set_display_title("Діалог")

bg_image = pygame.image.load('tiles/bg.png') #фон ігрового світу

player = Player() #гравець
obstacles = [] #список перешкод
#завантаження списку перешкод із CSV файлу
with open('obstacles.csv', newline='') as csvfile:
    obstacle_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in obstacle_reader:
        obstacles.append(Obstacle(int(row[0]),int(row[1]),int(row[2]),int(row[3]), str(row[4])))
characters = [] #список AI персонажів
characters.append(AICharacter(865,455,25,25, "characters/aicharacter4.png"))
characters.append(AICharacter(1130,350,24,24, "characters/aicharacter5.png"))
characters.append(AIAssistant(570,300,36,50, "characters/Gandalf.png"))
conflict = Conflict(characters[0], characters[1]) #створення конфлікту

portrait = Portrait(520,280, 400, 400)

muteButton = Obstacle(270,290, 32, 32, "tiles/sound.png")
obstacles.append(muteButton)
muted = True

current_character = None #персонаж, з яким активний діалог
model = None
chat = None

#виявлення зіткнень між об'єктами
def detect_collisions(player, game_objects):
    for obstacle in game_objects:
        if player.rect().colliderect(obstacle.rect()):
            return obstacle
    return False

#підготовка моделі
def set_context():
    genai.configure(api_key=api_key)
    MODEL = 'gemini-1.5-flash'
    SYSTEM_INSTRUCTION = current_character.get_prompt() + \
            "Суть конфлікту: " + \
            conflict.description + \
             " \nФОРМАТ УСІХ ТВОЇХ ВІДПОВІДЕЙ: три рядки, розділені символом '^'. \n1. Перший рядок - текстова відповідь твого персонажа." + \
             " \n2. Другий рядок - ціле число від -5 до 5, яке показує, чи змінилася твоя ДОВІРА до гравця." + \
             " -5 означає суттєво зменшилася, 5 означає суттєво збільшилася." + \
             " \n3. Третій рядок - ціле число від -3 до 3, яке показує, чи змінилася твоя ГОТОВНІСТЬ ДО КОМПРОМІСУ." + \
             " -3 означає суттєво зменшилася, 3 означає суттєво збільшилася."
            #"Третій рядок - рекомендація, що мав зробити співбесідник для того, щоб твоя довіра збільшилася."
    print (SYSTEM_INSTRUCTION)
    global model
    global chat
    model = genai.GenerativeModel(MODEL, system_instruction=SYSTEM_INSTRUCTION)
    chat = model.start_chat()

running = True
console_window.hide()
##GAME_FONT = pygame.freetype.SysFont(None, 16)
GAME_FONT = pygame.freetype.Font("terminus-normal.otb", 16)
pygame.mixer.music.load('retro-saloon-welcome-to-the-past-174372.mp3') #фонова музика
talk_sound = pygame.mixer.Sound("baby-talk-babble3-104858.mp3") #звук діалогу
#pygame.mixer.music.play(-1, fade_ms=2000) #запуск музики

#головний цикл гри
while running:
    time_delta = pygame.time.Clock().tick(60)/1000
    #обробка подій
    for event in pygame.event.get():
        #вихід з гри
        if event.type == pygame.QUIT:
            running = False
        #нове повідомлення в консолі
        if (event.type == pygame_gui.UI_CONSOLE_COMMAND_ENTERED and
                event.ui_element == console_window):
            command = event.command
            if current_character:
                PROMPT = "Твій рівень ДОВІРИ зараз становить " + str(current_character.trust) + " зі 100." + \
                         "Твоя ГОТОВНІСТЬ ДО КОМПРОМІСУ зараз становить " + str(current_character.consent) + " зі 100." + "Наступна репліка співбесідника: '" + command + "'"
                response = chat.send_message(PROMPT)
                print (response.text)
                if not muted:
                    talk_sound.play() #звук при відповіді
                console_window.add_output_line_to_log(response.text.split("^")[0], is_bold=True)
                try:
                    #зміна рівня довіри і готовності до діалогу
                    trust_change = int(response.text.split("^")[1])
                    current_character.change_trust(trust_change)
                    current_character.change_consent(int(response.text.split("^")[2]))
                    if trust_change>0:
                        portrait.set_emotion("positive")
                    elif trust_change<0:
                        portrait.set_emotion("negative")
                    else:
                        portrait.set_emotion("neutral")
                except:
                    pass
                console_window.set_display_title(current_character.name + \
                                " | Довіра: " + str(current_character.trust) + \
                                " | Схильність до компромісу: " + str(current_character.consent))

            if command == 'clear':
                console_window.clear_log()
        manager.process_events(event)
        ######################кінець обробника консолі

    #обробка клавіш
    keys = pygame.key.get_pressed()

    #попередня позиція гравця
    prev_x = player.x
    prev_y = player.y

    player.direction = Direction.NONE
    #рух гравця лише коли консоль невидима
    if not console_window.visible:
        pygame.mixer.music.set_volume(0.5) #зміна гучності музики
        if keys[pygame.K_LEFT]:
            player.x -= player.speed
            player.direction = Direction.LEFT
        if keys[pygame.K_RIGHT]:
            player.x += player.speed
            player.direction = Direction.RIGHT
        if keys[pygame.K_UP]:
            player.y -= player.speed
            player.direction = Direction.UP
        if keys[pygame.K_DOWN]:
            player.y += player.speed
            player.direction = Direction.DOWN

    #виявлення зіткнень з перешкодами
    collision = detect_collisions(player, obstacles)
    if collision == muteButton:
        muted = not muted
        if not muted:
            pygame.mixer.music.play(-1)  # запуск музики
        else:
            pygame.mixer.music.stop()
        prev_x = 210
        prev_y = 290
    if collision:
        player.x = prev_x
        player.y = prev_y

    #виявлення колізій з персонажами
    colliding_character = detect_collisions(player, characters)
    if colliding_character:
        pygame.mixer.music.set_volume(0.2) #зміна гучності музики
        current_character = colliding_character #встановлення поточного персонажу для діалогу
        portrait.set_gender(current_character.gender)
        set_context() #підготовка моделі
        console_window.set_display_title(current_character.name)
        console_window.clear_log() #очищення консолі
        console_window.show()
        player.x = prev_x
        player.y = prev_y

    #уникнення виходу за межі ігрового світу
    player.x = max(0, min(WORLD_WIDTH - player.width, player.x))
    player.y = max(0, min(WORLD_HEIGHT - player.height, player.y))

    #Розрахунок положення камери
    offset_x = max(WIDTH-WORLD_WIDTH, min(0, WIDTH//2 - player.x))
    offset_y = max(HEIGHT-WORLD_HEIGHT,min(0, WIDTH//2 - player.y))

    #малювання фону
    screen.fill((40, 61, 18))
    screen.blit(bg_image, (offset_x, offset_y))

    #малювання перешкод
    for o in obstacles:
        o.draw(screen, offset_x, offset_y)

    #малювання персонажів
    for c in characters:
        c.draw(screen, offset_x, offset_y)

    #малювання гравця
    player.draw(screen, offset_x, offset_y)

    if console_window.visible:
        portrait.draw(screen, offset_x, offset_y)

    total_trust = 0
    total_consent = 0
    for c in characters:
        total_trust += c.trust
        total_consent += c.consent

    text_surface, rect = GAME_FONT.render("Здобуто очок довіри: "+str(total_trust) + ";   готовності до компромісу: " + str(total_consent), (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

    pygame.display.update()
    #кінець ігрового циклу

pygame.quit()
sys.exit()
