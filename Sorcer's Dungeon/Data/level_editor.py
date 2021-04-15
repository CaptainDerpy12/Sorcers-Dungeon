import pygame, sys, csv, time
import clip as clip
pygame.init()

pygame.mouse.set_visible(False)
mb1_click = False
mb2_click = False
whole_display = pygame.display.set_mode((1100, 630), pygame.RESIZABLE + pygame.SCALED)
pygame.display.set_caption('Level Editor')
editor_screen = pygame.Surface((900, 600))
menu_bar = pygame.Surface((1100, 30))
tile_select_screen = pygame.Surface((200, 600))
save_button = pygame.image.load('Data/Images/Buttons/save_button.png').convert_alpha()
save_button_rect = save_button.get_rect(center=(100, 500))
clock = pygame.time.Clock()

img_list = []
mimg_list = []
for x in range(1, 9):
    img = pygame.image.load('Data/Images/Mouse/mouse' + str(x) + '.png').convert_alpha()
    mimg_list.append(img)

class Font():
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        font_img = pygame.image.load(path).convert()
        font_img.set_colorkey((0,0,0))
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip.clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing

def update_mouse():
    mx, my = pygame.mouse.get_pos()
    font.render(whole_display, str(int(mx/32)) + '  :  ' + str(int(my/32)), (70, 550))
    pointer_image = mimg_list[0]
    pointer_image_rect = pointer_image.get_rect(center=(mx, my))
    whole_display.blit(pointer_image, pointer_image_rect)
    if mb1_click or mb2_click:
        for x in range(0,8):
            pointer_image = mimg_list[x]
            whole_display.blit(pointer_image, pointer_image_rect)

def load_image(path, list=None, add_to_list=False):
    img = pygame.image.load(path).convert_alpha()
    img_rect = img.get_rect()
    if add_to_list == True:
        list.append(img)
    return img, img_rect

tiles = {
'top_tile':False,
'ground_tile':True,
'left_tile':False,
'right_tile':False,
'bottom_tile':False,
'corner_lt':False,
'corner_lb':False,
'corner_rt':False,
'corner_rb':False,
'spawner':False,
'archer tower':False
}

top_tile, top_tile_rect = load_image('Data/Images/Tiles/top_tile.png', img_list, True)
ground_tile, ground_tile_rect = load_image('Data/Images/Tiles/ground_tile.png', img_list, True)
bottom_tile, bottom_tile_rect = load_image('Data/Images/Tiles/bottom_tile.png', img_list, True)
left_tile, left_tile_rect = load_image('Data/Images/Tiles/left_tile.png', img_list, True)
right_tile, right_tile_rect = load_image("Data/Images/Tiles/right_tile.png", img_list, True)
corner_rb, corner_rb_rect = load_image('Data/Images/Tiles/corner_rb.png', img_list, True)
corner_rt, corner_rt_rect = load_image('Data/Images/Tiles/corner_rt.png', img_list, True)
corner_lb, corner_lb_rect = load_image('Data/Images/Tiles/corner_lb.png', img_list, True)
corner_lt, corner_lt_rect = load_image('Data/Images/Tiles/corner_lt.png', img_list, True)
spawner, spawner_rect = load_image('Data/Images/Spawner.png', img_list, True)
archer_tower, archer_tower_rect = load_image('Data/Images/Archer_Tower/tower.png', img_list, True)

tile_types = 11
current_level = 1
rows = 75
cols = 50
current_tile = 0
scrolls = {'left':False, 'right':False, 'up':False, 'down':False}
scrollx = 0
scrolly = 0
scroll_speed = 1
tile_size = 32
level_data = []
orig_level_data = level_data
for row in range(0, cols):
    r = [-1] * cols
    level_data.append(r)

def update_tile_selected_text():
    current_tile_str = ''
    if tiles['top_tile']:
        current_tile_str = 'Top Tile'
    elif tiles['ground_tile']:
        current_tile_str = 'Ground Tile'
    elif tiles['left_tile']:
        current_tile_str = 'Left Tile'
    elif tiles['right_tile']:
        current_tile_str = 'Right Tile'
    elif tiles['bottom_tile']:
        current_tile_str = 'Bottom Tile'
    elif tiles['corner_rb']:
        current_tile_str = 'Corner Right Bottom Tile'
    elif tiles['corner_rt']:
        current_tile_str = 'Corner Right Top Tile'
    elif tiles['corner_lb']:
        current_tile_str = 'Corner Left Bottom Tile'
    elif tiles['corner_lt']:
        current_tile_str = 'Corner Left Top Tile'
    elif tiles['spawner']:
        current_tile_str = 'Spawner'
    elif tiles['archer tower']:
        current_tile_str = 'Archer Tower'
    return current_tile_str

