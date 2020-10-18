import torch
import torch.nn as nn
import freenect
from threading import Thread

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

def formatData(data):
    return((torch.tensor([[data/255.0]])).to(dtype=torch.float))


def predict(im):
    data = formatData(im)
    output = model(data)
    return(output)

model = Net()
model.load_state_dict(torch.load(r"./CNN/models/all_data_full_pass.plt"))
model.eval()
model.share_memory()


ctx = freenect.init()
dev = freenect.open_device(ctx, 0)
freenect.set_video_mode(dev, 2, 2)

dims = (1920, 1080)
keep_running = True

def body(*args):
    if not keep_running:
        raise freenect.Kill

def update_screen(x, y):
    pass

def get_gaze(data):
    output = model(formatData(data))
    print ("x:{:.1f}\ny:{:.1f}\n{:.5f}".format(output[0][0].item()*dims[0], output[0][1].item()*dims[1], end-start))
    
def run(dev, data, timestamp):
    process = Thread(target=get_gaze, args=(data,))
    process.start()



freenect.runloop(dev=dev,
                 video=run,
                 body=body)
