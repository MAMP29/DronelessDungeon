import pygame

class TileProcessor:

    """ Representa el conjunto de tiles y sus respectivos tamaños, tamaño de la imagen y escala de los tiles."""

    def __init__(self, file_name, cheese_file, tile_size, scale_factor=4):
        self.file_name = file_name
        self.cheese_file = cheese_file
        self.tile_size = tile_size
        self.scale_factor = scale_factor
        self.tiles = {}  # Ahora usamos un diccionario en lugar de una lista
        self.new_size = tile_size * scale_factor  # Escalar tamaño
        self.load_tileset()  # Cargar tiles al iniciar

    def load_tileset(self):
        """Carga los tiles desde la imagen y los almacena en un diccionario"""
        tileset_image = pygame.image.load(self.file_name).convert_alpha()
        cheese_image = pygame.image.load(self.cheese_file).convert_alpha()

        tileset_width, tileset_height = tileset_image.get_size()

        # Extraer tiles y almacenarlos en un diccionario
        tile_id = 0
        for y in range(0, tileset_height, self.tile_size):
            for x in range(0, tileset_width, self.tile_size):
                tile = tileset_image.subsurface(pygame.Rect(x, y, self.tile_size, self.tile_size))
                tile = pygame.transform.scale(tile, (self.new_size, self.new_size))  # Escalar
                self.tiles[tile_id] = tile
                tile_id += 1

        # Cargar y escalar el queso
        cheese_image = pygame.transform.scale(cheese_image, (self.new_size, self.new_size))
        self.tiles["cheese"] = cheese_image

    def reload_tileset(self):
        self.tiles = {}
        self.load_tileset()

    def create_tile_map(self):
        """Crea el mapeo de tiles en base a los índices dados"""
        return {
            "floor": self.tiles[54],
            "obstacle": [self.tiles[154], self.tiles[158], self.tiles[162], self.tiles[183],
                         self.tiles[184], self.tiles[185], self.tiles[186]],

            # Bordes superiores
            "top_left": self.tiles[5],
            "top_left_corner": self.tiles[29],
            "top_middle": self.tiles[6],
            "top_wall": self.tiles[30],
            "top_right": self.tiles[7],
            "top_right_corner": self.tiles[31],

            # Bordes inferiores
            "bottom_left": self.tiles[77],
            "bottom_middle": self.tiles[78],
            "bottom_right": self.tiles[79],

            # Bordes laterales
            "left": self.tiles[53],
            "right": self.tiles[55],

            # Elementos del juego
            "cheese": self.tiles["cheese"],
        }

    def get_tile(self, tile_id):
        return self.tiles.get(tile_id, self.tiles[54])
