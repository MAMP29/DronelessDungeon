import random
import numpy as np

class MazeDrawer:
    """ Se encarga de dibujar el laberinto en la pantalla con base a los tiles proporcionados."""

    def __init__(self, maze_loader=None, tile_map=None, tile_size=None):
        self.maze = maze_loader.render_maze if maze_loader else None
        self.tile_map = tile_map
        self.tile_size = tile_size
        self.fixed_map = None
        self.packages_fixed = None
        self.obstacles_fixed = None
        self.obstacle_map = None
        self._border_tiles = {
            -1: "top_middle", -2: "top_wall", -3: "top_left", -4: "top_left_corner",
            -5: "top_right", -6: "top_right_corner", -7: "left", -8: "right",
            -9: "bottom_left", -10: "bottom_right", -11: "bottom_middle"
        }
        if maze_loader is not None:
            self.generate_fixed_map()

    def generate_fixed_map(self):
        """Crea una copia del mapa con obstáculos fijos (para que no cambien en cada frame)"""
        self.fixed_map = np.copy(self.maze)  # Copia la matriz original
        self.obstacle_map = {}  # Diccionario para almacenar los obstáculos fijos


        rows, cols = self.maze.shape
        for y in range(rows):
            for x in range(cols):
                if self.maze[y, x] == 1:  # Si es un obstáculo
                    self.obstacle_map[(y, x)] = random.choice(self.tile_map["obstacle"])


    def draw_maze(self, screen):
        """Dibuja el laberinto en la pantalla usando la matriz fija"""
        rows, cols = self.fixed_map.shape
        for y in range(rows):
            for x in range(cols):
                self._draw_tile(screen, x, y)

    def _draw_tile(self, screen, x, y):
        """Dibuja un tile en la posición dada"""
        cell = self.fixed_map[y, x]
        screen.blit(self.tile_map["floor"], (x * self.tile_size, y * self.tile_size))

        if (y, x) in self.obstacle_map:
            screen.blit(self.obstacle_map[(y, x)], (x * self.tile_size, y * self.tile_size))
        elif cell == 2:
            screen.blit(self.tile_map["searcher"], (x * self.tile_size, y * self.tile_size))
        elif cell == 3:
            screen.blit(random.choice(self.tile_map["danger"]), (x * self.tile_size, y * self.tile_size))
        elif cell == 4:
            screen.blit(self.tile_map["objetive"], (x * self.tile_size, y * self.tile_size))
        elif cell in self._border_tiles:
            screen.blit(self.tile_map[self._border_tiles[cell]], (x * self.tile_size, y * self.tile_size))
        
    def move_charanter(self, inir ,inic, newr, newc):
        element = 0

        if (inir, inic) in self.packages_fixed: element = 4
        if (inir, inic) in self.obstacles_fixed: element = 3
        inir +=2
        inic +=1
        newr +=2
        newc +=1
        self.fixed_map[inir, inic] = element
        self.fixed_map[newr, newc] = 2

