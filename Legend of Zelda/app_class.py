import pygame
import sys
import copy
import random
from settings import *
from player_class import *
from enemy_class import *


pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.llaveAtrapada = False
        self.estado = 'start'
        self.cell_width = WIDTH // COLS
        self.cell_height = HEIGHT // ROWS
        self.paredes = []
        self.llaves = []
        self.enemigos = []
        self.e_pos = []
        self.p_pos = None
        self.l_pos = None
        self.gridPosL = None
        self.generarMapa()  # COMENTAR ESTA FUNCION PARA NO GENERAR MAPA aleatorio
        self.cargarMapa()
        self.player = Player(self, vec(self.p_pos))
        self.crearEnemigos()

    def run(self):
        while self.running:
            if self.estado == 'start':
                self.iniciarEvento()
            elif self.estado == 'playing':
                self.actualizarJuego()
                self.dibujarTablero()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

############################ FUNCIONES DE DIBUJO ##################################

    def generarMapa(self):
        totalcasillas = COLS * ROWS
        pared = random.randrange(0, totalcasillas // 3)
        enemigos = 4  # random.randrange(0, totalcasillas//7)
        with open("mapa.txt", 'w') as file:  # Se abre el archivo
            for i in range(ROWS):
                for j in range(COLS):
                    file.write("S")  # S de suelo
                file.write("\n")
            file.close()
        a = open("mapa.txt").read().splitlines()

        a[0] = a[0].replace("S", "P", COLS)
        a[ROWS-1] = a[ROWS-1].replace("S", "P", COLS)
        for i in range(ROWS):
            a[i] = a[i].replace("S", "P", 1)
        for j in range(ROWS):
            limite = list(a[j])
            limite[COLS - 1] = 'P'
            a[j] = "".join(limite)
        for i in range(pared):
            corY = random.randrange(1, COLS-1)
            corX = random.randrange(1, ROWS-1)
            b = list(a[corX])
            for j in range(a[corX].__len__()):
                if j == corY:
                    b[j] = 'P'
            a[corX] = "".join(b)

        d = 2
        for i in range(enemigos):
            corY = random.randrange(1, COLS-1)
            corX = random.randrange(1, ROWS-1)
            b = a[corX]
            c = ""
            for j in range(a[corX].__len__()):
                if j == corY:
                    c = c + d.__str__()
                    d = d + 1
                else:
                    c = c + b[j]
            a[corX] = c
        llaveY = random.randrange(1, COLS-1)
        llaveX = random.randrange(1, ROWS-1)
        jugY = random.randrange(1, COLS-1)
        jugX = random.randrange(1, ROWS-1)
        b = a[llaveX]
        c = ""
        for j in range(a[llaveX].__len__()):
            if j == llaveY:
                c = c + "L"
            else:
                c = c + b[j]
        a[llaveX] = c
        p = a[jugX]
        c = ""
        for j in range(a[jugX].__len__()):
            if j == jugY:
                c = c + "J"
            else:
                c = c + p[j]
        a[jugX] = c
        open('mapa.txt', 'w').write('\n'.join(a))

    def cargarMapa(self):
        self.screen.fill(BLUE)
        self.background = pygame.image.load('piso.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        a = pygame.image.load('piso1.png')
        a = pygame.transform.scale(a, (self.cell_width, self.cell_height))
        with open("mapa.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "P":
                        self.paredes.append(vec(xidx, yidx))
                    elif char == "L":
                        self.llaves.append(vec(xidx, yidx))
                    elif char == "J":
                        self.p_pos = [xidx, yidx]
                        print("La INCIAL", self.p_pos)
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "S":
                        self.screen.blit(a, (int(xidx * self.cell_width),
                                             int(yidx * self.cell_height)))

    def crearEnemigos(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemigos.append(Enemy(self, vec(pos), idx))

    def iniciarEvento(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.music.load('keygen_music.mp3')
                pygame.mixer.music.play(-1)
                self.estado = 'playing'


########################### funciones del juego ##################################


    def actualizarJuego(self):
        self.player.actualizar()
        if self.player.posMatriz == self.llaves[0]:
            print("llave igual que jugador")
            a = pygame.mixer.Sound('door.wav')
            a.play()
            self.llaveAtrapada = True
            self.player.objetivo = vec(int(COLS//2), 0)
            self.llaves[0] = vec(int(COLS//2), 0)
            puertaAbierta = vec(int(COLS//2), 0)
            self.paredes.remove(puertaAbierta)

        a = self.player.matarEnemigo(self.enemigos)
        while a:
            b = a[0]
            coorE = b.posMatriz
            self.enemigos.remove(b)
            a.remove(b)
            self.draw_sangre(coorE)

            pygame.display.update()
        for enemigo in self.enemigos:
            enemigo.actualizar()

    def dibujarTablero(self):
        self.screen.fill(BLUE)
        self.draw_paredes()
        self.draw_llave()
        if self.llaveAtrapada:
            self.draw_puerta_abierta()
        else:
            self.draw_puerta()
        self.player.draw()
        for enemigo in self.enemigos:
            enemigo.draw()
        pygame.display.update()

    def draw_paredes(self):
        a = pygame.image.load('pared.png')
        a = pygame.transform.scale(a, (self.cell_width, self.cell_height))
        for pared in self.paredes:
            self.screen.blit(a, (int(pared.x * self.cell_width), int(pared.y * self.cell_height)))

    def draw_llave(self):
        a = pygame.image.load('llave.png')
        a = pygame.transform.scale(a, (self.cell_width, self.cell_height))
        x = self.llaves[0].x
        y = self.llaves[0].y
        self.screen.blit(a, (int(x * self.cell_width),
                             int(y * self.cell_height)))

    def draw_sangre(self, cadaver):
        a = pygame.mixer.Sound('muricion.wav')
        a.play()
        a = pygame.image.load('sangre.png')
        a = pygame.transform.scale(a, (self.cell_width, self.cell_height))
        x = cadaver.x
        y = cadaver.y
        self.screen.blit(a, (int(x * self.cell_width),
                             int(y * self.cell_height)))

    def draw_puerta(self):
        a = pygame.image.load('puerta.png')
        a = pygame.transform.scale(a, (self.cell_width, self.cell_height))
        x = COLS//2
        y = 0
        self.screen.blit(a, (int(x * self.cell_width),
                             int(y * self.cell_height)))

    def draw_puerta_abierta(self):
        a = pygame.image.load('puerta_abierta.png')
        a = pygame.transform.scale(a, (self.cell_width, self.cell_height))
        x = COLS//2
        y = 0
        self.screen.blit(a, (int(x * self.cell_width),
                             int(y * self.cell_height)))
