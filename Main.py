import pygame
import random
import math
import os
from pygame import mixer
import sys

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Invasion Espacial")

# Ruta base (por si se usa subcarpeta 'assets')
if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS  # cuando se ejecuta como .exe
else:
    BASE_PATH = os.path.dirname(__file__)  # en modo desarrollo

ASSETS = os.path.join(BASE_PATH, "assets")

# Cargar imágenes con rutas absolutas
icono = pygame.image.load(os.path.join(ASSETS, "astronave.png"))
fondo = pygame.image.load(os.path.join(ASSETS, "Fondo.jpg"))
pygame.display.set_icon(icono)

# Música
mixer.music.load(os.path.join(ASSETS, "MusicaFondo.mp3"))
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Efecto de sonido de explosión
sonido_explosion = mixer.Sound(os.path.join(ASSETS, "explosion.wav"))

# Fuente
fuente = pygame.font.Font(os.path.join(ASSETS, "04B_30__.TTF"), 30)
fuente_final = pygame.font.Font(os.path.join(ASSETS, "Daydream.ttf"), 45)

# Cargar imagenes de misiles UNA vez
misil_img_jugador = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, "misil.png")), (32, 32))
misil_img_enemigo = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, "misil_enemigo.png")), (32, 32))

# --- Funciones para crear power-ups pixel art ---

def pantalla_inicio():
    imagen_inicio = pygame.image.load(os.path.join(ASSETS, "pantalla_inicio.png"))
    imagen_inicio = pygame.transform.scale(imagen_inicio, (ANCHO, ALTO))
    fuente_texto = pygame.font.Font(os.path.join(ASSETS, "space age.TTF"), 30)
    esperando = True

    while esperando:
        pantalla.blit(imagen_inicio, (0, 0))

        texto = fuente_texto.render("Presiona ENTER", True, (255, 255, 255))
        rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO - 50))
        pantalla.blit(texto, rect_texto)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False

        pygame.display.update()
        pygame.time.Clock().tick(30)

