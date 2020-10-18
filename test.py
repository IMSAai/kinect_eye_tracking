#!/usr/bin/env python
import freenect
import cv2
import libfreenectWrapperDemos.frame_convert2 as frame_convert2
import os 

# cv2.namedWindow('Depth')
cv2.namedWindow('IR')
keep_running = True

ctx = freenect.init()
dev = freenect.open_device(ctx, 0)
freenect.set_video_mode(dev, 2, 2)


def display_depth(dev, data, timestamp):
    global keep_running
    cv2.imshow('Depth', frame_convert2.pretty_depth_cv(data))
    if cv2.waitKey(10) == 27:
        keep_running = False


def display_rgb(dev, data, timestamp):
    global keep_running
    if freenect.get_video_format(dev) == 0:
        cv2.imshow('IR', frame_convert2.video_cv(data))
    else:
        cv2.imshow('IR', data)
    if cv2.waitKey(10) == 27:
        save("", "testIR.png", data)
        keep_running = False


def body(*args):
    freenect.set_tilt_degs(args[0], 30)
    if not keep_running:
        raise freenect.Kill

def save(path, name, img):
    cv2.imwrite(os.path.join(path, name), img)


print('Press ESC in window to stop')
freenect.runloop(
                # depth=display_depth,
                video=display_rgb,
                body=body,
                dev=dev)