def scale(surface, x_size, y_size):
    scaled_img = pygame.transform.scale(surface, (x_size, y_size))
    return scaled_img

def render_level():
    for y, row in enumerate(level_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                editor_screen.blit(img_list[tile], (x * tile_size - scrollx - 192, y * tile_size - 16 - scrolly))

def buttons():
    mx, my = pygame.mouse.get_pos()
    whole_display.blit(save_button, save_button_rect)
    if save_button_rect.collidepoint((mx, my)):
        if mb1_click:
            with open('Data/levels/level_' + str(current_level) + '.csv', 'w', newline ='') as level_file:
                writer = csv.writer(level_file, delimiter = ',')
                for row in level_data:
                    writer.writerow(row)

def render_UI():
    current_tile_str = update_tile_selected_text()
    whole_display.fill((50, 70, 90))
    whole_display.blit(editor_screen, (200, 30))
    editor_screen.fill((0,0,0))
    whole_display.blit(menu_bar, (0, 0))
    menu_bar.fill((30, 50, 70))
    font.render(whole_display, 'Level Editor', (20, 10))
    font.render(whole_display, 'Tile Set', (50, 44))
    font.render(menu_bar, 'Current Tile Selected: ' + str(current_tile_str), (150, 10))
    buttons()

def select():
    top_tile_scaled = scale(top_tile, 16, 16)
    ground_tile_scaled = scale(ground_tile, 16, 16)
    left_tile_scaled = scale(left_tile, 16, 16)
    right_tile_scaled = scale(right_tile, 16, 16)
    bottom_tile_scaled = scale(bottom_tile, 16, 16)
    corner_rb_scaled = scale(corner_rb, 16, 16)
    corner_rt_scaled = scale(corner_rt, 16, 16)
    corner_lb_scaled = scale(corner_lb, 16, 16)
    corner_lt_scaled = scale(corner_lt, 16, 16)
    spawner_scaled = scale(spawner, 16, 16)
    archer_tower_scaled = scale(archer_tower, 32, 65)
    top_tile_loc = top_tile_scaled.get_rect(center=(50, 85))
    ground_tile_loc = pygame.Rect(top_tile_loc.left, top_tile_loc.bottom, 16, 16)
    left_tile_loc = pygame.Rect(ground_tile_loc.left - 16, ground_tile_loc.top, 16, 16)
    right_tile_loc = pygame.Rect(ground_tile_loc.right, ground_tile_loc.top, 16, 16)
    bottom_tile_loc = pygame.Rect(ground_tile_loc.left, ground_tile_loc.bottom, 16,16)
    corner_rb_loc = pygame.Rect(bottom_tile_loc.right, ground_tile_loc.bottom, 16, 16)
    corner_rt_loc = pygame.Rect(top_tile_loc.right, top_tile_loc.top,16,16)
    corner_lt_loc = pygame.Rect(top_tile_loc.left - 16, top_tile_loc.top,16,16)
    corner_lb_loc = pygame.Rect(left_tile_loc.left, left_tile_loc.bottom,16,16)
    spawner_loc = pygame.Rect(39, 150, 16, 16)
    archer_tower_loc = pygame.Rect(39, 170, 32, 65)
    whole_display.blit(ground_tile_scaled, ground_tile_loc)
    whole_display.blit(top_tile_scaled, top_tile_loc)
    whole_display.blit(left_tile_scaled, left_tile_loc)
    whole_display.blit(right_tile_scaled, right_tile_loc)
    whole_display.blit(bottom_tile_scaled, bottom_tile_loc)
    whole_display.blit(corner_rb_scaled, corner_rb_loc)
    whole_display.blit(corner_rt_scaled, corner_rt_loc)
    whole_display.blit(corner_lt_scaled, corner_lt_loc)
    whole_display.blit(corner_lb_scaled, corner_lb_loc)
    whole_display.blit(spawner_scaled, spawner_loc)
    whole_display.blit(archer_tower_scaled, archer_tower_loc)
    mx, my = pygame.mouse.get_pos()
    if mb1_click:
        if top_tile_loc.collidepoint((mx, my)):
            for key_value_pair in tiles.items():
                key, value = key_value_pair
                tiles.update({str(key):False})
            tiles['top_tile'] = True
        elif ground_tile_loc.collidepoint((mx, my)):
            for key_value_pair in tiles.items():
                key, value = key_value_pair
                tiles.update({str(key):False})
            tiles['ground_tile'] = True
        elif right_tile_loc.collidepoint((mx, my)):
            for key_value_pair in tiles.items():
                key, value = key_value_pair
                tiles.update({str(key):False})
            tiles['right_tile'] = True
        elif left_tile_loc.collidepoint((mx, my)):
            for key_value_pair in tiles.items():
                key, value = key_value_pair
                tiles.update({str(key):False})
            tiles['left_tile'] = True
        elif bottom_tile_loc.collidepoint((mx, my)):
            for key_value_pair in tiles.items():
                key, value = key_value_pair
                tiles.update({str(key):False})
            tiles['bottom_tile'] = True
        elif corner_rb_loc.collidepoint((mx, my)):
            for key_value_pair in tiles.items():
                key, value = key_value_pair
                tiles.update({str(key):False})
            tiles['corner_rb'] = True
        elif corner_rt_loc.collidepoint((mx, my)):
            for key_value_pair in tiles.items():
                key, value = key_value_pair
                tiles.update({str(key):False})
            tiles['corner_rt'] = True
        elif corner_lb_loc.collidepoint((mx, my)):
            for key_value_pair in tiles.items():
                key, value = key_value_pair
                tiles.update({str(key):False})
            tiles['corner_lb'] = True
        elif corner_lt_loc.collidepoint((mx, my)):
            for key_value_pair in tiles.items():
                key, value = key_value_pair
                tiles.update({str(key):False})
            tiles['corner_lt'] = True
        elif spawner_loc.collidepoint((mx, my)):
            for key_value_pair in tiles.items():
                key, value = key_value_pair
                tiles.update({str(key):False})
            tiles['spawner'] = True
        elif archer_tower_loc.collidepoint((mx, my)):
            for key_value_pair in tiles.items():
                key, value = key_value_pair
                tiles.update({str(key):False})
            tiles['archer tower'] = True

def edit():
    if tiles['top_tile']:
        current_tile = 0
    elif tiles['ground_tile']:
        current_tile = 1
    elif tiles['left_tile']:
        current_tile = 3
    elif tiles['right_tile']:
        current_tile = 4
    elif tiles['bottom_tile']:
        current_tile = 2
    elif tiles['corner_rb']:
        current_tile = 5
    elif tiles['corner_rt']:
        current_tile = 6
    elif tiles['corner_lb']:
        current_tile = 7
    elif tiles['corner_lt']:
        current_tile = 8
    elif tiles['spawner']:
        current_tile = 9
    elif tiles['archer tower']:
        current_tile = 10

    mx, my = pygame.mouse.get_pos()
    mpos = pygame.mouse.get_pos()
    x = (mpos[0] + scrollx) // tile_size
    y = (mpos[1] + scrolly) // tile_size
    if mx <= 1100 and mx >= 200 and my > 30 and my < 600:
        if pygame.mouse.get_pressed()[0]:
            if level_data[y][x] != current_tile:
                level_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2]:
            level_data[y][x] = -1