def menu_inicial():
    menu_activo = True
    fuente_menu = pygame.font.Font(os.path.join(ASSETS, "04B_30__.TTF"), 40)
    opciones_texto = ["JUGAR", "INSTRUCCIONES", "SALIR"]
    seleccion = 0  # índice opción seleccionada

    clock = pygame.time.Clock()

    while menu_activo:
        fondo_menu = pygame.image.load(os.path.join(ASSETS, "fondo_menu.png"))
        fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))
        pantalla.blit(fondo_menu, (0, 0))

        for i, texto_opcion in enumerate(opciones_texto):
            color = (255, 255, 0) if i == seleccion else (255, 255, 255)
            texto_render = fuente_menu.render(texto_opcion, True, color)
            rect = texto_render.get_rect(center=(ANCHO // 2, 200 + i * 100))
            pantalla.blit(texto_render, rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones_texto)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones_texto)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        menu_activo = False  # salir del menú y empezar juego
                    elif seleccion == 1:
                        mostrar_instrucciones()
                    elif seleccion == 2:
                        pygame.quit()
                        exit()

        pygame.display.update()
        clock.tick(30)


def wrap_text(text, font, max_width):
    """Divide un texto largo en varias líneas que quepan en max_width."""
    palabras = text.split(' ')
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        prueba_linea = linea_actual + palabra + " "
        if font.size(prueba_linea)[0] <= max_width:
            linea_actual = prueba_linea
        else:
            lineas.append(linea_actual)
            linea_actual = palabra + " "
    if linea_actual:
        lineas.append(linea_actual)
    return lineas

def mostrar_instrucciones():
    mostrando = True
    fuente_texto = pygame.font.Font(os.path.join(ASSETS, "04B_30__.TTF"), 24)
    texto_largo = (
        "Usa las flechas izquierda y derecha para mover la nave.\n"
        "Pulsa espacio para disparar.\n"
        "Elimina a todos los enemigos y evita que lleguen abajo.\n"
        "Recoge power-ups para mejorar.\n"
        "Pulsa ESC para volver al menú."
    )
    lineas_raw = texto_largo.split('\n')
    max_width = 700
    lineas = []
    for linea in lineas_raw:
        lineas.extend(wrap_text(linea, fuente_texto, max_width))

    clock = pygame.time.Clock()

    while mostrando:
        pantalla.fill((0, 0, 0))
        for i, linea in enumerate(lineas):
            txt_render = fuente_texto.render(linea, True, (255, 255, 255))
            pantalla.blit(txt_render, (50, 50 + i * 40))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    mostrando = False

        pygame.display.update()
        clock.tick(30)

def menu_pausa():
    pausado = True
    fuente_menu = pygame.font.Font(os.path.join(ASSETS, "04B_30__.TTF"), 50)
    opciones_texto = ["Continuar", "Salir"]
    seleccion = 0
    clock = pygame.time.Clock()

    while pausado:
        pantalla.fill((30, 30, 30))  # fondo oscuro semi-transparente
        for i, texto_opcion in enumerate(opciones_texto):
            color = (255, 255, 0) if i == seleccion else (255, 255, 255)
            texto_render = fuente_menu.render(texto_opcion, True, color)
            rect = texto_render.get_rect(center=(ANCHO // 2, 200 + i * 100))
            pantalla.blit(texto_render, rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones_texto)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones_texto)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        pausado = False  # continuar juego
                    elif seleccion == 1:
                        pygame.quit()
                        exit()

        pygame.display.update()
        clock.tick(30)

def crear_powerup_triple():
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    surf.fill((0, 0, 255))  # azul fondo
    for x in [6, 15, 24]:
        pygame.draw.circle(surf, (255, 255, 255), (x, 16), 4)
    return surf

def crear_powerup_rapido():
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    surf.fill((0, 128, 0))  # verde fondo
    points = [(14,4), (18,12), (12,12), (16,20), (10,20)]  # forma rayo
    pygame.draw.polygon(surf, (255, 255, 0), points)
    return surf

def crear_powerup_vida():
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    surf.fill((255, 0, 0))  # rojo fondo
    pygame.draw.circle(surf, (255,255,255), (10,12), 6)
    pygame.draw.circle(surf, (255,255,255), (22,12), 6)
    pygame.draw.polygon(surf, (255,255,255), [(4,18),(28,18),(16,30)])
    return surf

# Clases
class Jugador:
    def __init__(self):
        self.x = 368
        self.y = 500
        self.velocidad = 5
        self.mov_x = 0
        self.vidas = 3
        self.imagen = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSETS, "nave-espacial.png")).convert_alpha(), (64, 64)
        )

    def mover(self):
        self.x += self.mov_x
        self.x = max(0, min(self.x, ANCHO - 64))

    def dibujar(self):
        pantalla.blit(self.imagen, (self.x, self.y))

    def mostrar_vidas(self):
        for i in range(self.vidas):
            corazon = pygame.transform.scale(
                pygame.image.load(os.path.join(ASSETS, "corazon.png")).convert_alpha(), (32, 32)
            )
            x_pos = ANCHO - 10 - (i + 1) * 40
            pantalla.blit(corazon, (x_pos, 10))

class Enemigo:
    def __init__(self, imagen_file):
        ruta = os.path.join(ASSETS, imagen_file)
        self.imagen = pygame.transform.scale(pygame.image.load(ruta).convert_alpha(), (64, 64))
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 200)
        self.velocidad_x = 1.4
        self.velocidad_y = 70

    def mover(self):
        self.x += self.velocidad_x
        if self.x <= 0 or self.x >= 736:
            self.velocidad_x *= -1
            self.y += self.velocidad_y

    def dibujar(self):
        pantalla.blit(self.imagen, (self.x, self.y))

    def reset(self):
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)

class EnemigoZigZag(Enemigo):
    def __init__(self, imagen_file):
        super().__init__(imagen_file)
        self.tiempo = 0
        self.velocidad_y = 0.7  # velocidad vertical aumentada

    def mover(self):
        self.tiempo += 1
        self.x += math.sin(self.tiempo * 0.1) * 5  # movimiento horizontal más rápido y amplio
        self.y += self.velocidad_y
        # Mantener dentro de pantalla
        if self.x <= 0:
            self.x = 0
        elif self.x >= ANCHO - 80:
            self.x = ANCHO - 80

