import numpy as np
import freenect
import libfreenectWrapperDemos.frame_convert2 as frame_convert2
import cv2

ctx = freenect.init()
dev = freenect.open_device(ctx, 0)
freenect.set_video_mode(dev, 1, 0)


# cv2.namedWindow('Depth')
# cv2.namedWindow('Video')
cv2.namedWindow("combined")
print('Press ESC in window to stop')


def get_depth():
    return freenect.sync_get_depth()[0]


def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])


while 1:
    # cv2.imshow('Depth', get_depth())
    # cv2.imshow('Video', get_video())
    cv2.imshow("combined", get_video() * (get_depth()[:, :, None] < 700))
    

    if cv2.waitKey(10) == 27:
        break
