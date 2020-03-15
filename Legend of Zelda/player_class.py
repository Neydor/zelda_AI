import pygame
import math
from settings import *

vec = pygame.math.Vector2


class Nodo:
    def __init__(self, padre, x, y):
        self.f = 0
        self.padre = None
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.posicionInicial = [pos.x, pos.y]
        self.posMatriz = pos
        self.posPixel = self.get_posPixel()
        self.objetivo = self.app.llaves[0]
        self.direccion = vec(0, 0)
        self.casillaDisponible = True
        self.velocidad = 5
        self.personaje = pygame.image.load('person.png')
        self.personaje = pygame.transform.scale(
            self.personaje, (self.app.cell_width, self.app.cell_height))

    def actualizar(self):
        if self.casillaDisponible:
            self.posPixel += self.direccion * self.velocidad
        if self.puedeMover():
            self.mover()
            self.casillaDisponible = self.hayPared()
        self.posMatriz[0] = (self.posPixel[0] +
                             self.app.cell_width//2)//self.app.cell_width - 1
        self.posMatriz[1] = (self.posPixel[1] +
                             self.app.cell_height//2)//self.app.cell_height - 1
        if self.enLlave():
            self.cogerLlave()

    def draw(self):
        self.app.screen.blit(self.personaje, (int(self.posPixel.x - self.app.cell_width),
                                              int(self.posPixel.y - self.app.cell_width)))
        pygame.draw.rect(self.app.screen, RED, (self.posMatriz[0]*self.app.cell_width,
                                                self.posMatriz[1]*self.app.cell_height,
                                                self.app.cell_width, self.app.cell_height), 1)

    def enLlave(self):
        if self.posMatriz in self.app.llaves:
            if int(self.posPixel.x) % self.app.cell_width == 0:
                if self.direccion == vec(1, 0) or self.direccion == vec(-1, 0):
                    return True
            if int(self.posPixel.y) % self.app.cell_height == 0:
                if self.direccion == vec(0, 1) or self.direccion == vec(0, -1):
                    return True
        return False

    def cogerLlave(self):
        self.app.llaves.remove(self.posMatriz)

    def matarEnemigo(self, enemigos):
        enemigoMuelto = []
        posActual = [self.posMatriz.x, self.posMatriz.y]
        vecinos = [vec(0+posActual[0], -1+posActual[1]), vec(1+posActual[0], 0+posActual[1]),
                   vec(0+posActual[0], 1+posActual[1]), vec(-1+posActual[0], 0+posActual[1])]
        for vecino in vecinos:
            for enemigo in enemigos:
                if vecino == enemigo.posMatriz:
                    enemigoMuelto.append(enemigo)
        return enemigoMuelto

    def darDireccion(self, objetivo):
        next_cell = self.posSiguiente(objetivo)
        xdir = next_cell[0] - self.posMatriz[0]
        ydir = next_cell[1] - self.posMatriz[1]
        return vec(xdir, ydir)

    def posSiguiente(self, objetivo):
        path = self.Asteris([int(self.posMatriz.x), int(self.posMatriz.y)], [
            int(objetivo[0]), int(objetivo[1])])
        if len(path) == 1:
            return path[0]
        else:
            return path[1]

    def Asteris(self, posJ, posO):
        nodoActual = Nodo(None, posJ[0], posJ[1])
        camino = []
        creadosNodo = set()
        expandidosNodo = set()
        expandidosNodo.add(nodoActual)
        creadosNodo.add(nodoActual)
        while creadosNodo:
            nodoActual = min(creadosNodo, key=lambda x: x.g + x.h)
            posActual = [nodoActual.x, nodoActual.y]
            if posActual == posO:
                while nodoActual.padre != None:
                    camino.insert(0, [int(nodoActual.x), int(nodoActual.y)])
                    nodoActual = nodoActual.padre
                camino.insert(0, [int(nodoActual.x), int(nodoActual.y)])
                return camino
            creadosNodo.remove(nodoActual)
            expandidosNodo.add(nodoActual)
            vecinos = [vec(0+posActual[0], -1+posActual[1]), vec(1+posActual[0], 0+posActual[1]),
                       vec(0+posActual[0], 1+posActual[1]), vec(-1+posActual[0], 0+posActual[1])]
            for vecino in vecinos:
                if vecino not in self.app.paredes:

                    h = math.sqrt((vecino[0]-posO[0])**2+(vecino[1]-posO[1])**2)
                    f = h + nodoActual.g + 1
                    hijo = Nodo(None, vecino.x, vecino.y)
                    hijo.f = f
                    hijo.h = h
                    hijo.g = nodoActual.g+1
                    hijo.padre = nodoActual
                    creadosNodo.add(hijo)

    def mover(self):
        self.direccion = self.darDireccion(self.objetivo)

    def get_posPixel(self):
        return vec((self.posMatriz[0] * self.app.cell_width) + self.app.cell_width,
                   (self.posMatriz[1] * self.app.cell_height) + self.app.cell_height)

    def puedeMover(self):
        if int(self.posPixel.x) % self.app.cell_width == 0:
            if self.direccion == vec(1, 0) or self.direccion == vec(-1, 0) or self.direccion == vec(0, 0):
                return True
        if int(self.posPixel.y) % self.app.cell_height == 0:
            if self.direccion == vec(0, 1) or self.direccion == vec(0, -1) or self.direccion == vec(0, 0):
                return True
        return False

    def hayPared(self):
        for pared in self.app.paredes:
            if vec(self.posMatriz+self.direccion) == pared:
                return False
        return True