class EnemigoDisparador(Enemigo):
    def __init__(self, imagen_file):
        super().__init__(imagen_file)
        self.tiempo_disparo = 0
        self.cooldown = random.randint(100, 200)
        self.sonido_disparo = mixer.Sound(os.path.join(ASSETS, "disparo.mp3"))

    def actualizar(self, balas_enemigas):
        self.tiempo_disparo += 1
        if self.tiempo_disparo > self.cooldown:
            bala = {
                "x": self.x + 16,
                "y": self.y + 32,
                "velocidad": 3
            }
            balas_enemigas.append(bala)
            self.sonido_disparo.play()
            self.tiempo_disparo = 0
            self.cooldown = random.randint(100, 200)

class JefeFinal:
    def __init__(self):
        self.imagen = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSETS, "jefe.png")).convert_alpha(), (128, 128)
        )
        self.x = random.randint(100, 600)
        self.y = -150
        self.vida = 20
        self.visible = False
        self.direccion = 1
        self.cooldown = 90
        self.tiempo_disparo = 0
        self.sonido_disparo = mixer.Sound(os.path.join(ASSETS, "disparo.mp3"))

    def aparecer(self):
        self.visible = True
        self.x = random.randint(100, 600)
        self.y = -150
        self.vida = 20

    def mover(self):
        if self.visible:
            self.y += 0.3
            self.x += self.direccion
            if self.x <= 0 or self.x >= ANCHO - 128:
                self.direccion *= -1

    def dibujar(self):
        if self.visible:
            pantalla.blit(self.imagen, (self.x, self.y))

    def actualizar(self, balas_enemigas):
        if self.visible:
            self.tiempo_disparo += 1
            if self.tiempo_disparo >= self.cooldown:
                # Disparo recto, diagonal izquierda, diagonal derecha
                balas_enemigas.append({"x": self.x + 64, "y": self.y + 100, "vx": 0, "vy": 3})
                balas_enemigas.append({"x": self.x + 64, "y": self.y + 100, "vx": -2, "vy": 3})
                balas_enemigas.append({"x": self.x + 64, "y": self.y + 100, "vx": 2, "vy": 3})
                self.sonido_disparo.play()
                self.tiempo_disparo = 0

    def recibir_dano(self, danio):
        self.vida -= danio
        if self.vida <= 0:
            self.visible = False
            return True
        return False

class Bala:
    def __init__(self, x, y, tipo="normal"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidad = -6 if tipo != "rapido" else -10
        self.imagen = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSETS, "misil.png")).convert_alpha(), (32, 32)
        )

    def mover(self):
        self.y += self.velocidad

    def dibujar(self):
        pantalla.blit(self.imagen, (self.x, self.y))

    def fuera_de_pantalla(self):
        return self.y < -32

class PowerUp:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.imagen = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, f"powerup_{tipo}.png")), (32, 32))
        self.velocidad = 1

    def mover(self):
        self.y += self.velocidad

    def dibujar(self):
        pantalla.blit(self.imagen, (self.x, self.y))

    def fuera_de_pantalla(self):
        return self.y > ALTO

class Explosion:
    def __init__(self, x, y):
        self.frames = []
        for i in range(1, 9):  # Asegúrate de tener 8 imágenes: explosion1.png, ..., explosion8.png
            ruta = os.path.join(ASSETS, "explosion{}.png".format(i))
            imagen = pygame.transform.scale(pygame.image.load(ruta), (80, 80))
            self.frames.append(imagen)
        self.index = 0
        self.x = x
        self.y = y
        self.tiempo_entre_frames = 50  # milisegundos
        self.ultimo_update = pygame.time.get_ticks()
        self.completada = False

    def actualizar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_update > self.tiempo_entre_frames:
            self.index += 1
            self.ultimo_update = ahora
            if self.index >= len(self.frames):
                self.completada = True

    def dibujar(self):
        if not self.completada:
            pantalla.blit(self.frames[self.index], (self.x, self.y))

# Funciones

def detectar_colision(x1, y1, x2, y2):
    distancia = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distancia < 27

