import pygame, pygame.mixer
import csv, sys, random, math
import Data.engine
import Data.text
import Data.pathfind
import Data.levelRenderer as levelRenderer

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((900, 600), pygame.RESIZABLE + pygame.SCALED + pygame.HWSURFACE + pygame.DOUBLEBUF)
display = pygame.Surface((450, 300))
pygame.display.set_caption('''Sorcer's Dungeon''')
icon = pygame.image.load('Data/Images/icon.png').convert_alpha()
pygame.display.set_icon(icon)
tile_size = 32

def load_level(surface, level_number):
    data = []
    with open('Data/levels/level_' + str(level_number) + '.csv') as level_file:
        reader = csv.reader(level_file, delimiter = ',')
        for x, layer in enumerate(reader):
            for y in enumerate(layer):
                data.append([x, y])
    return data

# Defining stuff
clock = pygame.time.Clock()
fps = 21
level = 1
new_level = True
debug = False
wait = False
true_scroll = [0 ,0]
scroll = [0, 0]
screen_shake = 0
render_offset = [0, 0]
spawners = []
sorcers_list = []
witches = []
archers = []
archer_towers = []
witch_huts = []
spells = []
witch_potions = []
archer_arrows = []
particles = []
tile_list = []
pathfind_tiles = []
pathfind_nodes = []
player_health = 100
player_poison = 0
player = Data.engine.Player(150, 500)
sorcers = Data.engine.Sorcer()
spawner = Data.engine.Spawner()
archer_tower = Data.engine.ArcherTower()
witch_hut = Data.engine.WitchHut()
particle_system = Data.engine.Particles()
pathfinder = Data.pathfind.Pathfinder()


large_text = Data.text.Font('Data/Images/text/large_font.png')
small_text = Data.text.Font('Data/Images/text/small_font.png')

glass_break_sound = pygame.mixer.Sound('Data/SFX/bm-glass-break.wav')
arrow_shot_sound = pygame.mixer.Sound('Data/SFX/regular-arrow-shot.wav')

# 277000
adventure_track = pygame.mixer.Sound('Data/SFX/SoundTrack/Adventure-320bit.mp3')
adventure_track.set_volume(0.75)
adventure_track.play(-1)

play_button_images = [pygame.image.load('Data/Images/Buttons/play1.png').convert_alpha(), pygame.image.load('Data/Images/Buttons/play2.png').convert_alpha()]
setting_button_images = [pygame.image.load('Data/Images/Buttons/settings1.png').convert_alpha(), pygame.image.load('Data/Images/Buttons/settings2.png').convert_alpha()]
credit_button_images = [pygame.image.load('Data/Images/Buttons/credits1.png').convert_alpha(), pygame.image.load('Data/Images/Buttons/credits2.png').convert_alpha()]
exit_button_images = [pygame.image.load('Data/Images/Buttons/exit1.png').convert_alpha(), pygame.image.load('Data/Images/Buttons/exit2.png').convert_alpha()]
question_button_images = [pygame.image.load('Data/Images/Buttons/?_button1.png').convert_alpha(), pygame.image.load('Data/Images/Buttons/?_button2.png').convert_alpha()]
play_button = play_button_images[0].get_rect()
setting_button = setting_button_images[0].get_rect()
credit_button = credit_button_images[0].get_rect()
exit_button = exit_button_images[0].get_rect()
question_button = question_button_images[0].get_rect()

next_level_image = pygame.image.load('Data/Images/next_level_icon.png').convert_alpha()
next_level_indicator = False

