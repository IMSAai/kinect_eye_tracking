#!/usr/bin/env python
import pygame, sys
from pygame.locals import *
import time
import freenect
import cv2
import libfreenectWrapperDemos.frame_convert2 as frame_convert2
import os 


pygame.init()

width = 1920
height = 1016
x, y = 0, 0

DISPLAYSURF = pygame.display.set_mode((1920, 1016), pygame.RESIZABLE)

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
    global x
    global y
    # if freenect.get_video_format(dev) == 0:
    #     cv2.imshow('IR', frame_convert2.video_cv(data))
    # else:
    #     cv2.imshow('IR', data)
    name = str(x) + "x" + str(y) + ".png"
    save("/media/eh/ETHAN_HAQUE/ir_gaze_data", name, data)
    if cv2.waitKey(10) == 27:
        keep_running = False


def body(*args):
    global keep_running
    global x
    global y
    DISPLAYSURF.fill((255, 255, 255))
    DISPLAYSURF.set_at((x, y), (100, 10, 10))
    if x < width:
        x += 1
    else:
        x = 0
        y += 1
        time.sleep(1)
    if y >= height or x >= 20:
        keep_running = False
    pygame.display.update()
    if not keep_running:
        raise freenect.Kill
        pygame.quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

def save(path, name, img):
    cv2.imwrite(os.path.join(path, name), img)


print('Press ESC in window to stop')
freenect.runloop(
                # depth=display_depth,
                video=display_rgb,
                body=body,
                dev=dev)


    


