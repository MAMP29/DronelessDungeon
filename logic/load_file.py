import numpy as np


def load_data(file_path):
    data = load_file(file_path)
    maze = load_maze(data)
    maze = np.array(maze)

    # Obtener dimensiones del laberinto original
    rows, cols = maze.shape

    # Crear una nueva matriz con bordes adicionales
    new_rows = rows + 3
    new_cols = cols + 2
    new_maze = np.zeros((new_rows, new_cols), dtype=int)

    # Colocar el laberinto original en el centro de la nueva matriz
    new_maze[2:rows + 2, 1:cols + 1] = maze

    # Configurar los bordes con los nuevos valores
    # Esquinas superiores
    new_maze[0, 0] = -3
    new_maze[0, new_cols - 1] = -5

    # Primera fila (después de las esquinas)
    new_maze[0, 1:new_cols - 1] = -1

    # Segunda fila
    new_maze[1, 0] = -4
    new_maze[1, 1:new_cols - 1] = -2
    new_maze[1, new_cols - 1] = -6

    # Laterales izquierdos
    new_maze[2:new_rows - 1, 0] = -7

    # Laterales derechos
    new_maze[2:new_rows - 1, new_cols - 1] = -8

    # Última fila
    new_maze[new_rows - 1, 0] = -9
    new_maze[new_rows - 1, new_cols - 1] = -10
    new_maze[new_rows - 1, 1:new_cols - 1] = -11

    print(np.array(new_maze))
    return np.array(new_maze)

def control_size(maze):
    rows, cols = maze.shape

    if rows >= 512 or cols >= 512:
        return 2
    elif rows >= 256 or cols >= 256:
        return 3
    elif rows >= 128 or cols >= 128:
        return 4
    else:
        return 5



def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        #print(data)
        return data

def load_maze(data):
    maze = [list(map(int, line.split())) for line in data.splitlines()]
    return np.array(maze)

