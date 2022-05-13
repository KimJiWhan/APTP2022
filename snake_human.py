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
GREEN=(0,255,0)

# Constants
oneBlockSize = 20
headSpeed = 5

class snakeGame:
    def __init__(self, w=720, h=720):
        self.width = w
        self.height = h
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Asterisk->SnakeGame')
        self.clock = pygame.time.Clock()
        # initialize the snake (head at center, two blocks at tail)
        self.dir = Dir.RIGHT

        self.head = Cord((self.width)/2, (self.height)/2)
        self.snake = [self.head, Cord(self.head.x - oneBlockSize, self.head.y), Cord(self.head.x - (2 * oneBlockSize), self.head.y)]
        self.item = Cord(random.randint(0, (self.width - oneBlockSize) // oneBlockSize) * oneBlockSize, random.randint(0, (self.height - oneBlockSize) // oneBlockSize) * oneBlockSize)
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

    def _ui(self):
        self.display.fill(BLACK)

        pygame.draw.rect(self.display, GREEN, pygame.Rect(self.snake[0].x, self.snake[0].y, oneBlockSize, oneBlockSize))
        for idx,cord in enumerate(self.snake[1:]):
            aX=(self.snake[idx].x)-(self.snake[idx+1].x)
            aY=(self.snake[idx].y)-(self.snake[idx+1].y)
            bX = (self.snake[idx-1].x) - (self.snake[idx].x)
            bY = (self.snake[idx-1].y) - (self.snake[idx].y)
            pygame.draw.rect(self.display, GREY, pygame.Rect(cord.x, cord.y, oneBlockSize, oneBlockSize))
            pygame.draw.rect(self.display, WHITE, pygame.Rect(cord.x + 4, cord.y + 4, 12, 12))
            if aX>0 :
                if self.snake[idx]==self.snake[-1]:
                    pygame.draw.rect(self.display, WHITE, pygame.Rect(cord.x, cord.y + 4, 16, 12))
                else:
                    pygame.draw.rect(self.display, WHITE, pygame.Rect(cord.x, cord.y + 4, 20, 12))
            elif aX<0 :
                if self.snake[idx].x==self.snake[-1].x:
                    pygame.draw.rect(self.display, WHITE, pygame.Rect(cord.x+4, cord.y + 4, 16, 12))
                else:
                    pygame.draw.rect(self.display, WHITE, pygame.Rect(cord.x, cord.y + 4, 20, 12))
            if aY>0 :
                if self.snake[idx]==self.snake[-1]:
                    pygame.draw.rect(self.display, WHITE, pygame.Rect(cord.x+4, cord.y , 12, 16))
                else:
                    pygame.draw.rect(self.display, WHITE, pygame.Rect(cord.x+4, cord.y , 12, 20))
            elif aY<0 :
                if self.snake[idx].y==self.snake[-1].y:
                    pygame.draw.rect(self.display, WHITE, pygame.Rect(cord.x+4, cord.y+4 , 12, 16))
                else:
                    pygame.draw.rect(self.display, WHITE, pygame.Rect(cord.x+4, cord.y , 12, 20))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.item.x, self.item.y, oneBlockSize, oneBlockSize))

        text = font.render("Score: " + str(self.tail), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def play(self):
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
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move the snake by head
        self._move(self.dir)
        self.snake.insert(0, self.head)

        # Check if the game ends
        game_over = False
        if self._collision():
            game_over = True
            return game_over, self.tail

        # place new food if met
        if self.head == self.item:
            self.tail += 1
            self._locateItem()
        else:
            self.snake.pop()

        # update ui
        self._ui()
        self.clock.tick(headSpeed)

        return game_over, self.tail

if __name__ == "__main__":
    game = snakeGame()
    while True:
        game_over, score = game.play()
        if game_over == True:
            break
    print("Final Score: ", score)
    pygame.quit()