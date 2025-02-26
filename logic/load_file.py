import numpy as np

def load_data(file_path):
    data = load_file(file_path)
    maze = load_maze(data)
    print(maze)
    print(maze.shape)

def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        print(data)
        return data

def load_maze(data):
    maze = [list(map(int, line.split())) for line in data.splitlines()]
    return np.array(maze)

