import pygame
import Data.engine

def renderLevel(display, level_map, tile_list, pathfind_tiles, spawners, archer_tower, archer_towers, archers, witch_hut, witch_huts, witches, new_level, scroll):
    tile_size = 32
    for tile_data in level_map:
        tile_y = tile_data[0] * tile_size
        extract_tile_x, tile_type = tile_data[1]
        tile_x = extract_tile_x * tile_size
        if tile_x - scroll[0] >= -64 and tile_x - scroll[0] <= 964 and tile_y - scroll[1] >= -64 and tile_y - scroll[1] <= 664:
            if tile_type == '0':
                tile_img, tile_img_rect = Data.engine.load_image('Tiles/top_tile.png')
                display.blit(tile_img, (tile_x -scroll[0], tile_y - scroll[1], tile_size, tile_size))
                tile_list.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
                pathfind_tiles.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
            if tile_type == '1':
                tile_img, tile_img_rect = Data.engine.load_image('Tiles/ground_tile.png')
                display.blit(tile_img, (tile_x -scroll[0], tile_y - scroll[1], tile_size, tile_size))
                tile_list.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
            if tile_type == '2':
                tile_img, tile_img_rect = Data.engine.load_image('Tiles/bottom_tile.png')
                display.blit(tile_img, (tile_x -scroll[0], tile_y - scroll[1], tile_size, tile_size))
                tile_list.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
            if tile_type == '3':
                tile_img, tile_img_rect = Data.engine.load_image('Tiles/left_tile.png')
                display.blit(tile_img, (tile_x -scroll[0], tile_y - scroll[1], tile_size, tile_size))
                tile_list.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
            if tile_type == '4':
                tile_img, tile_img_rect = Data.engine.load_image('Tiles/right_tile.png')
                display.blit(tile_img, (tile_x -scroll[0], tile_y - scroll[1], tile_size, tile_size))
                tile_list.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
            if tile_type == '5':
                tile_img, tile_img_rect = Data.engine.load_image('Tiles/corner_rb.png')
                display.blit(tile_img, (tile_x -scroll[0], tile_y - scroll[1], tile_size, tile_size))
                tile_list.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
            if tile_type == '6':
                tile_img, tile_img_rect = Data.engine.load_image('Tiles/corner_rt.png')
                display.blit(tile_img, (tile_x -scroll[0], tile_y - scroll[1], tile_size, tile_size))
                tile_list.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
                pathfind_tiles.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
            if tile_type == '7':
                tile_img, tile_img_rect = Data.engine.load_image('Tiles/corner_lb.png')
                display.blit(tile_img, (tile_x -scroll[0], tile_y - scroll[1], tile_size, tile_size))
                tile_list.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
            if tile_type == '8':
                tile_img, tile_img_rect = Data.engine.load_image('Tiles/corner_lt.png')
                display.blit(tile_img, (tile_x -scroll[0], tile_y - scroll[1], tile_size, tile_size))
                tile_list.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
                pathfind_tiles.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
        if new_level:
            if tile_type == '9':
                spawners.append([tile_x, tile_y, 25, pygame.time.get_ticks()])
            elif tile_type == '10':
                archer_tower.create_tower(tile_x, tile_y, archer_towers, archers)
            elif tile_type == '11':
                witch_hut.create_hut(tile_x, tile_y, witch_huts, witches)

    return tile_list
