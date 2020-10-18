import numpy as np
import torch
import torch.nn as nn
import os
import copy
import time
from PIL import Image


# images have shape 1280x1024
dims = (1920, 1080)

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.layer2 = nn.Sequential(
            nn.Conv2d(1, 4, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(4),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(4, 4, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(4),
            nn.MaxPool2d(kernel_size=4, stride=4)
        )
        self.layer4 = nn.Sequential(
            nn.Conv2d(4, 4, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(4),
            nn.MaxPool2d(kernel_size=4, stride=4)
        )
        self.fc1 = nn.Linear(40 * 32 * 4, 200)
        self.fc2 = nn.Linear(200, 20)
        self.fc3 = nn.Linear(20, 2)

    def forward(self, x):
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        
        return(x)

def getPaths():
    ims = []
    count = 0
    for dir in os.listdir(r"C:/Users/Ethan_H_Laptop/base/programs/python/eye_tracker/data"):
        for im in os.listdir(r"C:/Users/Ethan_H_Laptop/base/programs/python/eye_tracker/data/" + dir):
            ims.append(r"C:/Users/Ethan_H_Laptop/base/programs/python/eye_tracker/data/" + dir + "/" + im)
    return(np.array(ims))

def loadImage(path):
    nameLoc = path[-13:-4].split("x")
    location = (int(nameLoc[0])/dims[0], int(nameLoc[1])/dims[1])
    image = Image.open(path)
    data = np.asarray(image)
    return(((torch.tensor([[data/255.0]])).to(dtype=torch.float), (torch.tensor([location])).to(dtype=torch.float)))

def evaluateModel(model, testPaths):
    model.eval()
    errx = 0
    erry = 0
    for i, path in enumerate(testPaths):
        im, label = loadImage(path)
        # print("eval", i, label)
        output = model(im)
        errx += abs(output[0][0].item() - label[0][0].item())
        erry += abs(output[0][1].item() - label[0][1].item())
    model.train()
    
    return((errx/len(testPaths)*dims[0], erry/len(testPaths)*dims[1]))

def trainModel():
    model = Net()
    # model.load_state_dict(torch.load(r"C:\Users\Ethan_H_Laptop\base\programs\python\eye_tracker\models\test_all.plt"))
    nums_epochs = 10

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)

    bestModel = model
    bestScore = (10000, 10000)
    testscores = []
    trainscores = []
    bigTest = []
    bigTrain = []
    
    paths = getPaths()
    np.random.shuffle(paths)
    trainingSet = paths[:18000]
    testSet = paths[18000:]
    # trainingSet = paths[:18]
    # testSet = paths[18:20]
    

    model.train()
    for epoch in range(nums_epochs):
        epochStart = time.time()
        print("start of epoch {}".format(epoch+1))
        np.random.shuffle(trainingSet)

        for i, path in enumerate(trainingSet):
            im, label = loadImage(path)
            # print("train", i, label)

            output = model(im)
            loss = criterion(output, label)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    #         if (i+1) % 9000 == 0:
    #             trainSc = evaluateModel(model, trainingSet)
    #             testSc = evaluateModel(model, testSet)
    #             if testSc < bestScore:
    #                 bestModel = copy.deepcopy(model)
    #                 bestScore = testSc
    #             testscores.append(testSc)
    #             trainscores.append(trainSc)

    #             print(trainSc)
    #             print(testSc)
    #             print("Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}"
    #                     .format(epoch+1, nums_epochs, i+1, len(trainingSet), loss.item()))
        
        testSc = evaluateModel(model, testSet)
        if sum(testSc) < sum(bestScore):
            bestModel = model
            bestScore = testSc
        print("Epoch [{}/{}], Loss: {:.4f}, Current Score [x:{:.3f} y:{:.3f}], Best Score [x:{:.3f} y:{:.3f}]"
                        .format(epoch+1, nums_epochs, loss.item(), testSc[0], testSc[1], bestScore[0], bestScore[1]))
        epochEnd = time.time()
        print("epoch took {} seconds".format(epochEnd-epochStart))
    # bigTest.append(testscores)
    # bigTrain.append(trainscores)
        
    finalscore = evaluateModel(model, testSet)
    print("-------------------------------------------------------")
    print("Final Score: [x:{:.3f} y:{:.3f}], Best Score: [x:{:.3f} y:{:.3f}]"
                        .format(finalscore[0], finalscore[1], bestScore[0], bestScore[1]))
    # print(bigTrain)
    # print(bigTest)

    # torch.save(bestModel.state_dict(), r"C:\Users\Ethan_H_Laptop\base\programs\python\eye_tracker\models\all_data_full_pass.plt")
        

start = time.time()
np.random.seed(1)
trainModel()
end = time.time()
print("total time {} seconds".format(end-start))


        