def mostrar_puntuacion(puntuacion):
    texto = fuente.render(f"Puntuacion: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(texto, (10, 10))

def texto_final(puntuacion):
    final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(final, (200, 250))
    final_puntaje = fuente.render(f"Puntuacion final: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(final_puntaje, (180, 350))

# Inicialización
def reiniciar_juego():
    global jugador, balas, balas_enemigas, powerups, puntuacion, modo_disparo
    global jefe, tiempo_ultimo_jefe, tiempo_entre_jefes, enemigos, oleada_actual, TIEMPO_ULTIMA_OLEADA
    global espacios_ocupados, ultimo_disparo, tiempo_powerup

pantalla_inicio()
menu_inicial()
reiniciar_juego()
jugador = Jugador()
balas = []
balas_enemigas = []
powerups = []
puntuacion = 0
modo_disparo = "normal"
tiempo_powerup = 0
jefe = JefeFinal()
tiempo_ultimo_jefe = pygame.time.get_ticks()
tiempo_entre_jefes = random.randint(30000, 60000)

oleada_actual = 0
enemigos = []
OLEADA_DURACION = 30_000  # 30 segundos
TIEMPO_ULTIMA_OLEADA = pygame.time.get_ticks()

espacios_ocupados = []  # para evitar solapamiento

sonido_bala = mixer.Sound(os.path.join(ASSETS, "disparo.mp3"))

# Cooldown para disparo del jugador
ultimo_disparo = 0
cooldown_disparo = 250  # milisegundos entre disparos

def generar_oleada(numero):
    nuevos_enemigos = []
    espacios_ocupados.clear()

    def posicion_disponible():
        for intento in range(100):
            x = random.randint(0, ANCHO - 64)
            y = random.randint(50, 150)
            solapado = any(abs(x - ex) < 70 and abs(y - ey) < 70 for ex, ey in espacios_ocupados)
            if not solapado:
                espacios_ocupados.append((x, y))
                return x, y
        return random.randint(0, ANCHO - 64), random.randint(50, 150)

    for _ in range(5 + numero):
        enemigo_normal = Enemigo("enemigo.png")
        enemigo_normal.velocidad = 2.0 + 0.2 * numero
        enemigo_normal.x, enemigo_normal.y = posicion_disponible()
        nuevos_enemigos.append(enemigo_normal)

    for _ in range(3 + numero // 2):
        enemigo_disparador = EnemigoDisparador("enemigo3.png")
        enemigo_disparador.x, enemigo_disparador.y = posicion_disponible()
        nuevos_enemigos.append(enemigo_disparador)

    for i in range(3):
        zigzag = EnemigoZigZag("enemigo2.png")
        zigzag.x, zigzag.y = posicion_disponible()
        nuevos_enemigos.append(zigzag)

    return nuevos_enemigos

enemigos = generar_oleada(oleada_actual)

reloj = pygame.time.Clock()
jugando = True

misil_img_enemigo = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS, "misil_enemigo.png")).convert_alpha(), (32, 32))

