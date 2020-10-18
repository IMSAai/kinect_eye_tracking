#!/usr/bin/env python
import freenect 
import cv2
import os
import pygame 
import random

ctx = freenect.init()
dev = freenect.open_device(ctx, 0)
freenect.set_video_mode(dev, 2, 2)

keep_running = True

pygame.init()

width = 1920
height = 1016
x, y = width//2, height//2
cx, cy = 200, 200
total = 0

DISPLAYSURF = pygame.display.set_mode((1920, 1016), pygame.RESIZABLE)

def process_ir(dev, data, timestamp):
    global keep_running
    global x 
    global y
    global total
    DISPLAYSURF.fill((100, 255, 255)) 
    pygame.draw.circle(DISPLAYSURF, (100, 10, 10), (x, y), 3)
    # DISPLAYSURF.set_at((x, y), (100, 10, 10))
    pygame.display.update()
    wait()
    name = '{:0>4}x{:0>4}.jpg'.format(x, y)
    save_image("", name, data)
    total += 1
    print(total)
    # if x + cx < width:
    #     x += cx
    # else:
    #     x = 0
    #     y += cy
    # if y >= height:
    #     keep_running = False
    x = random.randint(max(10, x-cx), min(x+cx, 1910))
    y = random.randint(max(10, y-cy), min(y+cy, 1010))
    if cv2.waitKey(10) == 27:
        keep_running = False

def body(*args):
    if not keep_running:
        raise freenect.Kill

def save_image(path, name, data):
    cv2.imwrite(os.path.join(path, name), data)

def wait():
    global keep_running
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                keep_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

freenect.runloop(
                video=process_ir,
                body=body,
                dev=dev)