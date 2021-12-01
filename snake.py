#! /usr/bin/python3

#Arriba falta el '/local/' entre usr y bin

#FALTA:
    #Linkear a glade
    #Mostrar la opción de reiniciar o salir (con glade)

"""
Código base de ejecución del programa:
Se contruyen los niveles, se importan imágenes y sonidos y ...
"""
import pygame
import time
from pygame.locals import *
import random

SIZE = 40


class Level:  # Creates the levels
    def __init__(self, parent_screen, layout):
        self.parent_screen = parent_screen
        archive = open('layouts/{}.txt'.format(layout), 'r')
        self.layout = []
        raw_ly = archive.readlines()
        archive.close
        for i in raw_ly:
            x = i[:49]
            self.layout.append(x.split(' '))
        self.position_wall = [((ix)*40, (iy)*40) for iy, fila in enumerate(self.layout) for ix, i in enumerate(fila) if i == '1']

    def draw(self):
        for wall in self.position_wall:
            x = Wall(self.parent_screen, wall[0], wall[1])
            x.draw()


class Wall():  # Creates the wall
    def __init__(self, parent_screen, x, y):
        self.image = pygame.image.load('resources/wall.jpeg').convert()
        self.parent_screen = parent_screen
        self.x = x
        self.y = y

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()


class Food:  # Defines the food
    def __init__(self, parent_screen):
        self.image = pygame.image.load('resources/apple.jpeg').convert()
        self.parent_screen = parent_screen
        self.x = random.randint(1, 23)*SIZE
        self.y = random.randint(2, 18)*SIZE

    def draw(self):  # Draws the food
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):  # Puts the food in a random position
        self.x = random.randint(1, 23)*SIZE
        self.y = random.randint(2, 18)*SIZE


class Snake:  # Defines the snake
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/block.jpg').convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'
        self.last_direction = 'down'

    def increase_length(self):  # Increases the length of the snake
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    # Methods to move the snake

    def move_up(self):
        if self.last_direction != 'down':
            self.direction = 'up'
            self.last_direction = 'up'
        else:
            pass

    def move_down(self):
        if self.last_direction != 'up':
            self.direction = 'down'
            self.last_direction = 'down'
        else:
            pass

    def move_right(self):
        if self.last_direction != 'left':
            self.direction = 'right'
            self.last_direction = 'right'
        else:
            pass

    def move_left(self):
        if self.last_direction != 'right':
            self.direction = 'left'
            self.last_direction = 'left'
        else:
            pass

    def walk(self):  # Moves the body of the snake
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
        self.layout = 0
        pygame.init()  # Inicializes pygame
        # Inicializes the window to play
        self.surface = pygame.display.set_mode((1000, 800))
        pygame.display.set_caption("Codebasics Snake And Food Game")
        pygame.mixer.init()
        self.play_background_music()
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.level = Level(self.surface, 'layout0')
        #self.level.draw()

        self.food = Food(self.surface)
        self.food.draw()

    def is_collision(self, x1, y1, x2, y2):  # Collision with an object
        if x1 == x2 and y1 == y2:
            return True
        return False

    # Rendering and sounds

    def play_background_music(self):
        pygame.mixer.music.load('resources/music_game.mp3')
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load('resources/background.jpg')
        self.surface.blit(bg, (0, 0))

    def play(self, timer, lives):
        self.render_background()
        self.snake.walk()
        self.food.draw()
        if self.layout == 0:
            self.level = Level(self.surface, 'layout0')
            self.level.draw()
        if self.layout == 1:
            self.level = Level(self.surface, 'layout1')
            self.level.draw()
        if self.layout == 2:
            self.level = Level(self.surface, 'layout2')
            self.level.draw()
        if self.layout == 3:
            self.level = Level(self.surface, 'layout3')
            self.level.draw()
        if self.layout == 4:
            raise 'game over'

        self.display_score()
        self.display_countdown(timer)
        self.display_lives(lives)
        pygame.display.flip()
        if timer == 0:
            self.layout += 1
            self.countdown = 100
            self.reset()
        if lives == 0:
            raise 'game over'
        # When the snake eats the apple:
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.play_sound('Bite')
            self.score += 1
            self.snake.increase_length()
            self.food.move()

        # When the snake collides with itself:
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('boing')
                raise 'game over'

        # Serpiente choca con un muro
        for wall in self.level.position_wall:
            if self.is_collision(self.snake.x[0], self.snake.y[0], wall[0], wall[1]):
                self.play_sound('boing')
                self.lives -= 1
                self.reset()

        for wall in self.level.position_wall:
            if self.is_collision(self.food.x, self.food.y, wall[0], wall[1]):
                self.food.move()


    def show_game_over(self):  # Game over
        self.render_background()  # Clears the background
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.score}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()
        # Save highscores
        highscores = []
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

    def display_score(self):
        # When ever you want to show something on a
        # surface you have to use the blit function
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def display_countdown(self, timer):
        # When ever you want to show something on a
        # surface you have to use the blit function
        font = pygame.font.SysFont('arial', 30)
        time = font.render(f'Time left: {timer}', True, (255, 255, 255))
        self.surface.blit(time, (10, 10))

    def display_lives(self, lives):
        # When ever you want to show something on a
        # surface you have to use the blit function
        font = pygame.font.SysFont('arial', 30)
        live = font.render(f'Lives left: {lives}', True, (255, 255, 255))
        self.surface.blit(live, (400, 10))



    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.food = Food(self.surface)

    def run(self):
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

#if __name__ == '__main__':
#    game = Game()
#    game.run()
