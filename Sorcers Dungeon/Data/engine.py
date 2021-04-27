import pygame, pygame.mixer, math, random
from pygame.locals import *

pygame.init()
pygame.mixer.init()

def load_image(path):
    img = pygame.image.load('Data/Images/' + str(path)).convert_alpha()
    img_rect = img.get_rect()
    return img, img_rect

def load_image_list(path, list, amount):
    for x in range(1, amount+1):
        img = pygame.image.load(str(path) + str(x) + '.png').convert_alpha()
        list.append(img)

def return_hit_list(obj, collision_objs):
    hit_list = []
    for collision_obj in collision_objs:
        if collision_obj.colliderect(obj):
            hit_list.append(collision_obj)
    return hit_list

class Player(object):
    def __init__(self, x, y):
        self.right = False
        self.left = False
        self.move_right_possible = True
        self.move_left_possible = True
        self.speed = 15
        self.image = pygame.image.load('Data/Images/Player/player_idle.png').convert_alpha()
        self.sword_image, self.sword_rect = load_image('Sword/sword.png')
        self.bow_image, self.bow_rect = load_image('bow.png')
        self.arrow_image, self.arrow_rect = load_image('arrow.png')
        self.x = x
        self.y = y
        self.orig_y = 0
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.movement = [0,0]
        self.acceleration = [0, 0]
        self.moving = False
        self.last_direction = ''
        self.gravity = 10
        self.jumping = False
        self.airtimer = 0
        self.dy = 0
        self.collisions = {'right':False, 'left':False, 'bottom':False, 'top':False}
        self.dead = False
        self.hit_area = pygame.Rect(self.x + 32, self.y - 32, 64, 64)
        self.hit_box = pygame.Rect(self.x - 8, self.y - 8, 16, 16)
        self.animate_sword = False
        self.sword_counter = 0
        self.sword_sound = pygame.mixer.Sound('Data/SFX/sword-sound-2.wav')
        self.sword_sound_timer = pygame.time.get_ticks()
        self.selection = 0
        self.arrows = []
        self.arrow_counter = 0
        self.load_images()

    def move_player(self, tiles, scroll):
        self.collisions['right'] = False
        self.collisions['left'] = False
        self.collisions['top'] = False
        self.collisions['bottom'] = False
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        for tile in hit_list:
            if tile.collidepoint(self.rect.midright):
                self.collisions['right'] = True
            if tile.collidepoint(self.rect.midleft):
                self.collisions['left'] = True
        if self.right and self.collisions['right'] == False:
            self.movement[0] = 1
        elif self.left and self.collisions['left'] == False:
            self.movement[0] = -1
        else:
            self.movement[0] = 0
        self.x += self.speed * self.movement[0]
        for tile in hit_list:
            if tile.collidepoint(self.rect.midbottom):
                self.collisions['bottom'] = True
                self.dy = 0
            if tile.collidepoint(self.rect.midtop):
                self.collisions['top'] = True
        if self.collisions['bottom'] == False:
            self.movement[1] = 1
            self.acceleration[1] += 0.1
        else:
            self.movement[1] = 0
            self.acceleration[1] = 0
        if self.collisions['top'] == False and self.jumping and self.dy < 30:
            self.movement[1] = -1
            self.dy += 2
        elif self.dy >= 30:
            self.jumping = False
            self.movement[1] = 1
        self.y += self.gravity * self.movement[1] + self.acceleration[1]
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.hit_area = [self.x  - 16, self.y - 16, 64, 64]
        self.hit_box = pygame.Rect(self.x + 8, self.y + 12, 16, 16)

    def inventory(self, scroll, sorcers, archer_towers, archers, witch_huts, witches, surface):
        if self.selection == 0:
            self.sword(scroll, sorcers, archer_towers, archers, witch_huts, witches, surface)
        elif self.selection == 1:
            self.bow(scroll, surface)
        elif self.selection == 2:
            pass
            # Spell shooter
        elif self.selection == 3:
            pass
        elif self.selection == 4:
            pass
        elif self.selection == 5:
            pass
        elif self.selection == 6:
            pass
        self.arrow(surface, scroll, sorcers, archer_towers, archers, witch_huts, witches)

    def sword(self, scroll, sorcers, archer_towers, archers, witch_huts, witches, surface):
        mx, my = pygame.mouse.get_pos()
        if mx < self.rect.x:
            sword_pos = [self.rect.x - scroll[0], self.rect.y + 10 - scroll[1]]
        elif mx >= self.rect.x:
            sword_pos = [self.rect.x + 16 - scroll[0], self.rect.y + 10 - scroll[1]]
        oppisite = abs(my - sword_pos[1])
        adjacent = abs(mx - sword_pos[0])
        try:
            final_angle = -math.degrees(math.atan2(oppisite, adjacent))
        except ZeroDivisionError:
            pass
        self.final_sword_image = pygame.transform.rotate(self.sword_image, final_angle)
        self.final_sword_rect = pygame.Rect(sword_pos[0], sword_pos[1], self.final_sword_image.get_width(), self.final_sword_image.get_height())
        hit_rect = pygame.Rect(self.hit_area[0], self.hit_area[1], self.hit_area[2], self.hit_area[3])
        if pygame.mouse.get_pressed()[0] == 1:
            self.animate_sword = True
            if pygame.time.get_ticks() - self.sword_sound_timer >= 100:
                self.sword_sound.set_volume(0.3)
                self.sword_sound.play()
                self.sword_sound_timer = pygame.time.get_ticks()
            for sorcer in sorcers:
                sorcer_rect = pygame.Rect(sorcer[0], sorcer[1], sorcer[2], sorcer[3])
                if sorcer_rect.colliderect(hit_rect):
                    sorcer[4] = 0
            for archer_tower in archer_towers:
                archer_tower_rect = pygame.Rect(archer_tower[0], archer_tower[1], 32, 65)
                if archer_tower_rect.colliderect(hit_rect):
                    archer_tower[2] -= 2
            for archer in archers:
                if archer[4] == False:
                    archer_rect = pygame.Rect(archer[0], archer[1], 11, 13)
                    if archer_rect.colliderect(hit_rect):
                        archer[2] -= 1
            for witch_hut in witch_huts:
                witch_hut_rect = pygame.Rect(witch_hut[0], witch_hut[1], 39, 32)
                if witch_hut_rect.colliderect(hit_rect):
                    witch_hut[2] -= 2
            for witch in witches:
                if not witch[4]:
                    witch_rect = pygame.Rect(witch[0], witch[1], 11, 13)
                    if witch_rect.colliderect(hit_rect):
                        witch[2] -= 1

        if self.animate_sword:
            if self.sword_counter <= 10:
                self.sword_image = self.sword_list[self.sword_counter]
                self.sword_counter += 1
            else:
                self.animate_sword = False
                self.sword_counter = 0
                # self.sword_image, self.sword_rect = load_image('Sword/sword.png')
        surface.blit(self.final_sword_image, self.final_sword_rect)

    def bow(self, scroll, surface):
        mx, my = pygame.mouse.get_pos()
        if mx < self.rect.x:
            bow_pos = [self.rect.x - scroll[0], self.rect.y + 10 - scroll[1]]
        elif mx >= self.rect.x:
            bow_pos = [self.rect.x + 16 - scroll[0], self.rect.y + 10 - scroll[1]]
        oppisite = my - bow_pos[1]
        adjacent = mx - bow_pos[0]
        try:
            final_angle = -math.degrees(math.atan2(oppisite, adjacent))
        except ZeroDivisionError:
            pass

        if pygame.mouse.get_pressed()[0]:
            arrow = [[self.rect.x + 8,self.rect.y + 10], [adjacent, oppisite]]
            self.arrows.append(arrow)

        final_bow_image = pygame.transform.rotate(self.bow_image, final_angle)
        final_bow_rect = pygame.Rect(bow_pos[0], bow_pos[1], final_bow_image.get_width(), final_bow_image.get_height())
        surface.blit(final_bow_image, final_bow_rect)

    def arrow(self, surface, scroll, sorcers, archer_towers, archers, witch_huts, witches):
        for arrow in self.arrows:
            arrow_rect = pygame.Rect(arrow[0][0], arrow[0][1], 6, 1)
            try:
                arrow_angle = int(-math.degrees(math.atan2(arrow[1][0], arrow[1][1])))
            except ZeroDivisionError:
                pass
            arrow[0][0] += arrow[1][0]//30
            arrow[0][1] += arrow[1][1]//30
            arrow_image = pygame.transform.rotate(self.arrow_image, arrow_angle)
            surface.blit(arrow_image, (arrow_rect.x - scroll[0], arrow_rect.y - scroll[1], arrow_rect.width, arrow_rect.height))


    def load_images(self):
        self.sword_list = []
        load_image_list('Data/Images/Sword/attack', self.sword_list, 11)

    def render(self, surface, scroll, health, poison):
        true_mx, true_my = pygame.mouse.get_pos()
        mx = true_mx + scroll[0] - 225
        my = true_my - scroll[1] - 150
        if mx < self.x:
            flipped_image = pygame.transform.rotate(self.image, 180)
            final_image = pygame.transform.flip(flipped_image, False, True)
        if mx > self.x:
            final_image = pygame.transform.rotate(self.image, 0)
        if mx == self.x:
            final_image = self.image
        surface.blit(final_image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))
        health_bar = pygame.Rect(5, 15, health, 10)
        if poison:
            pygame.draw.rect(surface, (0, 125 ,0), health_bar)
        else:
            pygame.draw.rect(surface, (125, 0 ,0), health_bar)
        # pygame.draw.rect(surface, (0, 70, 100), (self.hit_box.x - scroll[0], self.hit_box.y - scroll[1], 16, 16), 2)

