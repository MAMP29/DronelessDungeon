import pygame


def load_tileset(file_name, title_size):
    tileset_image = pygame.image.load(file_name).convert_alpha()
    tiles = []
    tileset_width, tileset_height = tileset_image.get_size()

    for y in range(0, tileset_height, title_size):
        for x in range(0, tileset_width, title_size):
            tile = tileset_image.subsurface(pygame.Rect(x, y, title_size, title_size))
            tiles.append(tile)

    return tiles


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
    }

    return tile_map

