import pygame as pg
import sys
import random
from enum import Enum
ANCHO = 800
ALTO = 600
FPS = 60
levels = [  ['---X----'],
            [ 'XXXXXXXX', 
                'X--DD--X',
                'X--DD--X',
                'XXXXXXXX',
                '---DD---'
          ],
            [ 'DDDDDDDD',
                'DDDDDDDD',
                'DDDDDDDD',
                'DDDDDDDD'  
          ]
]
class Marcador(pg.sprite.Sprite):
    class Justificado():
        izquierda = 'I'
        derecha = 'D'
        centrado = 'C'
    def __init__(self, x, y, justificado = None, fontsize=25, color=(255,255,255)):
        super().__init__()
        self.fuente = pg.font.Font(None, fontsize)
        self.text = "0"
        self.color = color
        self.x = x
        self.y = y
        if not justificado:
            self.justificado = Marcador.Justificado.izquierda
        else:
            self.justificado = justificado
        self.image = None
        self.rect = None
    def update(self, dt):
        self.image = self.fuente.render(str(self.text), True, self.color)
        if self.justificado == Marcador.Justificado.izquierda:
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        elif self.justificado == Marcador.Justificado.derecha:
            self.rect = self.image.get_rect(topright=(self.x, self.y))
        else:
            self.rect = self.image.get_rect(midtop=(self.x, self.y))
class MarcadorH(pg.sprite.Sprite):
    plantilla = "{}"
    def __init__(self, x, y, justificado = "topleft", fontsize=25, color=(255,255,255)):
        super().__init__()
        self.fuente = pg.font.Font(None, fontsize)
        self.text = ""
        self.color = color
        self.x = x
        self.y = y
        self.justificado = justificado
        self.image = None
        self.rect = None
    def update(self, dt):
        self.image = self.fuente.render(self.plantilla.format(self.text), True, self.color)
        d = {self.justificado: (self.x, self.y)}
        self.rect = self.image.get_rect(**d)
class CuentaVidas(MarcadorH):
    plantilla = "Vidas: {}"
class Ladrillo(pg.sprite.Sprite):
    disfraces = ['greenTile.png', 'redTile.png', 'redTileBreak.png']
    def __init__(self, x, y, esBlando=True):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.esBlando = esBlando
        self.imagen_actual = 0 if self.esBlando else 1
        self.image = self.imagenes[self.imagen_actual]
        self.rect = self.image.get_rect(topleft=(x,y))
        self.numGolpes = 0
    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("./images/{}".format(fichero)))
        return imagenes
    def update(self, dt):
        if self.esBlando == False and self.numGolpes == 1:
            self.imagen_actual = 2
            self.image = self.imagenes[self.imagen_actual]
    def desaparece(self):
        self.numGolpes += 1
        return (self.numGolpes > 0 and self.esBlando) or (self.numGolpes > 1 and not self.esBlando)
class Raqueta(pg.sprite.Sprite):
    disfraces = ['electric00.png', 'electric01.png', 'electric02.png']
    def __init__(self, x, y):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.milisegundos_para_cambiar = 1000 // FPS * 5
        self.milisegundos_acumulados = 0
        self.image = self.imagenes[self.imagen_actual]
        self.rect = self.image.get_rect(centerx = x, bottom = y)
        self.vx = 7
    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("./images/{}".format(fichero)))
        return imagenes
    def update(self, dt):
        teclas_pulsadas = pg.key.get_pressed()
        if teclas_pulsadas[pg.K_LEFT]:
            self.rect.x -= self.vx
            self.vx +=1
            self.vx = min(self.vx, 15)
        elif teclas_pulsadas[pg.K_RIGHT]:
            self.rect.x += self.vx
            self.vx += 1
            self.vx = min(self.vx, 15)
        else:
            self.vx = 7
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= ANCHO:
            self.rect.right = ANCHO
        self.milisegundos_acumulados += dt
        if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
            self.imagen_actual += 1
            if self.imagen_actual >= len(self.disfraces):
                self.imagen_actual = 0
            self.milisegundos_acumulados = 0
        self.image = self.imagenes[self.imagen_actual]
