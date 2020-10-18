import torch
import torch.nn as nn
import freenect
from threading import Thread
from network1 import Net


def formatData(data):
    """
    Returns tensor of image.

        Parameters:
            data (2d numpy array): A numpy array containing infrared intensity values.
        
        Returns:
            tens (pytorch tensor): Normalized 2d tensor of infrared image.
    """
    tens = torch.tensor([[data/255.0]]).to(dtype=torch.float)
    return(tens)


def predict(im):
    """
    Finds the gaze position of a user looking at an image.

        Parameters:
            im (2d numpy array): A numpy array containing infrared intensity values.

        Returns:
            output (pytorch tensor): A tensor with two values for x and y gaze position.
    """
    data = formatData(im)
    output = model(data)
    return(output)


def body(*args):
    """Body callback function for interfacing with kinect data stream."""
    if not keep_running:
        raise freenect.Kill

def update_screen(x, y):
    pass

def get_gaze(data):
    """
    Prints out prediction data from kinect.

        Parameters:
                data (2d numpy array): A numpy array containing infrared intensity values.
    """
    output = predict(data)
    print ("x:{:.1f}\ny:{:.1f}".format(output[0][0].item()*dims[0], output[0][1].item()*dims[1]))
    
def run(dev, data, timestamp):
    """
    Callback for processing kinect data stream.

        Parameters:
            dev (kinect device): Instance of Kinect being used.
            data (2d numpy array): A numpy array containing infrared intensity values.
            timestamp (int): Time of call.
    """
    process = Thread(target=get_gaze, args=(data,))
    process.start()




############### setup ###############
model = Net()
model.load_state_dict(torch.load("./CNN/models/all_data_full_pass.plt"))
model.eval()
model.share_memory()


ctx = freenect.init()
dev = freenect.open_device(ctx, 0)
#set to high res and to infrared mode
freenect.set_video_mode(dev, 2, 2)

dims = (1920, 1080)
keep_running = True
#####################################

#callback
freenect.runloop(dev=dev,
                 video=run,
                 body=body)
