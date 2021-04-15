import pygame, math, random

pygame.init()

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

    def inventory(self, scroll, sorcer, archer_towers, archers, surface):
        items = [['sword', [5, 30]], ['bow', [29, 30]], ['pearl', [53, 30]]]
        raw_inventory_slot_image = pygame.image.load('Data/Images/Inventory_slot.png').convert_alpha()
        inventory_slot_image = pygame.transform.scale(raw_inventory_slot_image, (24, 24))
        for item in items:
            inventory_slot_rect = pygame.Rect(item[1][0], item[1][1], 24, 24)
            surface.blit(inventory_slot_image, inventory_slot_rect)
            if item[0] == 'sword':
                raw_sword_image = pygame.image.load('Data/Images/Sword/sword.png').convert_alpha()
                sword_image = pygame.transform.rotate(raw_sword_image, -45)
                surface.blit(sword_image, (item[1][0] + 3, item[1][1] + 2, 24, 24))
            if item[0] == 'bow':
                raw_bow_image = pygame.image.load('Data/Images/bow.png').convert_alpha()
                bow_image = pygame.transform.rotate(raw_bow_image, 45)
                surface.blit(bow_image, (item[1][0] + 4, item[1][1] + 3, 24, 24))
            if item[0] == 'pearl':
                raw_pearl_image = pygame.image.load('Data/Images/pearl.png').convert_alpha()
                pearl_image = pygame.transform.scale(raw_pearl_image, (12, 12))
                surface.blit(pearl_image, (item[1][0] + 6, item[1][1] + 6, 24, 24))
        if self.selection == 0:
            self.sword(scroll, sorcer, archer_towers, archers, surface)
        elif self.selection == 1:
            self.bow(scroll, surface, sorcer)

    def sword(self, scroll, sorcers, archer_towers, archers, surface):
        mx, my = pygame.mouse.get_pos()
        if mx < self.rect.x:
            sword_pos = [self.rect.x - scroll[0], self.rect.y + 10 - scroll[1]]
        elif mx >= self.rect.x:
            sword_pos = [self.rect.x + 16 - scroll[0], self.rect.y + 10 - scroll[1]]
        oppisite = my - sword_pos[1]
        adjacent = mx - sword_pos[0]
        try:
            final_angle = -math.degrees(math.atan2(int(oppisite), int(adjacent)))
        except ZeroDivisionError:
            final_angle = -90
        self.final_sword_image = pygame.transform.rotate(self.sword_image, final_angle)
        self.final_sword_rect = pygame.Rect(sword_pos[0], sword_pos[1], self.final_sword_image.get_width(), self.final_sword_image.get_height())
        hit_rect = pygame.Rect(self.hit_area[0], self.hit_area[1], self.hit_area[2], self.hit_area[3])
        if pygame.mouse.get_pressed()[0] == 1:
            self.animate_sword = True
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
                    archer[2] -= 1

        if self.animate_sword:
            if self.sword_counter <= 10:
                self.sword_image = self.sword_list[self.sword_counter]
                self.sword_counter += 1
            else:
                self.animate_sword = False
                self.sword_counter = 0
                # self.sword_image, self.sword_rect = load_image('Sword/sword.png')
        surface.blit(self.final_sword_image, self.final_sword_rect)

    def bow(self, scroll, surface, sorcers):
        bow_power = 0
        mx, my = pygame.mouse.get_pos()
        if mx < self.rect.x:
            bow_pos = [self.rect.x - scroll[0], self.rect.y + 10 - scroll[1]]
        elif mx >= self.rect.x:
            bow_pos = [self.rect.x + 16 - scroll[0], self.rect.y + 10 - scroll[1]]
        oppisite = my - bow_pos[1]
        adjacent = mx - bow_pos[0]
        try:
            final_angle = -math.degrees(math.tan(oppisite/adjacent))
        except ZeroDivisionError:
            final_angle = -90
        final_bow_image = pygame.transform.rotate(self.bow_image, final_angle)
        final_bow_rect = pygame.Rect(bow_pos[0], bow_pos[1], final_bow_image.get_width(), final_bow_image.get_height())
        if pygame.mouse.get_pressed()[0] == 1:
            if bow_power < 5:
                bow_power += 0.02
            if self.arrow_counter < 1:
                self.arrow_counter += 1
        if pygame.mouse.get_pressed()[0] != 1:
            self.arrow_counter = 0
        if self.arrow_counter > 0:
            arrow = [final_bow_rect.x, final_bow_rect.y, 8, 3]
            self.arrows.append(arrow)
        for arrow in self.arrows:
            arrow[0] += bow_power * 10
            arrow_rect = pygame.Rect(arrow[0], arrow[1], arrow[2], arrow[3])
            surface.blit(self.arrow_image, arrow_rect)
        surface.blit(final_bow_image, final_bow_rect)

    def load_images(self):
        self.sword_list = []
        load_image_list('Data/Images/Sword/attack', self.sword_list, 11)

    def render(self, surface, scroll, health):
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
        pygame.draw.rect(surface, (125, 0 ,0), health_bar)
        # pygame.draw.rect(surface, (0, 70, 100), (self.hit_box.x - scroll[0], self.hit_box.y - scroll[1], 16, 16), 2)

