import pygame
import random
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.posMatriz = pos
        self.posInicial = [pos.x, pos.y]
        self.posPixel = self.get_posPixel()
        self.number = number
        self.direccion = vec(0, 0)
        self.objetivo = None
        self.speed = 4
        self.enemigos = pygame.image.load('enemigos.png')
        self.enemigos = pygame.transform.scale(
            self.enemigos, (self.app.cell_width, self.app.cell_height))

    def actualizar(self):
        self.objetivo = self.set_objetivo()
        if self.objetivo != self.posMatriz:
            self.posPixel += self.direccion * self.speed
            if self.puedeMover():
                self.mover()
        self.posMatriz[0] = (self.posPixel[0] +
                             self.app.cell_width // 2) // self.app.cell_width-1
        self.posMatriz[1] = (self.posPixel[1] +
                             self.app.cell_height // 2) // self.app.cell_height-1

    def draw(self):
        self.app.screen.blit(
            self.enemigos, (int(self.posPixel.x-self.app.cell_width), int(self.posPixel.y-self.app.cell_width)))
        pygame.draw.rect(self.app.screen, RED, (self.posMatriz[0]*self.app.cell_width,
                                                self.posMatriz[1]*self.app.cell_height,
                                                self.app.cell_width, self.app.cell_height), 1)

    def set_objetivo(self):
        return self.app.player.posMatriz

    def puedeMover(self):
        if int(self.posPixel.x) % self.app.cell_width == 0:
            if self.direccion == vec(1, 0) or self.direccion == vec(-1, 0) or self.direccion == vec(0, 0):
                return True
        if int(self.posPixel.y) % self.app.cell_height == 0:
            if self.direccion == vec(0, 1) or self.direccion == vec(0, -1) or self.direccion == vec(0, 0):
                return True
        return False

    def mover(self):
        self.direccion = self.darDireccion(self.objetivo)

    def darDireccion(self, objetivo):
        celdaSiguiente = self.posSiguiente(objetivo)
        xdir = celdaSiguiente[0] - self.posMatriz[0]
        ydir = celdaSiguiente[1] - self.posMatriz[1]
        return vec(xdir, ydir)

    def posSiguiente(self, objetivo):
        camino = self.amplitud([int(self.posMatriz.x), int(self.posMatriz.y)], [
            int(objetivo[0]), int(objetivo[1])])
        return camino[1]

    def amplitud(self, inicio, objetivo):
        matriz = [[0 for x in range(COLS)] for x in range(ROWS)]
        for celda in self.app.paredes:
            if celda.x < COLS and celda.y < ROWS:
                matriz[int(celda.y)][int(celda.x)] = 1
        queue = [inicio]
        camino = []
        visitado = []
        while queue:
            actual = queue[0]
            queue.remove(queue[0])
            visitado.append(actual)
            if actual == objetivo:
                break
            else:
                vecinos = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for vecino in vecinos:
                    if vecino[0]+actual[0] >= 0 and vecino[0] + actual[0] < len(matriz[0]):
                        if vecino[1]+actual[1] >= 0 and vecino[1] + actual[1] < len(matriz):
                            celdaSiguiente = [vecino[0] + actual[0], vecino[1] + actual[1]]
                            if celdaSiguiente not in visitado:
                                if matriz[celdaSiguiente[1]][celdaSiguiente[0]] != 1:
                                    queue.append(celdaSiguiente)
                                    camino.append({"actual": actual, "Siguiente": celdaSiguiente})
        caminoCorto = [objetivo]
        while objetivo != inicio:
            for paso in camino:
                if paso["Siguiente"] == objetivo:
                    objetivo = paso["actual"]
                    caminoCorto.insert(0, paso["actual"])
        return caminoCorto

    def get_posPixel(self):
        return vec((self.posMatriz.x * self.app.cell_width) + self.app.cell_width,
                   (self.posMatriz.y * self.app.cell_height) +
                   self.app.cell_height)