class ArcherTower(object):
    def __init__(self):
        self.tower_image = pygame.image.load('Data/Images/Archer_Tower/tower.png').convert_alpha()
        self.archer_image = pygame.image.load('Data/Images/Archer_Tower/archer.png').convert_alpha()
        self.bow_image = pygame.image.load('Data/Images/Archer_Tower/bow.png').convert_alpha()
        self.arrow_image = pygame.image.load('Data/Images/Archer_Tower/arrow.png').convert_alpha()
        self.archer_counter = 0
        self.arrow_sound = pygame.mixer.Sound('Data/SFX/regular-arrow-shot.wav')

    def create_tower(self, x, y, towers, archers):
        self.archer_counter += 1
        towers.append([x, y, 100, '#' + str(self.archer_counter)])
        archers.append([x + 12, y + 7, 5, '#' + str(self.archer_counter), True, pygame.time.get_ticks()])

    def towers(self, surface, scroll, debug, arrows, towers, archers, knight_pos, particle_system, particles):
        for tower in towers:
            tower_x, tower_y, tower_health, tower_id = tower
            tower_rect = pygame.Rect(tower_x, tower_y, 32, 65)
            if tower_health <= 0:
                towers.remove(tower)
                for i in range(17):
                    particle_system.add_particle(tower_rect.centerx, tower_rect.centery, 3, [random.randint(-5, 5), random.randint(-5, 5)], (85, 68, 53), particles)
                    particle_system.add_particle(tower_rect.centerx, tower_rect.centery, 3, [random.randint(-5, 5), random.randint(-5, 5)], (50, 40, 32), particles)
                    particle_system.add_particle(tower_rect.centerx, tower_rect.centery, 3, [random.randint(-5, 5), random.randint(-5, 5)], (71, 57, 45), particles)
            else:
                health_bar = pygame.Rect(tower_x - scroll[0], tower_y - 10 - scroll[1], tower_health * 0.32, 4)
                surface.blit(self.tower_image, (tower_x - scroll[0], tower_y - scroll[1], 32, 65))
                pygame.draw.rect(surface, (85, 68, 53), health_bar)

    def archers(self, surface, scroll, archers, archer_arrows, towers, knight_pos, particle_system, particles, tile_list):
        for archer in archers:
            archer_x, archer_y, archer_health, archer_id, archer_parent, shoot_timer = archer
            archer_rect = pygame.Rect(archer_x, archer_y, 10, 10)
            knight_dis = [knight_pos[0] - archer_x, knight_pos[1] - archer_y]
            bow_pos = [archer_x, archer_y]
            if archer_health <= 0:
                archers.remove(archer)
                for i in range(7):
                    particle_system.add_particle(archer_rect.centerx, archer_rect.centery, 3, [random.randint(-5, 5), random.randint(-5, 5)], (50, 32, 57), particles)
                    particle_system.add_particle(archer_rect.centerx, archer_rect.centery, 3, [random.randint(-5, 5), random.randint(-5, 5)], (37, 26, 42), particles)
                    particle_system.add_particle(archer_rect.centerx, archer_rect.centery, 3, [random.randint(-5, 5), random.randint(-5, 5)], (43, 28, 50), particles)
            else:
                if len(towers) > 0:
                    for tower in towers:
                        tower_x, tower_y, tower_health, tower_id = tower
                        if archer_id == tower_id:
                            archer_parent = True
                            break
                        if archer_id != tower_id:
                            archer_parent = False
                else:
                    archer_parent = False
                archer[4] = archer_parent
                archer_falling = False
                archer_movement = [0, 0]
                if archer_parent:
                    archer_falling = False
                elif not archer_parent:
                    archer_falling = True
                hit_list = return_hit_list(archer_rect, tile_list)
                for tile in hit_list:
                    if tile.collidepoint(archer_rect.midbottom):
                        archer_falling = False
                if archer_falling:
                    archer_movement[1] = 1
                archer_y = 10 * archer_movement[1] + archer_y
                archer[1] = archer_y

                bow_adj = knight_pos[0] - archer_x
                bow_opp = knight_pos[1] - archer_y
                try:
                    final_angle = math.degrees(bow_opp/bow_adj)
                except ZeroDivisionError:
                    final_angle = 0
                bow_rect = pygame.Rect(archer_x - 5, archer_y + 3, 2, 7)
                if pygame.time.get_ticks() - shoot_timer >= random.randint(3000, 5000):
                    self.arrow_sound.set_volume(0.3)
                    self.arrow_sound.play()
                    archer[5] = pygame.time.get_ticks()
                    archer_arrows.append([bow_rect.centerx, bow_rect.centery, [int(bow_adj), int(bow_opp)], self.arrow_image])
                archer_rect = pygame.Rect(archer_x, archer_y, 10, 10)
                final_bow_img = pygame.transform.rotate(self.bow_image, final_angle)
                surface.blit(final_bow_img, (bow_rect.x - scroll[0], bow_rect.y - scroll[1], bow_rect.width, bow_rect.height))
                surface.blit(self.archer_image, (archer_rect.x - scroll[0], archer_rect.y - scroll[1], 11, 13))
                if archer_parent == False:
                    pygame.draw.rect(surface, (50, 32, 57), (archer_x - scroll[0], archer_y - 5 - scroll[1], archer_health * 2.2, 2))

