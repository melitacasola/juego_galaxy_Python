import pygame
import random
import math
from pygame import mixer

# inicializar pygame
pygame.init()


# crear pantalla
pantalla = pygame.display.set_mode((800,600))


# titulo e icono
pygame.display.set_caption('Invasión Espacial')
icono = pygame.image.load('cohete-espacial.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Fondo.jpg')

#agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)


# variables de movimiento del jugador
img_jugador = pygame.image.load('nave-espacial.png')
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0
jugador_y_cambio = 0

# variables de movimiento del ovni
img_ovni = []
ovni_x = []
ovni_y = []
ovni_x_cambio = []
ovni_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_ovni.append(pygame.image.load('ovni.png'))
    ovni_x.append(random.randint(0, 736))
    ovni_y.append(random.randint(50, 200))
    ovni_x_cambio.append(0.7)
    ovni_y_cambio.append(50)

# variables de movimiento de las balas
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_disparada = False

#puntaje
puntaje = 0
fuente = pygame.font.Font('RubikGlitch-Regular.ttf', 28)
cord_x = 10
cord_y = 10

#texto final de juego
fuente_final = pygame.font.Font('RubikGlitch-Regular.ttf', 50)

def texto_final():
    mi_fuente = fuente_final.render("JUEGO TERMINADO", True, (78, 239, 22))
    pantalla.blit(mi_fuente, (130, 200))


#func mostrar ptje
def mostrar_ptje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (78, 239, 22))
    pantalla.blit(texto, (x,y))


# func jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))
    #jugador al medio de la pantalla 800/2 = 400/(64/2)=368

# func ovni
def ovni(x, y, ene):
    pantalla.blit(img_ovni[ene], (x, y))


# func  disparar bala
def disparar_bala(x, y):
    global bala_disparada
    bala_disparada = True
    pantalla.blit(img_bala, (x+16, y+10))


# func detectar colisiones
def hay_cosilion(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_1 - y_2, 2))
    if distancia < 27:
        return True
    else:
        return False



# loop del juego - p/ actualizar el juego dentro del loop
se_ejecuta = True

while se_ejecuta:
    #RGB pantalla - primera p/ qe no superponga iconos
    #pantalla.fill((34, 9, 72))
    pantalla.blit(fondo, (0,0))


    #iterar eventos
    for evento in pygame.event.get():

        #evento cerrar ventana:
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        #tecla evento:
        if evento.type == pygame.KEYDOWN:
            #sobre eje x
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1

            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                #hacemos falso a la bala visible p/ qe no reinicie ycambie
                if not bala_disparada:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

            #sobre eje y
            if evento.key == pygame.K_DOWN:
                jugador_y_cambio = -1

            if evento.key == pygame.K_UP:
                jugador_y_cambio = 1


        #evento soltar tecla
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
            if evento.key == pygame.K_DOWN or evento.key == pygame.K_UP:
                jugador_y_cambio = 0

    #modif ubicacion
    jugador_x += jugador_x_cambio
    jugador_y -= jugador_y_cambio

    #mantener en la pantalla jugador
    #sobre eje x
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    #sobre eje y
    if jugador_y <= 0:
        jugador_y = 0
    elif jugador_y >= 536:
        jugador_y = 536


    #ubicacin del enemigo
    for e in range(cantidad_enemigos):

        #fin juego
        if ovni_y[e] > 450:
            for k in range(cantidad_enemigos):
                ovni_y[k] = 800
            texto_final()
            break

        ovni_x[e] += ovni_x_cambio[e]
        #mantener en la pantalla enemigo y mueva solo
        if ovni_x[e] <= 0:
            ovni_x_cambio[e] = 0.7
            ovni_y[e] += ovni_y_cambio[e]
        elif ovni_x[e] >= 736:
            ovni_x_cambio[e] = -0.7
            ovni_y[e] += ovni_y_cambio[e]

            # colision
        colision = hay_cosilion(ovni_x[e], ovni_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_disparada = False
            puntaje += 1
            ovni_x[e] = random.randint(0, 736)
            ovni_y[e] = random.randint(50, 200)

        ovni(ovni_x[e], ovni_y[e], e)

    #movimiento bala
    if bala_y <= -64:
        #reestablece posicion
        bala_y = 500
        bala_disparada = False

    if bala_disparada:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio



    jugador(jugador_x, jugador_y)

    mostrar_ptje(cord_x, cord_x)

    #actualizar
    pygame.display.update()