while True:
    menu_inicial()
    reiniciar_juego()
    jugador = Jugador()
    balas = []
    balas_enemigas = []
    powerups = []
    puntuacion = 0
    modo_disparo = "normal"
    tiempo_powerup = 0
    jefe = JefeFinal()
    tiempo_ultimo_jefe = pygame.time.get_ticks()
    tiempo_entre_jefes = random.randint(30000, 60000)

    oleada_actual = 0
    enemigos = []
    OLEADA_DURACION = 30_000  # 30 segundos
    TIEMPO_ULTIMA_OLEADA = pygame.time.get_ticks()

    espacios_ocupados = []  # para evitar solapamiento
    jugando = True

    while jugando:
        pantalla.blit(fondo, (0, 0))
        tiempo_actual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones_texto)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones_texto)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        pausado = False
                    elif seleccion == 1:
                        reiniciar_juego()
                        pausado = False
                    elif seleccion == 2:
                        pygame.quit()
                        exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    menu_pausa()
                if evento.key == pygame.K_LEFT:
                    jugador.mov_x = -jugador.velocidad
                if evento.key == pygame.K_RIGHT:
                    jugador.mov_x = jugador.velocidad
                if evento.key == pygame.K_SPACE:
                    ahora = pygame.time.get_ticks()
                    if ahora - ultimo_disparo > cooldown_disparo:
                        sonido_bala.play()
                        if modo_disparo == "normal":
                            balas.append(Bala(jugador.x, jugador.y))
                        elif modo_disparo == "triple":
                            balas.append(Bala(jugador.x + 8, jugador.y, tipo="normal"))
                            balas.append(Bala(jugador.x + 24, jugador.y, tipo="normal"))
                            balas.append(Bala(jugador.x + 40, jugador.y, tipo="normal"))
                        elif modo_disparo == "rapido":
                            balas.append(Bala(jugador.x, jugador.y, tipo="rapido"))
                        ultimo_disparo = ahora
            if evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    jugador.mov_x = 0

        jugador.mover()
        jugador.dibujar()
        jugador.mostrar_vidas()

        if not jefe.visible and tiempo_actual > tiempo_ultimo_jefe + tiempo_entre_jefes:
            jefe.aparecer()
            tiempo_ultimo_jefe = tiempo_actual
            tiempo_entre_jefes = random.randint(30000, 60000)

        jefe.mover()
        jefe.actualizar(balas_enemigas)
        jefe.dibujar()

        for bala in balas[:]:
            if jefe.visible and math.hypot(jefe.x - bala.x, jefe.y - bala.y) < 50:
                jefe.recibir_dano(1)
                balas.remove(bala)
                puntuacion += 1

        for enemigo in enemigos[:]:
            enemigo.mover()
            if enemigo.y + 64 >= jugador.y:
                jugador.vidas -= 1
                enemigos.remove(enemigo)
                if jugador.vidas <= 0:
                    iniciar_animacion_explosion(jugador.x, jugador.y)
                    mostrar_game_over()
                    pantalla_inicio()
                    menu_inicial()
                    reiniciar_juego()
                    continue  # saltar al siguiente frame del bucle principal
            enemigo.dibujar()

            if isinstance(enemigo, EnemigoDisparador):
                enemigo.actualizar(balas_enemigas)

            for bala in balas[:]:
                if detectar_colision(enemigo.x, enemigo.y, bala.x, bala.y):
                    balas.remove(bala)
                    puntuacion += 1
                    enemigo.reset()
                    if random.random() < 0.2:
                        tipo = random.choice(["triple", "rapido", "vida"])
                        powerups.append(PowerUp(enemigo.x, enemigo.y, tipo))

        for bala in balas[:]:
            bala.mover()
            bala.dibujar()
            if bala.fuera_de_pantalla():
                balas.remove(bala)

        for ebala in balas_enemigas[:]:
            ebala.setdefault("vx", 0)
            ebala.setdefault("vy", 3)
            ebala["x"] += ebala["vx"]
            ebala["y"] += ebala["vy"]
            pantalla.blit(misil_img_enemigo, (ebala["x"], ebala["y"]))
            if ebala["y"] > ALTO:
                balas_enemigas.remove(ebala)
            elif detectar_colision(jugador.x, jugador.y, ebala["x"], ebala["y"]):
                balas_enemigas.remove(ebala)
                jugador.vidas -= 1
                if jugador.vidas <= 0:
                    sonido_explosion.play()
                    explosion_jugador = Explosion(jugador.x, jugador.y)
                    while not explosion_jugador.completada:
                        pantalla.blit(fondo, (0, 0))
                        explosion_jugador.actualizar()
                        explosion_jugador.dibujar()
                        mostrar_puntuacion(puntuacion)
                        pygame.display.update()
                        reloj.tick(60)
                    texto_final(puntuacion)
                    pygame.display.update()
                    pygame.time.delay(3000)
                    jugando = False

        for pu in powerups[:]:
            pu.mover()
            pu.dibujar()
            if pu.fuera_de_pantalla():
                powerups.remove(pu)
            if detectar_colision(jugador.x, jugador.y, pu.x, pu.y):
                if pu.tipo == "vida" and jugador.vidas < 5:
                    jugador.vidas += 1
                else:
                    modo_disparo = pu.tipo
                    tiempo_powerup = pygame.time.get_ticks()
                powerups.remove(pu)

        if modo_disparo != "normal" and pygame.time.get_ticks() - tiempo_powerup > 10000:
            modo_disparo = "normal"

        if tiempo_actual - TIEMPO_ULTIMA_OLEADA > OLEADA_DURACION or len(enemigos) == 0:
            oleada_actual += 1
            enemigos = generar_oleada(oleada_actual)
            TIEMPO_ULTIMA_OLEADA = tiempo_actual

        mostrar_puntuacion(puntuacion)
        pygame.display.update()
        reloj.tick(60)