class WitchHut(object):
    def __init__(self):
        self.hut_image = pygame.image.load('Data/Images/Witch Hut/witch_hut.png').convert_alpha()
        self.witch_image = pygame.image.load('Data/Images/Witch Hut/witch.png').convert_alpha()
        self.splash_potion_poison_image = pygame.image.load('Data/Images/Potions/splash_potion_poison.png').convert_alpha()
        self.counter = 0

    def create_hut(self, x, y, witch_huts, witches):
        self.counter += 1
        witch_huts.append([x, y, 100, '#' + str(self.counter)])
        witches.append([x + 17, y + 5, 20, '#' + str(self.counter), True, pygame.time.get_ticks()])

    def huts(self, display, scroll, witch_huts, particle_system, particles):
        for hut in witch_huts:
            hut_x, hut_y, hut_health, hut_id = hut
            if hut_health <= 0:
                witch_huts.remove(hut)
            else:
                hut_rect = pygame.Rect(hut_x, hut_y, 39, 32)
                hut_health_bar = pygame.Rect(hut_x + 8, hut_y - 5, hut_health * 31/100, 3)
                display.blit(self.hut_image, (hut_rect.x - scroll[0], hut_rect.y - scroll[1], hut_rect.width, hut_rect.height))
                pygame.draw.rect(display, (85, 68, 53), (hut_health_bar.x - scroll[0], hut_health_bar.y - scroll[1], hut_health_bar.width, hut_health_bar.height))

    def witches(self, display, scroll, witch_huts, witches, player_pos, witch_potions, particle_system, particles, tiles):
        for witch in witches:
            witch_x, witch_y, witch_health, witch_id, witch_parent, splash_potion_timer = witch
            witch_falling = False
            if witch_health <= 0:
                witches.remove(witch)
            else:
                witch_rect = pygame.Rect(witch_x, witch_y, 11, 13)
                if witch_parent == True:
                    witch_parent = False
                    for hut in witch_huts:
                        hut_x, hut_y, hut_health, hut_id = hut
                        if hut_id == witch_id:
                            witch_parent = True
                            break
                        elif hut_id != witch_id:
                            witch_parent = False
                if witch_parent == False:
                    witch_falling = True
                    for tile in tiles:
                        if tile.collidepoint(witch_rect.midbottom):
                            witch_falling = False
                if witch_falling:
                    witch_y += 1
                if pygame.time.get_ticks() - splash_potion_timer >= 3500:
                    if witch_x - scroll[0] >= -32 and witch_x - scroll[0] <= 932 and witch_y - scroll[1] <= 632 and witch_y - scroll[1] >= -32:
                        witch[5] = pygame.time.get_ticks()
                        opp = int(player_pos[1] - witch_x)
                        adj = int(player_pos[0] - witch_y)
                        witch_potions.append([witch_x, witch_y, [adj, opp], self.splash_potion_poison_image, 'poison'])
                witch_rect = pygame.Rect(witch_x, witch_y, 11, 13)
                witch_health_bar = pygame.Rect(witch_x - scroll[0], witch_y - 5 - scroll[1], witch_health * 11/20, 3)
                display.blit(self.witch_image, (witch_rect.x - scroll[0], witch_rect.y - scroll[1], witch_rect.width, witch_rect.height))
                if not witch_parent:
                    pygame.draw.rect(display, (78, 33, 55), witch_health_bar)
                witch[1] = witch_y
                witch[4] = witch_parent

