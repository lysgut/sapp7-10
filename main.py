import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Atrapa los Reciclables")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Cargar imágenes
fondo = pygame.image.load("fondo.jpg")
contenedor_img = pygame.image.load("contenedor.png")
reciclable_img = pygame.image.load("reciclable.png")
contaminante_img = pygame.image.load("contaminante.png")

# Escalar imágenes
contenedor_img = pygame.transform.scale(contenedor_img, (100, 80))
reciclable_img = pygame.transform.scale(reciclable_img, (50, 50))
contaminante_img = pygame.transform.scale(contaminante_img, (50, 50))

# Fuente
fuente = pygame.font.Font(None, 40)

# Sonido (opcional)
try:
    punto_sonido = pygame.mixer.Sound("punto.wav")
except:
    punto_sonido = None

# Variables del jugador
contenedor_x = ANCHO // 2 - 50
contenedor_y = ALTO - 100
velocidad = 7

# Variables de los objetos
obj_x = random.randint(0, ANCHO - 50)
obj_y = -50
obj_velocidad = 5
es_reciclable = True

# Puntuación y vidas
puntos = 0
vidas = 3

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal del juego
while True:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento del contenedor
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and contenedor_x > 0:
        contenedor_x -= velocidad
    if teclas[pygame.K_RIGHT] and contenedor_x < ANCHO - 100:
        contenedor_x += velocidad

    # Movimiento del objeto
    obj_y += obj_velocidad

    # Reiniciar objeto si cae fuera de pantalla
    if obj_y > ALTO:
        obj_y = -50
        obj_x = random.randint(0, ANCHO - 50)
        es_reciclable = random.choice([True, False])

    # Rectángulos para detección de colisiones
    cont_rect = pygame.Rect(contenedor_x, contenedor_y, 100, 80)
    obj_rect = pygame.Rect(obj_x, obj_y, 50, 50)

    # Colisión
    if cont_rect.colliderect(obj_rect):
        if es_reciclable:
            puntos += 1
            if punto_sonido:
                punto_sonido.play()
        else:
            vidas -= 1

        # Reiniciar objeto tras colisión
        obj_y = -50
        obj_x = random.randint(0, ANCHO - 50)
        es_reciclable = random.choice([True, False])

    # Dibujar fondo
    pantalla.blit(fondo, (0, 0))

    # Dibujar contenedor y objeto
    pantalla.blit(contenedor_img, (contenedor_x, contenedor_y))
    if es_reciclable:
        pantalla.blit(reciclable_img, (obj_x, obj_y))
    else:
        pantalla.blit(contaminante_img, (obj_x, obj_y))

    # Mostrar puntaje y vidas
    texto = fuente.render(f"Puntos: {puntos} | Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

    # Game over
    if vidas <= 0:
        game_over = fuente.render("💀 GAME OVER 💀", True, BLANCO)
        pantalla.blit(game_over, (ANCHO // 2 - 100, ALTO // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        puntos = 0
        vidas = 3

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(30)
