


class MazeSolver:
    """ Representa el laberinto original y lo resuelve con base a distintas funciones de búsqueda  """

    def __init__(self, maze_loader):
        self.maze = maze_loader.maze
        self.start = None
        self.end = None