class Bola(pg.sprite.Sprite):
    disfraces = ['ball1.png', 'ball2.png', 'ball3.png', 'ball4.png', 'ball5.png']
    class Estado():
        viva = 0
        agonizando = 1
        muerta = 2
    def __init__(self, x, y,):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.image = self.imagenes[self.imagen_actual]
        self.milisegundos_acumulados = 0
        self.milisegundos_para_cambiar = 1000 // FPS * 10
        self.rect = self.image.get_rect(center=(x,y))
        self.xOriginal = x
        self.yOriginal = y
        self.estado = Bola.Estado.viva
        self.vx = random.randint(5, 10) * random.choice([-1, 1])
        self.vy = random.randint(5, 10) * random.choice([-1, 1])
    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("./images/{}".format(fichero)))
        return imagenes
    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False)
        if len(candidatos) > 0:
            self.vy *= -1
        return candidatos
    def update(self, dt):
        if self.estado == Bola.Estado.viva:
            self.rect.x += self.vx
            self.rect.y += self.vy
            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.vx *= -1 
            if self.rect.top <= 0:
                self.vy *= -1
            if self.rect.bottom >= ALTO:
                self.estado = Bola.Estado.agonizando
                self.rect.bottom = ALTO
        elif self.estado == Bola.Estado.agonizando:
            self.milisegundos_acumulados += dt
            if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
                self.imagen_actual += 1
                self.milisegundos_acumulados = 0
                if self.imagen_actual >= len(self.disfraces):
                    self.estado = Bola.Estado.muerta
                    self.imagen_actual = 0
                self.image = self.imagenes[self.imagen_actual]
        else:
            self.rect.center = (self.xOriginal, self.yOriginal)
            self.vx = random.randint(5, 10) * random.choice([-1, 1])
            self.vy = random.randint(5, 10) * random.choice([-1, 1])
            self.estado = Bola.Estado.viva
class Game():
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.vidas = 3
        self.puntuacion = 0
        self.todoGrupo = pg.sprite.Group()
        self.grupoJugador = pg.sprite.Group()
        self.grupoLadrillos = pg.sprite.Group()
        self.level = 0
        self.disponer_ladrillos(levels[self.level])
        self.cuentaPuntos = MarcadorH(10,10, fontsize=50)
        self.cuentaVidas = CuentaVidas(790, 10, "topright", 50, (255, 255, 0))
        self.fondo = pg.image.load("./images/background.png")
        self.bola = Bola(ANCHO // 2, ALTO // 2)
        self.todoGrupo.add(self.bola)    
        self.raqueta = Raqueta(x = ANCHO//2, y = ALTO - 40)
        self.grupoJugador.add(self.raqueta)
        self.todoGrupo.add(self.grupoJugador, self.grupoLadrillos)
        self.todoGrupo.add(self.cuentaPuntos, self.cuentaVidas)
    def disponer_ladrillos(self, level):
        for fila, cadena in enumerate(level):
            for columna, caracter in enumerate(cadena):
                if caracter in 'DX':
                    x = 5 + (100 * columna)
                    y = 5 + (40 * fila)
                    ladrillo = Ladrillo(x, y, caracter == 'X')
                    self.grupoLadrillos.add(ladrillo)
    def bucle_principal(self):
        game_over = False
        reloj = pg.time.Clock()
        while not game_over and self.vidas > 0: 
            dt = reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True
            self.cuentaPuntos.text = self.puntuacion
            self.cuentaVidas.text = self.vidas 
            self.bola.prueba_colision(self.grupoJugador)
            tocados = self.bola.prueba_colision(self.grupoLadrillos)
            for ladrillo in tocados:
                self.puntuacion += 5
                if ladrillo.desaparece():
                    self.grupoLadrillos.remove(ladrillo)
                    self.todoGrupo.remove(ladrillo)
                    if len(self.grupoLadrillos) == 0:
                        self.level += 1
                        self.disponer_ladrillos(levels[self.level])
                        self.todoGrupo.add(self.grupoLadrillos)
            self.todoGrupo.update(dt)
            if self.bola.estado == Bola.Estado.muerta:
                self.vidas -= 1
            self.pantalla.blit(self.fondo, (0,0))
            self.todoGrupo.draw(self.pantalla)
            pg.display.flip()
if __name__ == '__main__':
    pg.init()
    game = Game()
    game.bucle_principal()