splash_screen_start = pygame.time.get_ticks()
running = True
game_state = {'game_running':False, 'main_menu':False, 'settings':False, 'splash_screen':True, 'credits':False, 'question':False, 'game over':False}
while running:
    display.fill((0, 5, 10))
    if game_state['game_running']:
        next_level_indicator = False
        if len(sorcers_list) <= 0 and len(spawners) <= 0:
            if level < 3:
                next_level_indicator = True
                if pygame.mouse.get_pressed()[2]:
                    level += 1
                    player_health = 100
                    player.movement  = [0, 0]
                    player.x = 250
                    player.y = 500
                    scroll = [100, 0]
                    new_level = True
        elif player_health <= 0:
            game_state['game_running'] = False
            game_state['game over'] = True

        true_scroll[0] += (player.rect.x - true_scroll[0] - 250)/8
        true_scroll[1] += (player.rect.y - true_scroll[1] - 150)/8
        scroll[0] = int(true_scroll[0])
        scroll[1] = int(true_scroll[1])
        if scroll[1] >= 1400:
            player.y = -200
            scroll[1] = (player.rect.y - 150)/3

        # Map Stuff
        if new_level:
            sorcers_list.clear()
            spawners.clear()
            archer_towers.clear()
            archers.clear()
            witch_huts.clear()
            witches.clear()
            level_map = load_level(screen, level)
        tile_list.clear()
        pathfind_tiles.clear()
        tile_list = levelRenderer.renderLevel(display, level_map, tile_list, pathfind_tiles, spawners, archer_tower, archer_towers, archers, witch_hut, witch_huts, witches, new_level, scroll)
        new_level = False

        # Player Stuff
        player.move_player(tile_list, scroll)
        player.render(display, scroll, player_health, player_poison)
        player.inventory(scroll, sorcers_list, archer_towers, archers, witch_huts, witches, display)
        if player_poison:
            player_poison -= 1
            if random.randint(0, 1):
                player_health -= 0.15

        small_text.render(display, 'Health: ' + str(round(player_health)) + '''/100''', (8, 16))
        small_text.render(display, 'fps: ' + str(int(clock.get_fps())), (400, 16))
        small_text.render(display, str(round(pygame.time.get_ticks()/1000)), (400, 30))

        # Sorcers
        sorcers.main(tile_list, [player.rect.x, player.rect.y], scroll, sorcers_list, spells, display, particle_system, particles)
        for spell in spells:
            if spell[0] - scroll[0] >= -64 and spell[0] - scroll[0] <= 964 and spell[1] - scroll[1] >= -64 and spell[1] - scroll[1] <= 664:
                pygame.draw.circle(display, (0, 70, 70), (spell[0] - scroll[0], spell[1] - scroll[1]), 5)
            spell_rect = pygame.Rect(spell[0] - 5, spell[1] - 5, 10, 10)
            spell[0] += 18 * spell[2]
            if spell[0] > 1500 or spell[0] < -1500:
                try:
                    spells.remove(spell)
                except ValueError:
                    pass
            if spell_rect.colliderect(player.hit_box):
                player_health -= 5
                screen_shake = 15
                for i in range(2):
                    particle_system.add_particle(spell[0], spell[1], 3, [random.randint(-5, 5), random.randint(-5, 5)], (41, 63, 83), particles)
                    particle_system.add_particle(spell[0], spell[1], 3, [random.randint(-5, 5), random.randint(-5, 5)], (60, 90, 117), particles)
                    particle_system.add_particle(spell[0], spell[1], 3, [random.randint(-5, 5), random.randint(-5, 5)], (70, 106, 168), particles)
                try:
                    spells.remove(spell)
                except ValueError:
                    pass

        # Archer Towers
        archer_tower.archers(display, scroll, archers, archer_arrows, archer_towers, [player.rect.centerx, player.rect.centery], particle_system, particles, tile_list)
        archer_tower.towers(display, scroll, debug, archer_arrows, archer_towers, archers, [player.rect.x, player.rect.y], particle_system, particles)
        for arrow in archer_arrows:
            arrow_x, arrow_y, arrow_movement, arrow_img = arrow
            if arrow_x > 1500 or arrow_x < -500 or arrow_y > 1700 or arrow_y < -500:
                archer_arrows.remove(arrow)
            if pygame.Rect(arrow_x, arrow_y, 6, 1).colliderect(player.hit_box):
                try:
                    archer_arrows.remove(arrow)
                except ValueError:
                    pass
                screen_shake = 15
                if player.x > arrow_x:
                    player.x += 10
                else:
                    player.x -= 10
                for i in range(2):
                    particle_system.add_particle(arrow_x, arrow_y, 3, [random.randint(-5, 5), random.randint(-5, 5)], (41, 63, 83), particles)
                    particle_system.add_particle(arrow_x, arrow_y, 3, [random.randint(-5, 5), random.randint(-5, 5)], (60, 90, 117), particles)
                    particle_system.add_particle(arrow_x, arrow_y, 3, [random.randint(-5, 5), random.randint(-5, 5)], (70, 106, 168), particles)
                player_health -= 1
            arrow_x += (arrow_movement[0]//30)
            arrow_y += (arrow_movement[1]//30)
            arrow[0], arrow[1] = arrow_x, arrow_y
            arrow_angle = -math.degrees(math.atan2(arrow_movement[1], arrow_movement[0]))
            final_arrow_img = pygame.transform.scale(arrow_img, (12, 2))
            final_arrow_img = pygame.transform.rotate(final_arrow_img, arrow_angle)
            display.blit(final_arrow_img, (arrow_x - scroll[0], arrow_y - scroll[1], 12, 2))
            if arrow_movement[0] > 0:
                arrow_movement[0] -= 0.5
            elif arrow_movement[0] < 0:
                arrow_movement[0] += 0.5
            arrow_movement[1] += 0.5
            arrow[2] = [arrow_movement[0], arrow_movement[1]]

        # Witch Huts
        witch_hut.witches(display, scroll, witch_huts, witches, [player.rect.x + 12, player.rect.y + 17], witch_potions, particle_system, particles, tile_list)
        witch_hut.huts(display, scroll, witch_huts, particle_system, particles)
        for potion in witch_potions:
            potion_x, potion_y, potion_movement, potion_image, potion_type = potion
            potion_rect = pygame.Rect(potion_x, potion_y, 5, 7)
            for tile in tile_list:
                if tile.colliderect(potion_rect):
                    witch_potions.remove(potion)
                    glass_break_sound.set_volume(0.5)
                    glass_break_sound.play()
                    if potion_type == 'poison':
                        potion_radius = pygame.Rect(potion_rect.x - 50, potion_rect.y - 50, 100, 100)
                        for i in range(13):
                            particle_system.add_particle(potion_x, potion_y, 3, [random.randint(-5, 5), random.randint(-5, 5)], (43, 170, 30), particles)
                            particle_system.add_particle(potion_x, potion_y, 3, [random.randint(-5, 5), random.randint(-5, 5)], (35, 117, 17), particles)
                            particle_system.add_particle(potion_x, potion_y, 3, [random.randint(-5, 5), random.randint(-5, 5)], (40, 128, 30), particles)
                        if potion_radius.colliderect(player.rect):
                            player_poison += random.randint(125, 225)
                    break
            potion_x += potion_movement[0]//20
            potion_y += potion_movement[1]//20
            if potion_movement[0] > 0:
                potion_movement[0] += -2
            elif potion_movement[0] < 0 :
                potion_movement[0] += 2
            potion_movement[1] += 2
            potion[0] = potion_x
            potion[1] = potion_y
            potion_rect = pygame.Rect(potion_x, potion_y, 5, 7)
            display.blit(potion_image, (potion_rect.x - scroll[0], potion_rect.y - scroll[1], potion_rect.width, potion_rect.height))
            if potion_x > 1700 or potion_x < -2000 or potion_y > 2000 or potion_y < -500:
                witch_potions.remove(potion)

        # Spawners
        spawner.main(display, spawners, scroll, particle_system, particles, [player.rect.x, player.rect.y], sorcers, sorcers_list)

        # Particles
        particle_system.main(display, scroll, particles)

        #   Debug Interface
        if debug:
            for x in range(51):
                pygame.draw.line(display, (55,55,55), (x*32 - scroll[0], 0 - scroll[1]), (x*32- scroll[0], 12400- scroll[1]), 1)
            for y in range(50):
                pygame.draw.line(display, (55, 55,55), (0 - scroll[0], y*32 - scroll[1]), (1600 - scroll[0], y*32 - scroll[1]), 1)

    if game_state['splash_screen']:
        display.fill((255, 255, 255))
        display.blit(pygame.image.load('Data/Images/splash_screen.png'), (0, 0, 450, 300))
        if pygame.time.get_ticks() - splash_screen_start >= 1000:
            game_state['splash_screen'] = False
            game_state['main_menu'] = True

    if game_state['main_menu']:
        display.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        play_button.x = 293
        play_button.y = 85
        setting_button.x = 258
        setting_button.y = 143
        credit_button.x = 273
        credit_button.y = 199
        exit_button.x = 4
        exit_button.y = 264
        question_button.x = 46
        question_button.y = 260
        play_button_image_current = play_button_images[0]
        setting_button_image_current = setting_button_images[0]
        credit_button_image_current = credit_button_images[0]
        exit_button_image = exit_button_images[0]
        question_button_image = question_button_images[0]
        if play_button.collidepoint((mx/2, my/2)):
            play_button_image_current = play_button_images[1]
            if pygame.mouse.get_pressed()[0]:
                pygame.time.wait(100)
                game_state['game_running'] = True
                game_state['main_menu'] = False
        if setting_button.collidepoint((mx/2, my/2)):
            setting_button_image_current = setting_button_images[1]
            if pygame.mouse.get_pressed()[0]:
                pygame.time.wait(100)
                game_state['main_menu'] = False
                game_state['settings'] = True
        if credit_button.collidepoint((mx/2, my/2)):
            credit_button_image_current = credit_button_images[1]
            if pygame.mouse.get_pressed()[0]:
                pygame.time.wait(100)
                game_state['main_menu'] = False
                game_state['credits'] = True
        if exit_button.collidepoint((mx/2, my/2)):
            exit_button_image = exit_button_images[1]
            if pygame.mouse.get_pressed()[0]:
                running = False
        if question_button.collidepoint((mx/2, my/2)):
            question_button_image = question_button_images[1]
            if pygame.mouse.get_pressed()[0]:
                game_state['main_menu'] = False
                game_state['question'] = True
        display.blit(pygame.image.load('Data/Images/main_menu.png'), (0, 0, 450, 300))
        display.blit(play_button_image_current, play_button)
        display.blit(setting_button_image_current, setting_button)
        display.blit(credit_button_image_current, credit_button)
        display.blit(exit_button_image, exit_button)
        display.blit(question_button_image, question_button)

    if game_state['settings']:
        display.fill((0, 150, 150))

    if game_state['credits']:
        display.fill((50, 100, 150))
        mx, my = pygame.mouse.get_pos()
        exit_button.x = 4
        exit_button.y = 264
        exit_button_image = exit_button_images[0]
        if exit_button.collidepoint((mx/2, my/2)):
            exit_button_image = exit_button_images[1]
            if pygame.mouse.get_pressed()[0]:
                pygame.time.wait(100)
                game_state['credits'] = False
                game_state['main_menu'] = True
        display.blit(pygame.image.load('Data/Images/credits.png').convert_alpha(), (0, 0, 450, 300))
        display.blit(exit_button_image, exit_button)

    if game_state['question']:
        display.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        exit_button.x = 4
        exit_button.y = 264
        exit_button_image = exit_button_images[0]
        if exit_button.collidepoint((mx/2, my/2)):
            exit_button_image = exit_button_images[1]
            if pygame.mouse.get_pressed()[0]:
                pygame.time.wait(100)
                game_state['question'] = False
                game_state['main_menu'] = True
        display.blit(pygame.image.load('Data/Images/how_to_play.png'), (0, 0, 450, 300))
        display.blit(exit_button_image, exit_button)

    if game_state['game over']:
        display.fill((0, 0, 0))
        print('hi')
        if pygame.mouse.get_pressed()[2]:
            player_health = 100
            player.x = 150
            player.y = 400
            particles = []
            new_level = True
            game_state['game_running'] = True
            game_state['game over'] = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.right = True
                player.moving = True
            if event.key == pygame.K_a:
                player.left = True
                player.moving = True
            if event.key == pygame.K_SPACE:
                player.jumping = True
            if event.key == pygame.K_h:
                running = False
            if event.key == pygame.K_TAB:
                if player.selection <= 0:
                    player.selection += 1
                else:
                    player.selection = 0
            if event.key == pygame.K_RETURN:
                level = 1
                player_health = 100
                player.x = 150
                player.y = 400
                sorcers_list = []
                spells = []
                particles = []
                new_level = True
                game_state['game_running'] = True
            if event.key == pygame.K_b:
                if debug:
                    debug = False
                elif not debug:
                    debug = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.right = False
                player.left = False
                player.moving = False
            if event.key == pygame.K_a:
                player.right = False
                player.left = False
                player.moving = False

    if next_level_indicator:
        display.blit(next_level_image, (225 - 48, 10, 64, 9))

    if screen_shake > 0:
        screen_shake -= 1
    render_offset = [0, 0]
    if screen_shake:
        render_offset[0] = random.randint(-10, 10)
        render_offset[1] = random.randint(-10, 10)
    surf = pygame.transform.scale(display, (900, 600))
    screen.blit(surf, render_offset)
    pygame.display.update()
    clock.tick(fps)
