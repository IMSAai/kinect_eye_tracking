import torch
import torch.nn as nn
import freenect
from threading import Thread
from network1 import Net
import tkinter as tk


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
    update_screen()

def update_screen():
    """Upates position of ball on Tkinter GUI"""
    x = min(max(0, current_x), dims[0])
    y = min(max(0, current_y), dims[1])

    x1 = x - ball_radius
    x2 = x + ball_radius
    y1 = y - ball_radius
    y2 = y + ball_radius

    canvas.coords(ball, x1, y1, x2, y2)
    canvas.update()
    


def get_gaze(data):
    """
    Prints out prediction data from kinect.

        Parameters:
                data (2d numpy array): A numpy array containing infrared intensity values.
    """
    output = predict(data)
    global current_x
    global current_y
    current_x = output[0][0].item()*dims[0]
    current_y = output[0][1].item()*dims[1]
    print ("x:{:.1f}\ny:{:.1f}".format(current_x, current_y))

    
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
    # get_gaze(data)


if __name__ == "__main__":
    ############### setup ###############
    model = Net()
    model.load_state_dict(torch.load(r"/home/eto/Desktop/kinect_eye_tracking/cnn/models/all_data_full_pass.plt"))
    model.eval()
    model.share_memory()


    ctx = freenect.init()
    dev = freenect.open_device(ctx, 0)
    #set to high res and to infrared mode
    freenect.set_video_mode(dev, 2, 2)

    dims = (1920, 1080)
    keep_running = True

    current_x = dims[0] / 2
    current_y = dims[1] / 2
    #####################################


    ############### simple gui overlay ###############
    root = tk.Tk()
    root.title("gaze position")
    root.wait_visibility(root)
    root.wm_attributes('-alpha', .1)
    canvas = tk.Canvas(root, width = 1920, height = 1080)
    canvas.pack()

    ball_radius = 20
    ball = canvas.create_oval(dims[0]/2 - ball_radius, dims[1]/2 - ball_radius, dims[0]/2 + ball_radius, dims[1]/2 + ball_radius, fill="red")
    root.update()
     #################################################

    freenect.runloop(dev=dev,
                    video=run,
                    body=body)