class Sorcer(object):
    def __init__(self):
        self.sorcer_image, self.rect = load_image('Sorcer/sorcer_idle.png')
        self.sound = pygame.mixer.Sound('Data/SFX/spell-shoot.wav')
        self.sound.set_volume(0.15)

    def add_sorcer(self, x, y, sorcers):
        sorcers.append([x, y, 32, 32, 1, random.randint(1, 14), pygame.time.get_ticks()])

    def main(self, tile_list, knight_pos, scroll, sorcers, spells, surface, particle_system, particles):
        for sorcer in sorcers:
            '''Move'''
            left = False
            right = False
            up = False
            down = False
            collisions = {'right':False, 'left':False, 'bottom':False, 'top':False}
            sorcer_rect = pygame.Rect(sorcer[0], sorcer[1], 32, 32)
            sorcer_movement = [0 ,0]
            for tile in tile_list:
                if tile.collidepoint(sorcer_rect.midright):
                    collisions['right'] = True
                if tile.collidepoint(sorcer_rect.midleft):
                    collisions['left'] = True
                if tile.collidepoint(sorcer_rect.midbottom):
                    collisions['bottom'] = True
                if tile.collidepoint(sorcer_rect.midtop):
                    collisions['top'] = True
            knight_disx = (knight_pos[0] - scroll[0]) - (sorcer_rect.x - scroll[0])
            knight_disy = (knight_pos[1] - scroll[1]) - (sorcer_rect.y - scroll[1])
            if knight_pos[0] < sorcer_rect.x:
                left = True
            if knight_pos[0] > sorcer_rect.x:
                right = True
            if knight_pos[1] > sorcer_rect.y:
                down = True
            if knight_pos[1] < sorcer_rect.y:
                up = True
            if right and collisions['right'] == False:
                sorcer_movement[0] = 1
            elif left and collisions['left'] == False:
                sorcer_movement[0] = -1
            else:
                sorcer_movement[0] = 0
            if up and collisions['top'] == False:
                sorcer_movement[1] = -1
            elif down and collisions['bottom'] == False:
                sorcer_movement[1] = 1
            else:
                sorcer_movement[1] = 0
            sorcer[0] += sorcer_movement[0] * sorcer[5]
            sorcer[1] += sorcer_movement[1] * sorcer[5]
            sorcer_rect = pygame.Rect(sorcer[0], sorcer[1], 32, 32)
            if collisions['right'] and collisions['left'] and collisions['bottom'] and collisions['top']:
                sorcers.remove(sorcer)
            '''Shoot'''
            dt = pygame.time.get_ticks() - sorcer[6]
            sorcer_rect = pygame.Rect(sorcer[0], sorcer[1], 32, 32)
            knight_disx = (knight_pos[0] - scroll[0]) - (sorcer_rect.x - scroll[0])
            knight_disy = (knight_pos[1] - scroll[1]) - (sorcer_rect.y - scroll[1])
            if dt > 500:
                sorcer[6] = pygame.time.get_ticks()
                self.sound.play()
                if knight_disx < 300 and knight_disx > 0 and knight_disy < 50 and knight_disy > -50:
                    spells.append([sorcer_rect.x, sorcer_rect.y, 1])
                if knight_disx > -300 and knight_disx < 0 and knight_disy < 50 and knight_disy > -50:
                    spells.append([sorcer_rect.x, sorcer_rect.y, -1])
            rect = pygame.Rect(sorcer[0] - scroll[0], sorcer[1] - scroll[1], 32, 32)
            surface.blit(self.sorcer_image, rect)
            ''' Remove Sorcers'''
            for sorcer in sorcers:
                if sorcer[4] == 0:
                    for i in range(0, 4):
                        particle_system.add_particle(sorcer[0], sorcer[1], 3, [random.randint(-5, 5), random.randint(-5, 5)], (90, 83, 83), particles)
                        particle_system.add_particle(sorcer[0], sorcer[1], 3, [random.randint(-5, 5), random.randint(-5, 5)], (48, 44, 46), particles)
                        particle_system.add_particle(sorcer[0], sorcer[1], 3, [random.randint(-5, 5), random.randint(-5, 5)], (26, 26, 28), particles)
                    sorcers.remove(sorcer)
            # pygame.draw.rect(surface, (255, 255, 255), rect)

