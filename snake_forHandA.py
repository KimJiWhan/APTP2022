import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

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
GREEN = (0, 255, 0)
# Constants
oneBlockSize = 20
headSpeed = 10

class snakeGameHA:
    def __init__(self, w = 720, h = 720):
        # CONSTANTS (will not be reset)
        self.width = w
        self.height = h
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Asterisk->SnakeGameAI')
        self.clock = pygame.time.Clock()

        self.spd = headSpeed

        self.dir = Dir.RIGHT
        self.head = Cord((self.width) / 2, (self.height) / 2)
        self.snake = [self.head, Cord(self.head.x - oneBlockSize, self.head.y),
                      Cord(self.head.x - (2 * oneBlockSize), self.head.y)]
        self.item = Cord(random.randint(0, (self.width - oneBlockSize) // oneBlockSize) * oneBlockSize,
                         random.randint(0, (self.height - oneBlockSize) // oneBlockSize) * oneBlockSize)
        self.rec = 0
        self.tail = 0
        self.loop = False
        self.mode = 0 # 0 for human, 1 for AI

    def reset(self):
        self.dir = Dir.RIGHT
        self.head = Cord((self.width) / 2, (self.height) / 2)
        self.snake = [self.head, Cord(self.head.x - oneBlockSize, self.head.y),
                      Cord(self.head.x - (2 * oneBlockSize), self.head.y)]
        self.item = Cord(random.randint(0, (self.width - oneBlockSize) // oneBlockSize) * oneBlockSize,
                         random.randint(0, (self.height - oneBlockSize) // oneBlockSize) * oneBlockSize)
        self.tail = 0
        self.rec = 0
        self.loop = False

    def _locateItem(self):
        x = random.randint(0, (self.width - oneBlockSize) // oneBlockSize) * oneBlockSize
        y = random.randint(0, (self.height - oneBlockSize) // oneBlockSize) * oneBlockSize
        self.item = Cord(x, y)
        # if somehow the item is created in the snake. Recursive Method
        if self.item in self.snake:
            self._locateItem()

    def _moveHu(self, direction):
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

    def _moveAI(self, move):
        # Gets current coordinate and direction
        # Gives head a new Coordination
        clock_wise = [Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT]
        idx = clock_wise.index(self.dir)

        if np.array_equal(move, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(move, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d
        self.dir = new_dir

        x = self.head.x
        y = self.head.y
        if self.dir == Dir.UP:
            y -= oneBlockSize
        elif self.dir == Dir.RIGHT:
            x += oneBlockSize
        elif self.dir == Dir.DOWN:
            y += oneBlockSize
        elif self.dir == Dir.LEFT:
            x -= oneBlockSize



        self.head = Cord(x, y)

    def _collision(self):
        # Checks if the head collides with snake itself or the wall
        x = self.head.x
        y = self.head.y
        if self.rec == 500:
            self.loop = True
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return True
        elif self.head in self.snake[1:]:
            return True
        elif self.rec > 700:
            return True
        else:
            return False


    def collideCheck(self, cord):
        x = cord.x
        y = cord.y

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return True
        elif self.head in self.snake[1:]:
            return True
        elif self.rec + self.tail > 500:
            return True
        else:
            return False

    def _ui(self):
        self.display.fill(BLACK)
        pygame.draw.rect(self.display, GREEN, pygame.Rect(self.snake[0].x, self.snake[0].y, oneBlockSize, oneBlockSize))
        for idx, cord in enumerate(self.snake[1:len(self.snake) - 1]):
            x = [self.snake[idx].x - cord.x, self.snake[idx + 2].x - cord.x]
            y = [self.snake[idx].y - cord.y, self.snake[idx + 2].y - cord.y]
            pygame.draw.rect(self.display, GREY, pygame.Rect(cord.x, cord.y, oneBlockSize, oneBlockSize))
            self._draw(cord, x, y)
        pygame.draw.rect(self.display, GREY,
                         pygame.Rect(self.snake[-1].x, self.snake[-1].y, oneBlockSize, oneBlockSize))
        x = self.snake[-2].x - self.snake[-1].x
        y = self.snake[-2].y - self.snake[-1].y
        addition = [4, 4]
        if x == -20:
            addition[0] -= 4
        elif y == -20:
            addition[1] -= 4
        pygame.draw.rect(self.display, WHITE,
                         pygame.Rect(self.snake[-1].x + addition[0], self.snake[-1].y + addition[1], 12 + abs(x) / 5,
                                     12 + abs(y) / 5))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.item.x, self.item.y, oneBlockSize, oneBlockSize))

        text0 = font.render("Score: " + str(self.tail) + "/ Mode: " + str(self.mode), True, WHITE)
        self.display.blit(text0, [0, 0])
        pygame.display.flip()

    def _draw(self, cord, x, y):
        px = cord.x + 4
        py = cord.y + 4
        # dir = [top, right, bottom, left]
        length = [12, 12]  # x, y length
        length[0] = length[0] + (abs(x[0]) + abs(x[1])) / 5
        length[1] = length[1] + (abs(y[0]) + abs(y[1])) / 5
        if x[0] == -20 or x[1] == -20:
            px -= 4
        if y[0] == -20 or y[1] == -20:
            py -= 4
        pygame.draw.rect(self.display, WHITE, pygame.Rect(px, py, length[0], length[1]))

    def playHtoA(self, move, gen):
        if self.mode == 0:
            return self.playHu()
        else:
            return self.playAI(move, gen)
    def playHu(self):
        # Get Input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.dir = Dir.UP
                elif event.key == pygame.K_DOWN:
                    self.dir = Dir.DOWN
                elif event.key == pygame.K_LEFT:
                    self.dir = Dir.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.dir = Dir.RIGHT
                elif event.key == pygame.K_SPACE:
                    self.mode = 1
                    self.spd = 1000
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

        reward = 0

        # Move the snake by head
        self._moveHu(self.dir)
        self.snake.insert(0, self.head)

        # Check if the game ends
        game_over = False
        if self._collision():
            reward = -10
            game_over = True
            return reward, game_over, self.tail

        # place new food if met
        if self.head == self.item:
            self.tail += 1
            self._locateItem()
            reward = 10
        else:
            self.snake.pop()

        # update ui
        self._ui()
        self.clock.tick(headSpeed)

        return reward, game_over, self.tail

    def playAI(self, move, gen):
        # Set Input

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.spd = 10
                    self.mode = 0

        # Move the snake by head
        reward = 0
        self.rec += 1
        self._moveAI(move)
        self.snake.insert(0, self.head)

        # Check if the game ends
        if self._collision():
            reward = -10
            return reward, True, self.tail

        # Place new food if the head encounters the item
        if self.head == self.item:
            self.tail += 1
            reward = 10
            self._locateItem()
            self.rec = 0
        else:
            self.snake.pop()

        # update UI
        self._ui()
        self.clock.tick(self.spd)

        if gen == 150:
           self.spd = 50

        return reward, False, self.tail