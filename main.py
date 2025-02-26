import pygame
import pygame_gui
from pygame_gui.core import ObjectID

pygame.init()

WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RatCheese")

ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT), "Assets/themes.json")

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

        ui_manager.process_events(event)

    ui_manager.update(time_delta)
    screen.fill((234, 221, 215))

    # pygame.draw.rect(screen, (161, 128, 114), presentation_rect)
    ui_manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
