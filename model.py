import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class LinearQNet(nn.Module):
    def __init__(self, inputSize, hiddenSize1, hiddenSize2, outputSize):
        super().__init__()
        self.linear1 = nn.Linear(inputSize, hiddenSize1)
        self.linear2 = nn.Linear(hiddenSize1, hiddenSize2)
        self.linear3 = nn.Linear(hiddenSize2, outputSize)
    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.linear3(x)
        return x
    def save(self, fileName='model.pth'):
        modelPath = './model'
        if not os.path.exists(modelPath):
            os.makedirs(modelPath)
        fileName = os.path.join(modelPath, fileName)
        torch.save(self.state_dict(), fileName)

class QTrain:
    def __init__(self, model, LR, gamma):
        self.LR = LR # Learning Rate
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.LR)
        self.criterion = nn.MSELoss()

    def trainMove(self, oldState, move, reward, nextState, done):
        oldState = torch.tensor(oldState, dtype = torch.float)
        nextState = torch.tensor(nextState, dtype = torch.float)
        move = torch.tensor(move, dtype = torch.long)
        reward = torch.tensor(reward, dtype = torch.float)

        if len(oldState.shape) == 1: # one dimension
            oldState = torch.unsqueeze(oldState, 0)
            nextState = torch.unsqueeze(nextState, 0)
            move = torch.unsqueeze(move, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

            # 1: predicted Q values with current state
        pred = self.model(oldState)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(nextState[idx]))

            target[idx][torch.argmax(move[idx]).item()] = Q_new

        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
