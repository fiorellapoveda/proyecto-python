#! /usr/bin/python3

#Puede ser necesario colocar el "/local/" entre usr y bin

"""
Proyecto de Python - Código para imprimir los cinco records más altos
obtenidos en el juego luegode presionar el botón indicado en el menú principal.

Este código fue realizado en máquinas virtuales con instalaciones de Ubuntu
version 20.04 y un repositorio en github.
Para ejecutarlo es necesario tener instalada pygame (sudo pip3 install pygame).
El archivo que debe ejecutarse desde la terminal es el "main.py".

Estudiantes:
- Fiorella Poveda Chaves (B86145).
- Luis Ricardo Carmona Mora (B91646).
- Julián Zamora Villalobos (B07025).
"""

#archivo = ("resources/highscores.txt")
#print(archivo.read())

#def __init__(self, parent_screen, layout):
# Constructor
#    self.parent_screen = parent_screen
#    archive = open("layouts/{}.txt".format(layout), 'r')
#    self.layout = []
#    raw_ly = archive.readlines()
#    archive.close
#    for i in raw_ly:
#        x = i[:49]
#        self.layout.append(x.split(' '))
#    self.position_wall = [
#        ((ix)*40,
#        (iy)*40) for iy,
#        fila in enumerate(self.layout) for ix,
#        i in enumerate(fila) if i == "1"]

import pygame
from pygame.locals import *

class Records:
    def __init__(self):#, parent_screen):
        pygame.init()
        self.surface = pygame.display.set_mode((500,400))
        pygame.display.set_caption("Table of Records")

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0,0))

    def show_records(self):
        self.render_background()
        archive = open("resources/highscores.txt", "r")
        font = pygame.font.SysFont("arial",25)
        raw_records = archive.readlines()
        for item in raw_records:
            line = font.render(f"{item}", True, (255,255,255))
            self.surface.blit(line, (100, 100))
            print(line)
        self.display_records()
        pygame.display.flip()

    def display_records(self):
        font = pygame.font.SysFont("arial", 30)
        record = font.render(f"Score: {self.item}", True, (0, 0, 0))
        self.surface.blit(record, (800, 10)) # Used to show something in a surface

def runRecords():
    records = Records()
    records.show_records()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pygame.display.quit()
                    running = False

    #def show_records(self):
        #self.render_background()
        #archivo = ("resources/highscores.txt")
        #print(archivo.read())
        #font = pygame.font.SysFont("arial",25)
        #line1 = font.render("1. The objetive is to collect as many apples as "
        #"you can.",True,(255,255,255))
        #self.surface.blit(line1,(50,100))
        #line2 = font.render("2. Everytime you collect an apple, the snake's "
        #"length will increase.",True,(255,255,255))
        #self.surface.blit(line2,(50,150))
        #line3 = font.render("3. Everytime the snake collides with a wall or "
        #"itself, you'll lose a live.",True,(255,255,255))
        #self.surface.blit(line3,(50,200))
        #line4 = font.render("4. With the keyboard arrows you can move up, "
        #"down, left or right.",True,(255,255,255))
        #self.surface.blit(line4,(50,250))
        #line5 = font.render("5. You'll begin with three lives. The game "
        #"ends if you lose all the lives.",True,(255,255,255))
        #self.surface.blit(line5,(50,300))
        #line6 = font.render("6. If the timer gets to 0 and you still have "
        #"lives, you'll pass to the next level.",True,(255,255,255))
        #self.surface.blit(line6,(50,350))
        #line7 = font.render("7. The game has four levels.",True,(255,255,255))
        #self.surface.blit(line7,(50,400))
        #line8 = font.render("8. Once you end the game your score will be "
        #"saved and ranked with other scores.",True,(255,255,255))
        #self.surface.blit(line8,(50,450))
        #line9 = font.render("PRESS ENTER TO GET BACK TO MENU", True,(255,255,255))
        #self.surface.blit(line9,(50,515))
        #pygame.display.flip()

#def runRecords():
    #rcrds = Records()
    #rcrds.show_records()
    #running = True
    #while running:
        #for event in pygame.event.get():
            #if event.type == KEYDOWN:
                #if event.key == K_RETURN:
                    #pygame.display.quit()
                    #running = False
