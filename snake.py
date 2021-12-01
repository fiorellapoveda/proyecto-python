#! /usr/bin/python3

# Puede ser necesario colocar el "/local/" entre usr y bin

"""
Proyecto de Python - Código base de ejecución del programa.
En este se encuentra toda la lógica del modo de juego.

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
import time
from pygame.locals import *
import random

SIZE = 40


class Level:
# Creates the diferent levels with help of the files in the "layouts" folder

    def __init__(self, parent_screen, layout):
    # Constructor
        self.parent_screen = parent_screen
        archive = open("layouts/{}.txt".format(layout), 'r')
        self.layout = []
        raw_ly = archive.readlines()
        archive.close
        for i in raw_ly:
            x = i[:49]
            self.layout.append(x.split(' '))
        self.position_wall = [
            ((ix)*40,
            (iy)*40) for iy,
            fila in enumerate(self.layout) for ix,
            i in enumerate(fila) if i == "1"]

    def draw(self):
    # Draws the walls of the level depending of the layout file
        for wall in self.position_wall:
            x = Wall(self.parent_screen, wall[0], wall[1])
            x.draw()


class Wall():
# Creates the wall with the respective file in the "resources" folder

    def __init__(self, parent_screen, x, y):
    # Constructor
        self.image = pygame.image.load("resources/wall.jpeg").convert()
        self.parent_screen = parent_screen
        self.x = x
        self.y = y

    def draw(self):
    # Draws the apple in the display
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()


class Food:
# Imports the image and defines the random position of the apple

    def __init__(self, parent_screen):
    # Constructor
        self.image = pygame.image.load("resources/apple.jpeg").convert()
        self.parent_screen = parent_screen
        self.x = random.randint(1, 23)*SIZE
        self.y = random.randint(2, 18)*SIZE

    def draw(self):
    # Draws the food
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
    # Puts the food in a random position
        self.x = random.randint(1, 23)*SIZE
        self.y = random.randint(2, 18)*SIZE


class Snake:
# Defines the increment in the snake's length, the controls and other aspects

    def __init__(self, parent_screen, length):
    # Constructor
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = "down"
        self.last_direction = "down"

    def increase_length(self):
    # Increases the length of the snake
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    # Methods to move the snake
    def move_up(self):
        if self.last_direction != "down":
            self.direction = "up"
            self.last_direction = "up"
        else:
            pass
    def move_down(self):
        if self.last_direction != "up":
            self.direction = "down"
            self.last_direction = "down"
        else:
            pass
    def move_right(self):
        if self.last_direction != "left":
            self.direction = "right"
            self.last_direction = "right"
        else:
            pass
    def move_left(self):
        if self.last_direction != "right":
            self.direction = "left"
            self.last_direction = "left"
        else:
            pass

    def walk(self):
    # Moves the body of the snake (the diferent blocks)
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        self.draw()

    def draw(self):
    # Draws the snake in the display
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


class Game:
# Has the logic of all the game and its objects and conditions

    def __init__(self):
    # Contructor
        self.layout = 0
        pygame.init()  # Inicializes pygame
        self.surface = pygame.display.set_mode((1000, 800)) # Inicializes window
        pygame.display.set_caption("Snake And Food Game")
        pygame.mixer.init()
        self.play_background_music()
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.level = Level(self.surface, "layout0")
        #self.level.draw()
        self.food = Food(self.surface)
        self.food.draw()

    def is_collision(self, x1, y1, x2, y2):
    # Defines the collision with an object
        if x1 == x2 and y1 == y2:
            return True
        return False

    # Methods for rendering and sounds

    def play_background_music(self):
        pygame.mixer.music.load("resources/music_game.mp3")
        pygame.mixer.music.play(-1) #The -1 helps to play the music in loop

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self, timer, lives):
        self.render_background()
        self.snake.walk()
        self.food.draw()
        if self.layout == 0:
            self.level = Level(self.surface, "layout0")
            self.level.draw()
        if self.layout == 1:
            self.level = Level(self.surface, "layout1")
            self.level.draw()
        if self.layout == 2:
            self.level = Level(self.surface, "layout2")
            self.level.draw()
        if self.layout == 3:
            self.level = Level(self.surface, "layout3")
            self.level.draw()
        if self.layout == 4:
            raise "game over"

        self.display_score()
        self.display_countdown(timer)
        self.display_lives(lives)
        pygame.display.flip()
        if timer == 0:
            self.layout +=1
            self.countdown = 100
            self.reset()
        if lives == 0:
            raise "game over"

        # When the snake eats the apple:
        if self.is_collision(self.snake.x[0],
                self.snake.y[0], self.food.x, self.food.y):
            self.play_sound("Bite")
            self.score += 1
            self.snake.increase_length()
            self.food.move()

        # When the snake collides with itself:
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0],
                    self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("boing")
                raise "game over"

        # When the snake collides with a wall:
        for wall in self.level.position_wall:
            if self.is_collision(self.snake.x[0],
                    self.snake.y[0], wall[0], wall[1]):
                self.play_sound("boing")
                self.lives -= 1
                self.reset()
        for wall in self.level.position_wall:
            if self.is_collision(self.food.x, self.food.y, wall[0], wall[1]):
                self.food.move()

    def show_game_over(self):
    # Defines the game over display
        self.render_background()  # Clears the background
        font1 = pygame.font.SysFont("arial", 40)
        font2 = pygame.font.SysFont("arial", 30)
        line1 = font1.render(f"GAME IS OVER!", True, (255, 255, 255))
        self.surface.blit(line1, (200, 200))
        line2 = font2.render(f"Your score is {self.score}.", True, (255, 255, 255))
        self.surface.blit(line2, (200, 300))
        line3 = font2.render(f"You can see the table of records in the Main "
        "Menu.", True, (255, 255, 255))
        self.surface.blit(line3, (200, 330))
        line3 = font2.render("PLEASE PRESS ENTER.", True, (255, 255, 255))
        self.surface.blit(line3, (200, 400))
        pygame.display.flip()

        pygame.mixer.music.pause()

        # Save highscores
        archive = open('resources/highscores.txt', 'r')
        raw_high = archive.readlines()
        archive.close
        print(raw_high)
        for raw_score in raw_high:
            highscores.append(int(raw_score))

        if self.score > highscores[4]:
            highscores.append(self.score)
            highscores.sort(reverse=True)
            highscores.pop(5)
            archive = open('resources/highscores.txt', 'w')
            for score in highscores:
                archive.write('{}\n'.format(score))
            archive.close()

    # Methods for variables in the game display

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.surface.blit(score, (800, 10)) # Used to show something in a surface

    def display_countdown(self, timer):
        font = pygame.font.SysFont("arial", 30)
        time = font.render(f"Time left: {timer}", True, (0, 0, 0))
        self.surface.blit(time, (10, 10))

    def display_lives(self, lives):
        font = pygame.font.SysFont("arial", 30)
        live = font.render(f"Lives left: {lives}", True, (0, 0, 0))
        self.surface.blit(live, (400, 10))

    def reset(self):
    # Resets the elements when a life is missed
        self.snake = Snake(self.surface, 2)
        self.food = Food(self.surface)

    def run(self):
    # Method for when the game starts
        self.score = 0
        self.lives = 3
        self.countdown = 100
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.countdown = 100
                        pause = False
                        pygame.display.quit()

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play(self.countdown, self.lives)
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.2)
            self.countdown -= 1

def runGame():
    game = Game()
    game.run()
