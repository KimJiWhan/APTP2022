import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

# Fonts
font = pygame.font.Font('arial.ttf', 20)

# Moving Direction
class Dir(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


# Coordination of point
Cord = namedtuple('Cord', ['x', 'y'])

# RGBs
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Constants
oneBlockSize = 20
headSpeed = 20

class snakeGameAI:
    def __init__(self, w = 720, h = 720):
        # CONSTANTS (will not be reset)
        self.width = w
        self.height = h
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Asterisk->SnakeGameAI')
        self.clock = pygame.time.Clock()

        self.dir = Dir.RIGHT
        self.head = Cord((self.width) / 2, (self.height) / 2)
        self.snake = [self.head, Cord(self.head.x - oneBlockSize, self.head.y),
                      Cord(self.head.x - (2 * oneBlockSize), self.head.y)]
        self.item = Cord(random.randint(0, (self.width - oneBlockSize) // oneBlockSize) * oneBlockSize,
                         random.randint(0, (self.height - oneBlockSize) // oneBlockSize) * oneBlockSize)
        self.tail = 0

    def reset(self):
        self.dir = Dir.RIGHT
        self.head = Cord((self.width) / 2, (self.height) / 2)
        self.snake = [self.head, Cord(self.head.x - oneBlockSize, self.head.y),
                      Cord(self.head.x - (2 * oneBlockSize), self.head.y)]
        self.item = Cord(random.randint(0, (self.width - oneBlockSize) // oneBlockSize) * oneBlockSize,
                         random.randint(0, (self.height - oneBlockSize) // oneBlockSize) * oneBlockSize)
        self.tail = 0

    def _locateItem(self):
        x = random.randint(0, (self.width - oneBlockSize) // oneBlockSize) * oneBlockSize
        y = random.randint(0, (self.height - oneBlockSize) // oneBlockSize) * oneBlockSize
        self.item = Cord(x, y)
        # if somehow the item is created in the snake. Recursive Method
        if self.item in self.snake:
            self._locateItem()

    def _move(self, direction):
        # Gets current coordinate and direction
        # Gives head a new Coordination
        x = self.head.x
        y = self.head.y
        if direction == Dir.UP:
            y -= oneBlockSize
        elif direction == Dir.RIGHT:
            x += oneBlockSize
        elif direction == Dir.DOWN:
            y += oneBlockSize
        elif direction == Dir.LEFT:
            x -= oneBlockSize
        self.head = Cord(x, y)

    def _collision(self):
        # Checks if the head collides with snake itself or the wall
        x = self.head.x
        y = self.head.y
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return True
        elif self.head in self.snake[1:]:
            return True
        else:
            return False

    def _ui(self, gen):
        self.display.fill(BLACK)

        for cord in self.snake:
            pygame.draw.rect(self.display, WHITE, pygame.Rect(cord.x, cord.y, oneBlockSize, oneBlockSize))
            pygame.draw.rect(self.display, GREY, pygame.Rect(cord.x+4, cord.y+4, 12, 12))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.item.x, self.item.y, oneBlockSize, oneBlockSize))

        text0 = font.render("Score: " + str(self.tail) + "/ Generation: " + str(gen), True, WHITE)
        self.display.blit(text0, [0, 0])
        pygame.display.flip()

    def play(self, dir, gen):
        # Set Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            else:
                self.dir = dir

        # Move the snake by head
        self._move(self.dir)
        self.snake.insert(0, self.head)

        # Check if the game ends
        game_over = False
        if self._collision():
            game_over = True
            return game_over, self.tail

        # Place new food if the head encounters the item
        if self.head == self.item:
            self.tail += 1
            self._locateItem()
        else:
            self.snake.pop()

        # update UI
        self._ui(gen)
        self.clock.tick(headSpeed)

        return game_over, self.tail