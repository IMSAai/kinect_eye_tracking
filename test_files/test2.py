#!/usr/bin/env python
import freenect
import cv2
import libfreenectWrapperDemos.frame_convert2 as frame_convert2

# ctx = freenect.init()
# dev = freenect.open_device(ctx, 0)

# freenect.set_depth_mode(dev, 1, 2)


def get_depth():
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])


while 1:
    cv2.imshow('Depth', get_depth())
    cv2.imshow('Video', get_video())
    if cv2.waitKey(10) == 27:
        break
