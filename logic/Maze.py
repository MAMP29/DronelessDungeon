import random
import numpy as np

def generate_fixed_map(maze, tile_map):
    """Crea una copia del mapa con obstáculos fijos (para que no cambien en cada frame)"""
    fixed_map = np.copy(maze)  # Copia la matriz original
    obstacle_map = {}  # Diccionario para almacenar los obstáculos fijos

    rows, cols = maze.shape
    for y in range(rows):
        for x in range(cols):
            if maze[y, x] == 1:  # Si es un obstáculo
                obstacle_map[(y, x)] = random.choice(tile_map["obstacle"])

    return fixed_map, obstacle_map  # Retornamos la matriz y el diccionario de obstáculos


def draw_maze(screen, fixed_map, obstacle_map, tile_map, tile_size):
    """Dibuja el laberinto en la pantalla usando la matriz fija"""
    rows, cols = fixed_map.shape
    for y in range(rows):
        for x in range(cols):
            cell = fixed_map[y, x]

            # 🔹 Siempre dibujar el piso primero
            screen.blit(tile_map["floor"], (x * tile_size, y * tile_size))

            # 🔹 Dibujar los obstáculos fijos
            if (y, x) in obstacle_map:
                screen.blit(obstacle_map[(y, x)], (x * tile_size, y * tile_size))

            # 🔹 Dibujar los bordes y paredes
            elif cell == -1:
                screen.blit(tile_map["top_middle"], (x * tile_size, y * tile_size))
            elif cell == -2:
                screen.blit(tile_map["top_wall"], (x * tile_size, y * tile_size))
            elif cell == -3:
                screen.blit(tile_map["top_left"], (x * tile_size, y * tile_size))
            elif cell == -4:
                screen.blit(tile_map["top_left_corner"], (x * tile_size, y * tile_size))
            elif cell == -5:
                screen.blit(tile_map["top_right"], (x * tile_size, y * tile_size))
            elif cell == -6:
                screen.blit(tile_map["top_right_corner"], (x * tile_size, y * tile_size))
            elif cell == -7:
                screen.blit(tile_map["left"], (x * tile_size, y * tile_size))
            elif cell == -8:
                screen.blit(tile_map["right"], (x * tile_size, y * tile_size))
            elif cell == -9:
                screen.blit(tile_map["bottom_left"], (x * tile_size, y * tile_size))
            elif cell == -10:
                screen.blit(tile_map["bottom_right"], (x * tile_size, y * tile_size))
            elif cell == -11:
                screen.blit(tile_map["bottom_middle"], (x * tile_size, y * tile_size))