font = Font('Data/Images/text/large_font.png')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mb1_click = True
            if event.button == 3:
                mb2_click = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                with open('Data/levels/level_' + str(current_level) + '.csv', 'w', newline ='') as level_file:
                    writer = csv.writer(level_file, delimiter = ',')
                    for row in level_data:
                        writer.writerow(row)
            if event.key == pygame.K_l:
                with open('Data/levels/level_' + str(current_level) + '.csv', newline='') as level_file:
                    reader = csv.reader(level_file, delimiter = ',')
                    for x, row  in enumerate(reader):
                        for y, tile in enumerate(row):
                            level_data[x][y] = int(tile)
            if event.key == pygame.K_RIGHT:
                scrolls['right'] = True
            if event.key == pygame.K_LEFT:
                scrolls['left'] = True
            if event.key == pygame.K_UP:
                scrolls['up'] = True
            if event.key == pygame.K_DOWN:
                scrolls['down'] = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                scrolls['right'] = False
            if event.key == pygame.K_LEFT:
                scrolls['left'] = False
            if event.key == pygame.K_UP:
                scrolls['up'] = False
            if event.key == pygame.K_DOWN:
                scrolls['down'] = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1
    if scrolls['left'] == True and scrollx > -192:
        scrollx -= 5 * scroll_speed
    if scrolls['right'] == True and scrollx < (cols * tile_size) - 1100:
        scrollx += 5 * scroll_speed
    if scrolls['up'] == True and scrolly > 0:
        scrolly -= 5 * scroll_speed
    if scrolls['down'] == True and scrolly < (rows * tile_size):
        scrolly += 5 * scroll_speed
    edit()
    render_level()
    render_UI()
    select()
    update_mouse()
    mb1_click = False
    mb2_click = False
    clock.tick(60)
    pygame.display.update()
