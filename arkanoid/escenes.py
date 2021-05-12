from arkanoid import ANCHO, ALTO, levels, FPS
from arkanoid.entities import Marcador, Bola, Raqueta, Ladrillo
import pygame as pg

import sys

class Escene():
    def __init__(self, pantalla):
        self.todoGrupo = pg.sprite.Group()
        self.reloj = pg.time.Clock()

    def reset(self):
        pass

    def maneja_eventos(self):
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                return True
            if evento.type == pg.QUIT or \
                evento.type == pg.KEYDOWN and evento.key == pg.K_q:
                    pg.quit()
                    sys.exit()

        return False

    def reset(self):
        pass

    def bucle_principal(self):
        pass
        """
        while True:
            self.maneja_eventos()
            self.todoGrupo.update(dt)
            self.todoGrupo.draw(self.pantalla)
            pg.display.flip()
        """

class Game():
class Game(Escene):
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.todoGrupo = pg.sprite.Group()
        self.vidas = 3
        self.puntuacion = 0
        super().__init__(pantalla)
        self.grupoJugador = pg.sprite.Group()
        self.grupoLadrillos = pg.sprite.Group()
        self.level = 0

        self.disponer_ladrillos(levels[self.level])

        self.cuentaPuntos = Marcador(10,10, fontsize=50)
        self.cuentaVidas = Marcador(790, 10, "topright", 50, (255, 255, 0))
        self.raqueta = Raqueta(x = ANCHO//2, y = ALTO - 40)
        self.grupoJugador.add(self.raqueta)

        self.todoGrupo.add(self.grupoJugador, self.grupoLadrillos)
        self.todoGrupo.add(self.grupoJugador)
        

    def reset(self):
        self.vidas = 3
        self.puntuacion = 0
        self.level = 0
        self.todoGrupo.remove(self.grupoLadrillos)
        self.grupoLadrillos.empty()
        self.disponer_ladrillos(levels[self.level])
        self.todoGrupo.add(self.grupoLadrillos)
        self.todoGrupo.remove(self.cuentaPuntos, self.cuentaVidas)
        self.todoGrupo.add(self.cuentaPuntos, self.cuentaVidas)



    def disponer_ladrillos(self, level):
        for fila, cadena in enumerate(level):
            for columna, caracter in enumerate(cadena):

    def bucle_principal(self):
        game_over = False
        reloj = pg.time.Clock()
        while not game_over and self.vidas > 0: 
            dt = reloj.tick(FPS)
            dt = self.reloj.tick(FPS)

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True
            self.maneja_eventos()

            self.cuentaPuntos.text = self.puntuacion
            self.cuentaVidas.text = self.vidas 

            pg.display.flip()

class Portada():
class Portada(Escene):
    def __init__(self, pantalla):
        self.pantalla = pantalla
        super().__init__(pantalla)
        self.instrucciones = Marcador(ANCHO // 2, ALTO // 2, "center", 50, (255, 255, 0))
        self.instrucciones.text = "Pulsa espacio para jugar"
        self.todoGrupo = pg.sprite.Group()
        self.todoGrupo.add(self.instrucciones)
        self.reloj = pg.time.Clock()


    def bucle_principal(self):
        game_over = False
        while not game_over:
            dt = self.reloj.tick(FPS)

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True  
                    #TODO hay que arreglar que nos tire del juego
            self.maneja_eventos()

            teclas_pulsadas = pg.key.get_pressed()
            if teclas_pulsadas[pg.K_SPACE]:
