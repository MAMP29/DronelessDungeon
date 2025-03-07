import pygame

class TileProcessor:

    """ Representa el conjunto de tiles y sus respectivos tamaños, tamaño de la imagen y escala de los tiles."""

    def __init__(self, assets_file, searcher_file, danger_file, tile_size, scale_factor=4):
        self.assets_file = assets_file
        self.searcher_file = searcher_file
        self.danger_file = danger_file
        #self.objetive_file = None #Como el objetivo viene el asset_file no lo cargamos en la clase, pero aquí esta función en caso de que lo necesitemos
        self.tile_size = tile_size
        self.scale_factor = scale_factor
        self.tiles = {}  # Ahora usamos un diccionario en lugar de una lista
        self.new_size = tile_size * scale_factor  # Escalar tamaño
        self.load_tileset()  # Cargar tiles al iniciar

    def load_tileset(self):
        """Carga los tiles desde la imagen y los almacena en un diccionario"""
        tileset_image = pygame.image.load(self.assets_file).convert_alpha()
        searcher_image = pygame.image.load(self.searcher_file).convert_alpha()
        danger_image = pygame.image.load(self.danger_file).convert_alpha()

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
        searcher_image = pygame.transform.scale(searcher_image, (self.new_size, self.new_size))
        danger_image = pygame.transform.scale(danger_image, (self.new_size, self.new_size))

        self.tiles["searcher"] = self.tiles[188]
        self.tiles["danger"] = danger_image

        self.tiles["objetive"] = self.tiles[182]

    def reload_tileset(self):
        self.tiles = {}
        self.load_tileset()


    def create_tile_map(self):
        """Crea el mapeo de tiles en base a los índices dados"""
        return {
            "floor": self.tiles[54],
            "obstacle": [self.tiles[154], self.tiles[183]], #, self.tiles[162], self.tiles[183], self.tiles[184], self.tiles[185], self.tiles[186]

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
            "searcher": self.tiles["searcher"],
            "danger": self.tiles["danger"],
            "objetive": self.tiles["objetive"],
        }

    def get_tile(self, tile_id):
        return self.tiles.get(tile_id, self.tiles[54])
