#! /usr/local/bin/python3
"""
Código base de ejecución del programa:
Se contruyen los niveles, se importan imágenes y sonidos y ...
"""
import pygame
from pygame.locals import *
import time
import random

SIZE = 40
# BACKGROUND_COLOR = (110, 110, 5)


class Level:  # Esta clase se encarga de crear los niveles
    def __init__(self, parent_screen, layout, timer, speed):
        self.timer = timer
        self.speed = speed
        self.parent_screen = parent_screen
        archive = open('layouts/{}.txt'.format(layout), 'r')
        self.layout = []
        raw_ly = archive.readlines()
        archive.close
        for i in raw_ly:
            x = i[:49]
            self.layout.append(x.split(' '))
        self.position_wall = [((ix)*40, (iy)*40) for iy, fila in enumerate(self.layout) for ix, i in enumerate(fila) if i == '1']
        print(self.position_wall)
        print(len(self.position_wall))

    def draw(self):
        for wall in self.position_wall:
            x = Wall(self.parent_screen, wall[0], wall[1])
            x.draw()


class Wall():
    def __init__(self, parent_screen, x, y):
        self.image = pygame.image.load('resources/wall.jpeg').convert()
        self.parent_screen = parent_screen
        self.x = x
        self.y = y

    def draw(self):  # Dibuja la manzana
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()


class Apple:  # Clase que define a la manzana
    def __init__(self, parent_screen):
        self.image = pygame.image.load('resources/apple.jpeg').convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):  # Dibuja la manzana
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):  # Coloca la manzana en posición aleatoria
        self.x = random.randint(0, 24)*SIZE
        self.y = random.randint(0, 19)*SIZE


class Snake:  # Clase que define la serpiente
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/block.jpeg').convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'
        self.last_direction = 'down'

    def increase_length(self):  # Serpiente crece
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_up(self):  # Mover arriba
        if self.last_direction != 'down':
            self.direction = 'up'
            self.last_direction = 'up'
        else:
            pass

    def move_down(self):  # Mover abajo
        if self.last_direction != 'up':
            self.direction = 'down'
            self.last_direction = 'down'
        else:
            pass

    def move_right(self):  # Mover derecha
        if self.last_direction != 'left':
            self.direction = 'right'
            self.last_direction = 'right'
        else:
            pass

    def move_left(self):  # Mover izquierda
        if self.last_direction != 'right':
            self.direction = 'left'
            self.last_direction = 'left'
        else:
            pass

    def walk(self):  # Movimiento del cuerpo

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()  # Inicializa módulos de pygame
        self.surface = pygame.display.set_mode((1000, 800))  # Inicializa ventana
        pygame.display.set_caption("Codebasics Snake And Apple Game")
        pygame.mixer.init()
        self.play_background_music()
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.level = Level(self.surface, 'layout0', 300, 0.2)
        self.level.draw()
        self.wall = Wall(self.surface, 0, 0)
        self.wall.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):  # Colisión de un objeto
        if x1 == x2 and y1 == y2:
            return True
        return False

    # Renderizado y sonidos
    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load('resources/background1.jpeg')
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.level.draw()
        self.wall.draw()
        self.display_score()
        pygame.display.flip()

        # Serpiente come manzana:
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.snake.increase_length()
            self.apple.move()

        # Serpiente choca contra sí misma:
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise 'game over'
        # Serpiente choca con un muro

            #if self.is_collision(self.snake.x[0], self.snake.y[0], i[0], i[1]):
        for wall in self.level.position_wall:
            if self.is_collision(self.snake.x[0], self.snake.y[0], wall[0], wall[1]):
                self.play_sound('crash')
                raise 'game over'

    def show_game_over(self):  # Juego terminado
        self.render_background()  # Limpia la pantalla
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))  # Esto se agrega siempre que se quiera mostrar algo
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        pygame.mixer.music.pause()


    def display_score(self):
    # When ever you want to show something on a
    # surface you have to use the blit function
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.snake.length-2}', True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if event.key == K_ESCAPE:
                        exit(0)

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
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.5)


if __name__ == '__main__':
    game = Game()
    game.run()
