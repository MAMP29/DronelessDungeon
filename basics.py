import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RatCheese")

image = pygame.image.load("assets/sprites/swiss.png") # Cargar imagen
pygame.mixer.init() # Inicializar mixer
pygame.mixer.music.load("assets/music/background-music-for-mobile-casual-video-game-short-8-bit-music-164703.mp3") # Cargar música
pygame.mixer.music.play(1) # Reproducir música, -1 para infinito, 1 para una sola vez

x, y = 100, 100
speed = 5

clock = pygame.time.Clock()

# Crear clase
class Swiss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/swiss.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 100, 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

# Crear objeto y añadir a sprites
Swiss = Swiss()
sprites = pygame.sprite.Group()
sprites.add(Swiss)



running = True
while running:
    clock.tick(60) # Tiempo entre cada frame, limitar a 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: # Evento de tecla
            if event.key == pygame.K_w:
                print("Arriba")
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     print(f"Clic en {event.pos}")

        keys = pygame.key.get_pressed()  # Obtener teclas presionadas
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed
        if keys[pygame.K_UP]:
            y -= speed
        if keys[pygame.K_DOWN]:
            y += speed

    screen.fill((234, 221, 215))
    pygame.draw.rect(screen, (255, 0, 0), (x, x, 50, 50))  # Rectangulo rojo con movimiento
    pygame.draw.circle(screen, (0, 255, 0), (200, 200), 50)  # Círculo verde
    pygame.draw.line(screen, (0, 0, 255), (300, 300), (400, 400), 5)  # Línea azul
    screen.blit(image, (500, 500))

    # Dibujar sprites
    sprites.update()  # Llamar a update() del sprite
    sprites.draw(screen)  # Dibujar sprite en pantalla

    pygame.display.flip()


pygame.quit()