class Spawner(object):
    def __init__(self):
        self.image, self.rect = load_image('Spawner.png')

    def main(self, surface, spawners, scroll, particle_system, particles, knight_pos, sorcers_class, sorcers_list):
        for spawner in spawners:
            spawner_rect = pygame.Rect(spawner[0], spawner[1], 32, 32)
            if spawner[2] > 0:
                spawner_dt = pygame.time.get_ticks() - spawner[3]
                knight_dis = [knight_pos[0] - spawner[0], knight_pos[1] - spawner[1]]
                if spawner_dt >= random.randint(500, 1000) and knight_dis[0] < 250 and knight_dis[0] > -250 and knight_dis[1] < 250 and knight_dis[1] > -250:
                    spawner[3] = pygame.time.get_ticks()
                    spawner[2] -= 1
                    sorcers_class.add_sorcer(spawner_rect.x + 8, spawner_rect.y, sorcers_list)
                if spawner[0] - scroll[0] >= -64 and spawner[0] - scroll[0] <= 964 and spawner[1] - scroll[1] >= -64 and spawner[1] - scroll[1] <= 664:
                    surface.blit(self.image, (spawner[0] - scroll[0], spawner[1] - scroll[1], 32, 32))
                pygame.draw.rect(surface, (0, 125, 125), (spawner_rect.x - scroll[0], spawner_rect.y - 5 - scroll[1], spawner[2]*1.28, 5))
            else:
                for i in range(0, 25):
                    particle_system.add_particle(spawner_rect.centerx, spawner_rect.centery, 4, [random.randint(-7,7), random.randint(-7, 7)], (41, 63, 83), particles)
                    particle_system.add_particle(spawner_rect.centerx, spawner_rect.centery, 4, [random.randint(-7,7), random.randint(-7, 7)], (80, 103, 123), particles)
                    particle_system.add_particle(spawner_rect.centerx, spawner_rect.centery, 4, [random.randint(-7,7), random.randint(-7, 7)], (120, 143, 163), particles)
                spawners.remove(spawner)

class Particles(object):
    def __init__(self):
        pass

    def add_particle(self, x, y, radius, velocity, color, particles, decay=0.05):
        particles.append([x, y, radius, velocity, color, decay])

    def main(self, surface, scroll, particles):
        for particle in particles:
            particle[0] += particle[3][0]
            particle[1] += particle[3][1]
            particle[2] -= particle[5]
            if particle[2] <= 0:
                particles.remove(particle)
            pygame.draw.circle(surface, particle[4], (particle[0] - scroll[0], particle[1] - scroll[1]), particle[2])
