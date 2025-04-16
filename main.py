import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from logic.MazeLoader import MazeLoader
from logic.MazeSolver import MazeSolver
from logic.TileProcessor import TileProcessor
from logic.MazeDrawer import MazeDrawer

pygame.init()

TILE_SIZE = 16
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RatCheese")

ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT), "assets/themes.json")

presentation_rect = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((WIDTH - 500 - 50, 50), (500, 300)),  # (X, Y, Ancho, Alto)
    manager=ui_manager,
    object_id=ObjectID(class_id='@wooden_panel', object_id='#presentation_panel'),
)

load_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH - 500 - 50, 380), (500, 50)),  # Ajustado debajo del panel
    text="Load",
    manager=ui_manager,
    object_id=ObjectID(class_id='@wooden_button', object_id='#load_button'),
)

start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH - 500 - 50, HEIGHT - 100), (500, 50)),  # Pegado abajo
    text="Start",
    manager=ui_manager,
    object_id=ObjectID(class_id='@wooden_button', object_id='#start_button'),
)


tile_processor = TileProcessor("assets/tiles/dungeon_sheet.png", "assets/sprites/electric_field1.png",
                               TILE_SIZE, scale_factor=4, danger_file2="assets/sprites/electric_field2.png",
                               danger_file3="assets/sprites/electric_field3.png")
maze_loader = MazeLoader()
maze_drawer = MazeDrawer(tile_map = tile_processor.create_tile_map(), tile_size=tile_processor.new_size)
maze_solver = 0

clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                if maze_solver:
                    maze_solver.gbfs()
                    pygame.display.flip()  # Asegurar que la pantalla se actualice después del BFS

                    #time.sleep(2)
                    #maze_drawer.move_charanter(2, 1, 2, 2)

            if event.ui_element == load_button:
                file_dialog = pygame_gui.windows.UIFileDialog(
                    rect=pygame.Rect((400, 200), (600, 400)),  # Tamaño y posición
                    manager=ui_manager,
                    initial_file_path=".",
                )

        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            print(f"File path picked: {event.text}")
            maze_loader.file_path = event.text
            maze_loader.load_maze()
            maze_solver = MazeSolver(maze_loader, maze_drawer)
            tile_processor.reload_tileset()
            maze_drawer.maze = maze_loader.render_maze
            maze_drawer.generate_fixed_map()
            file_dialog = None

        ui_manager.process_events(event)

    ui_manager.update(time_delta)
    screen.fill((47, 40, 58))

    if  maze_drawer.maze is not None:
        #draw_maze(screen, fixed_map, obstacle_map, tile_map, new_size)
        maze_drawer.draw_maze(screen)

    # pygame.draw.rect(screen, (161, 128, 114), presentation_rect)
    ui_manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()

