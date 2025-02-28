import pygame


def load_tileset(file_name, cheese_file, tile_size, scale_factor=4):
    tileset_image = pygame.image.load(file_name).convert_alpha()
    cheese_image = pygame.image.load(cheese_file).convert_alpha()
    tiles = []
    tileset_width, tileset_height = tileset_image.get_size()
    new_size = tile_size * scale_factor  # Aumentar tamaño

    for y in range(0, tileset_height, tile_size):
        for x in range(0, tileset_width, tile_size):
            tile = tileset_image.subsurface(pygame.Rect(x, y, tile_size, tile_size))
            tile = pygame.transform.scale(tile, (new_size, new_size))  # Escalar
            tiles.append(tile)

    cheese_image = pygame.transform.scale(cheese_image, (new_size, new_size))
    tiles.append(cheese_image)
    return tiles, new_size  # Retornar tiles y nuevo tamaño

def reload_tileset(file_name, cheese_file, tile_size, scale_factor=4):
    tiles, new_size = load_tileset(file_name, cheese_file, tile_size, scale_factor)
    return tiles, new_size



def create_tile_map(tiles):
    """Crea el mapeo de tiles en base a los índices dados"""
    tile_map = {
        "floor": tiles[54],
        "obstacle": [tiles[154], tiles[158], tiles[162], tiles[183], tiles[184], tiles[185], tiles[186]],

        # Bordes superiores
        "top_left": tiles[5],
        "top_left_corner": tiles[29],
        "top_middle": tiles[6],
        "top_wall": tiles[30],
        "top_right": tiles[7],
        "top_right_corner": tiles[31],

        # Bordes inferiores
        "bottom_left": tiles[77],
        "bottom_middle": tiles[78],
        "bottom_right": tiles[79],

        # Bordes laterales
        "left": tiles[53],
        "right": tiles[55],

        # Elementos del juego
        "cheese": tiles[240],
    }

    return tile_map

