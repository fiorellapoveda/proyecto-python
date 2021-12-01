#! /usr/bin/python3

#Puede ser necesario colocar el "/local/" entre usr y bin

"""
Proyecto de Python - Código para imprimir las instrucciones del programa luego
de presionar el botón indicado en el menú principal.

Este código fue realizado en máquinas virtuales con instalaciones de Ubuntu
version 20.04 y un repositorio en github.
Para ejecutarlo es necesario tener instalada pygame (sudo pip3 install pygame).
El archivo que debe ejecutarse desde la terminal es el "main.py".

Estudiantes:
- Fiorella Poveda Chaves (B86145).
- Luis Ricardo Carmona Mora (B91646).
- Julián Zamora Villalobos (B07025).
"""

import pygame
from pygame.locals import *

class Instructions:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        pygame.display.set_caption("Instructions for the game")

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0, 0))

    def show_instructions(self):
        self.render_background()
        font = pygame.font.SysFont("arial", 25)
        line1 = font.render("1. The objetive is to collect as many apples as "
        "you can.", True, (255, 255, 255))
        self.surface.blit(line1, (50, 100))
        line2 = font.render("2. Everytime you collect an apple, the snake's "
        "length will increase.", True, (255, 255, 255))
        self.surface.blit(line2, (50, 150))
        line3 = font.render("3. Everytime the snake collides with a wall or "
        "itself, you'll lose a live.", True, (255, 255, 255))
        self.surface.blit(line3, (50, 200))
        line4 = font.render("4. With the keyboard arrows you can move up, "
        "down, left or right.", True, (255, 255, 255))
        self.surface.blit(line4, (50, 250))
        line5 = font.render("5. You'll begin with three lives. The game "
        "ends if you lose all the lives.", True, (255, 255, 255))
        self.surface.blit(line5, (50, 300))
        line6 = font.render("6. If the timer gets to 0 and you still have "
        "lives, you'll pass to the next level.", True, (255, 255, 255))
        self.surface.blit(line6, (50, 350))
        line7 = font.render("7. The game has four levels.", True, (255, 255, 255))
        self.surface.blit(line7, (50, 400))
        line8 = font.render("8. Once you end the game your score will be "
        "saved and ranked with other scores.", True, (255, 255, 255))
        self.surface.blit(line8, (50, 450))
        line9 = font.render("PRESS ENTER TO GET BACK TO MENU", True, (255, 255, 255))
        self.surface.blit(line9, (50, 515))
        pygame.display.flip()

def runInst():
    inst = Instructions()
    inst.show_instructions()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pygame.display.quit()
                    running = False
