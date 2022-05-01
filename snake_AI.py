import random
import numpy as np
import torch
from collections import deque
from snake_ForAI import snakeGameAI, Dir, Cord, oneBlockSize
from model import LinearQNet, QTrain
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

SetDir = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
class snake_AI:
    def __init__(self):
        self.gen = 0
        self.epsilon = 0 # Control randomness
        self.gamma = 0.9 # Discount rate , < 1
        self.memory = deque(maxlen = MAX_MEMORY)
        self.model = LinearQNet(14, 256, 256, 3)
        self.trainer = QTrain(self.model, LR = LR, gamma = self.gamma)

    def _setState(self, game):
        # front, right, left, back

        ptUp = Cord(game.head.x, game.head.y - oneBlockSize)
        ptRight = Cord(game.head.x + oneBlockSize, game.head.y)
        ptDown = Cord(game.head.x, game.head.y + oneBlockSize)
        ptLeft = Cord(game.head.x - oneBlockSize, game.head.y)

        dirUp = (game.dir == Dir.UP)
        dirRight = (game.dir == Dir.RIGHT)
        dirDown = (game.dir == Dir.DOWN)
        dirLeft = (game.dir == Dir.LEFT)


        self.state = [
            # Front Check
            (dirUp and game.collideCheck(ptUp)) or
            (dirRight and game.collideCheck(ptRight)) or
            (dirDown and game.collideCheck(ptDown)) or
            (dirLeft and game.collideCheck(ptLeft)),
            # Right side Check
            (dirUp and game.collideCheck(ptRight)) or
            (dirRight and game.collideCheck(ptDown)) or
            (dirDown and game.collideCheck(ptLeft)) or
            (dirLeft and game.collideCheck(ptUp)),
            # Bottom side Check is not needed (Always 0)
            # Left side Check
            (dirUp and game.collideCheck(ptLeft)) or
            (dirRight and game.collideCheck(ptUp)) or
            (dirDown and game.collideCheck(ptRight)) or
            (dirLeft and game.collideCheck(ptDown)),

            # Front Check
            (dirUp and game.collideCheck2(game.head)[0]) or
            (dirRight and game.collideCheck2(game.head)[0]) or
            (dirDown and game.collideCheck2(game.head)[0]) or
            (dirLeft and game.collideCheck2(game.head)[0]),
            # Right side Check
            (dirUp and game.collideCheck2(game.head)[1]) or
            (dirRight and game.collideCheck2(game.head)[1]) or
            (dirDown and game.collideCheck2(game.head)[1]) or
            (dirLeft and game.collideCheck2(game.head)[1]),
            # Bottom side Check is not needed (Always 0)
            # Left side Check
            (dirUp and game.collideCheck2(game.head)[2]) or
            (dirRight and game.collideCheck2(game.head)[2]) or
            (dirDown and game.collideCheck2(game.head)[2]) or
            (dirLeft and game.collideCheck2(game.head)[2]),

            # Direction of Head
            dirUp, dirRight, dirDown, dirLeft,

            # Food Direction
            # Food at Front
            (dirUp and game.item.y < game.head.y) or
            (dirRight and game.item.x > game.head.x) or
            (dirDown and game.item.y > game.head.y) or
            (dirLeft and game.item.x < game.head.x),

            # Food at Right side
            (dirUp and game.item.x > game.head.x) or
            (dirRight and game.item.y > game.head.y) or
            (dirDown and game.item.x < game.head.x) or
            (dirLeft and game.item.y < game.head.y),

            # Food Back
            (dirUp and game.item.y > game.head.y) or
            (dirRight and game.item.x < game.head.x) or
            (dirDown and game.item.y < game.head.y) or
            (dirLeft and game.item.x > game.head.x),

            # Food at Left side
            (dirUp and game.item.x < game.head.x) or
            (dirRight and game.item.y < game.head.y) or
            (dirDown and game.item.x > game.head.x) or
            (dirLeft and game.item.y > game.head.y)
        ]
    def _setMove(self, state):
        self.epsilon = 80 - self.gen
        move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move[random.randint(0, 2)] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move[torch.argmax(prediction).item()] = 1
        return move

    def remember(self, oldState, move, reward, nextState, done):
        # stores a tuple in memory
        self.memory.append((oldState, move, reward, nextState, done)) # pop memory if exceed the max memory

    def trainLongMemory(self):
        if len(self.memory) > BATCH_SIZE:
            miniSample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            miniSample = self.memory

        # for state, action, reward, nextStates, done in miniSample:
        #   self trainer.trainMove(state, action, reward, nextState, done)
        # equivalent to below arguments
        oldStates, moves, rewards, nextStates, dones = zip(*miniSample)
        self.trainer.trainMove(oldStates, moves, rewards, nextStates, dones)

    def trainShortMemory(self, oldState, move, reward, nextState, done):
        # Train for only one move
        self.trainer.trainMove(oldState, move, reward, nextState, done)

    def returnState(self, game):
        self._setState(game)
        return np.array(self.state, dtype=int)

    def returnMove(self, state):
        # calculate direction by preference
        # returns array
        # straight, left, right
        self.move = self._setMove(state)
        return self.move

def learn():
    scores = []
    i = 1
    meanScores = []
    totalScore = 0
    best = 0
    game = snakeGameAI()
    AI = snake_AI()
    while True:
        stateOld = AI.returnState(game)
        move = AI.returnMove(stateOld)
        reward, gameOver, score = game.play(move, AI.gen)
        stateNew = AI.returnState(game)

        # train short memory for one move
        AI.trainShortMemory(stateOld, move, reward, stateNew, gameOver)

        # remember
        AI.remember(stateOld, move, reward, stateNew, gameOver)

        if gameOver:
            # train long memory for one game, plot result
            AI.gen += 1
            AI.trainLongMemory()
            if best < game.tail:
                best = game.tail
                AI.model.save()
            print("Generation: ", AI.gen, "/ Score: ", game.tail, "/ BestScore: ", best)
            scores.append(game.tail)
            game.reset()
if __name__ == "__main__":
    game = learn()