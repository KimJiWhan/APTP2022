from snake_ForAI import snakeGameAI, Dir, Cord
from model import Train
import pygame

class snake_AI:
    def __init__(self):
        self.dir = Dir.RIGHT
        self.state = []
    def _setState(self, game):
        # Delta x(item), Delta y(item), Delta x(Left Wall), Delta y(Top Wall)
        x = game.head.x
        y = game.head.y
        ix = game.item.x
        iy = game.item.y
        self.state = [
            ix - x, iy - y, x, y
        ]
    def _setDir(self, state):
        self.dir = Dir.RIGHT
    def returnDir(self, game):
        # calculate direction by preference
        self.dir = self._setDir(self.state)
        return self.dir
    def returnState(self, game):
        self._setState(game)
        return self.state



def learn():
    pygame.init()
    gen = 0 # shows the generation
    game = snakeGameAI()
    AI = snake_AI()
    best = 0
    while True:
        stateOld = AI.returnState(game)
        dir = AI.returnDir(game)
        gameOver, score = game.play(dir, gen)
        stateNew = AI.returnState(game)


        if gameOver == True:
            game.reset()
            gen += 1

            if best < score:
                best = score

            print("Generation: ", gen, "/ Score: ", score, "/ BestScore: ", best)

if __name__ == "__main__":
    game = learn()