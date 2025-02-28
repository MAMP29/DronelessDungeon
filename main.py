import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from logic.load_file import load_data, control_size
from logic.tiles_processer import load_tileset, create_tile_map, reload_tileset
from logic.Maze import draw_maze, generate_fixed_map

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

# Cargar titles
tiles, new_size = load_tileset("assets/tiles/dungeon_sheet.png", "assets/sprites/swiss.png",TILE_SIZE, scale_factor=1)
print("Tiles:", len(tiles))
tile_map = create_tile_map(tiles) if tiles else {}
maze = None
fixed_map = None
obstacle_map = None

clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                print("Start button pressed")
            if event.ui_element == load_button:
                file_dialog = pygame_gui.windows.UIFileDialog(
                    rect=pygame.Rect((400, 200), (600, 400)),  # Tamaño y posición
                    manager=ui_manager,
                    initial_file_path=".",
                )

        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            print(f"File path picked: {event.text}")
            path = event.text
            maze = load_data(path)
            size = control_size(maze)
            tiles, new_size = reload_tileset("assets/tiles/dungeon_sheet.png", "assets/sprites/swiss.png",TILE_SIZE, scale_factor=size)
            tile_map = create_tile_map(tiles) if tiles else {}
            fixed_map, obstacle_map = generate_fixed_map(maze, tile_map)
            file_dialog = None

        ui_manager.process_events(event)

    ui_manager.update(time_delta)
    screen.fill((47, 40, 58))

    if "floor" in tile_map and fixed_map is not None:
        draw_maze(screen, fixed_map, obstacle_map, tile_map, new_size)

    # pygame.draw.rect(screen, (161, 128, 114), presentation_rect)
    ui_manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()

