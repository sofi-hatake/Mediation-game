import pygame
def show_start_screen():
    clock = pygame.time.Clock()

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mediation Game")

    bg = pygame.image.load('images/bg5.png')
    walk_right = [
        pygame.image.load('images/player_right/girl_right4.png'),
        pygame.image.load('images/player_right/girl_right5.png'),
        pygame.image.load('images/player_right/girl_right6.png'),
    ]

    sound = pygame.image.load('images/sound.png')
    start_game = pygame.image.load('images/start.png')
    sound_rect = sound.get_rect(topright=(70, 20))
    start_rect = start_game.get_rect(center=(400, 250))

    player_anim_count = 0
    bg_x = 0

    bg_sound = pygame.mixer.Sound('sounds/bg1.mp3')
    music_playing = False

    running = True
    while running:

        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 800, 0))
        screen.blit(walk_right[player_anim_count], (250, 500))

        screen.blit(sound, sound_rect)
        screen.blit(start_game, start_rect)

        if player_anim_count == 2:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -800:
            bg_x = 0

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    bg_sound.stop()
                    return
                if sound_rect.collidepoint(event.pos):
                    if not music_playing:
                        bg_sound.play(-1)
                        music_playing = True
                    else:
                        bg_sound.stop()
                        music_playing = False


        clock.tick(7)