class Potions(object):
    def __init__(self):
        self.heal_potion = pygame.image.load('Data/Images/Potions/heal_potion.png').convert_alpha()

    def add_potion(self, type, strength_value, potions):
        potions.append([type, strength_value])

    def main(self, surface, scroll, potions, player_health):
        for potion in potions:
            potion_type = potion[0]
            potion_strength = potion[1]
            if potion_type == 'healing':
                player_health += potion_strength

class Sorcer(object):
    def __init__(self):
        self.sorcer_image, self.rect = load_image('Sorcer/sorcer_idle.png')

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

class Witch(object):
    def __init__(self):
        self.image = pygame.image.load('Data/Images/Witch/witch.png').convert_alpha()
        self.witch_node = [0, 0, 1]
        self.player_node = [0, 0, 1]

    def add_witch(self, x, y, witches):
        witches.append([x, y, 32, 32, 1, random.randint(0, 10), pygame.time.get_ticks()])

    def main(self, surface, scroll, witches, potions, knight_pos, tile_list, pathfind_nodes, pathfinder, particle_system, particles, debug):
        for witch in witches:
            knight_rect = pygame.Rect(knight_pos[0], knight_pos[1], 18, 28)
            witch_rect = pygame.Rect(witch[0], witch[1], 32, 32)
            between_nodes = []
            for node in pathfind_nodes:
                node_rect = pygame.Rect(node[0] - 8, node[1] + 26, 32, 32)
                if node_rect.colliderect(knight_rect):
                    if debug:
                        pygame.draw.rect(surface, (0, 255, 0), (node[0] - scroll[0] - 8, node[1] - scroll[1] - 4, 24, 24))
                    self.player_node = [node[0], node[1], node[2]]
                if node_rect.colliderect(witch_rect):
                    self.witch_node = [node[0], node[1], node[2]]
            pathfinder.find_path(self.witch_node[2], self.player_node[2])
            if debug:
                pygame.draw.line(surface, (50, 50, 150), (self.witch_node[0] - scroll[0], self.witch_node[1] - scroll[1]), (self.player_node[0] - scroll[0], self.player_node[1] - scroll[1]))
            witch_rect = pygame.Rect(witch[0], witch[1], 32, 32)
            surface.blit(self.image, (witch_rect.x - scroll[0], witch_rect.y - scroll[1], 32, 32))

class ArcherTower(object):
    def __init__(self):
        self.tower_image = pygame.image.load('Data/Images/Archer_Tower/tower.png').convert_alpha()
        self.archer_image = pygame.image.load('Data/Images/Archer_Tower/archer.png').convert_alpha()
        self.bow_image = pygame.image.load('Data/Images/Archer_Tower/bow.png').convert_alpha()
        self.arrow_image = pygame.image.load('Data/Images/Archer_Tower/arrow.png').convert_alpha()
        self.archer_counter = 0

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
                bow_rect = pygame.Rect(archer_x - 5, archer_y + 3, 4, 14)
                if pygame.time.get_ticks() - shoot_timer >= 1000:
                    archer[5] = pygame.time.get_ticks()
                    archer_arrows.append([bow_rect.centerx, bow_rect.centery, [int(bow_adj), int(bow_opp)], self.arrow_image])
                archer_rect = pygame.Rect(archer_x, archer_y, 10, 10)
                final_bow_img = pygame.transform.rotate(self.bow_image, final_angle)
                surface.blit(final_bow_img, (bow_rect.x - scroll[0], bow_rect.y - scroll[1], bow_rect.width, bow_rect.height))
                surface.blit(self.archer_image, (archer_rect.x - scroll[0], archer_rect.y - scroll[1], 20, 20))
                if archer_parent == False:
                    pygame.draw.rect(surface, (50, 32, 57), (archer_x - scroll[0], archer_y - 5 - scroll[1], archer_health * 2.2, 2))

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

    def add_particle(self, x, y, radius, velocity, color, particles):
        particles.append([x, y, radius, velocity, color])

    def main(self, surface, scroll, particles):
        for particle in particles:
            particle[0] += particle[3][0]
            particle[1] += particle[3][1]
            particle[2] -= 0.05
            if particle[2] <= 1:
                particles.remove(particle)
            pygame.draw.circle(surface, particle[4], (particle[0] - scroll[0], particle[1] - scroll[1]), particle[2])
