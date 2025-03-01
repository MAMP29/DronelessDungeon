import numpy as np


class MazeLoader:

    """ Esta clase se encarga de cargar y procesar el laberinto, está compuesta de dos partes,
        el laberinto original y el laberinto ampliado que se utiliza para dibujar el laberinto en pantalla."""

    def __init__(self, file_path=None):
        self.file_path = file_path
        self.maze = None
        self.render_maze = None
        self.shape = None

        if file_path:
            self.load_maze()

    def load_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def load_maze(self):
        data = self.load_file()
        maze = [list(map(int, line.split())) for line in data.splitlines()]
        self.maze = np.array(maze)
        self.shape = self.maze.shape
        self.generate_render_maze()

    def generate_render_maze(self):

        """Genera el laberinto con bordes adicionales para renderizado."""
        # Obtener dimensiones del laberinto original
        rows, cols = self.shape

        # Crear una nueva matriz con bordes adicionales
        new_rows, new_cols = rows + 3, cols + 2
        new_maze = np.zeros((new_rows, new_cols), dtype=int)

        # Colocar el laberinto original en el centro de la nueva matriz
        new_maze[2:rows + 2, 1:cols + 1] = self.maze

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
        self.render_maze = new_maze

    def control_size(self):
        """Define el factor de escala basado en el tamaño del laberinto."""
        rows, cols = self.shape
        if rows >= 512 or cols >= 512:
            return 2
        elif rows >= 256 or cols >= 256:
            return 3
        elif rows >= 128 or cols >= 128:
            return 4
        else:
            return 5

