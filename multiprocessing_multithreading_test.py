from threading import Thread
from Queue import Queue
import time


def sleeping(seconds):
    time.sleep(seconds)
    return "slept for {}".format(seconds)


q = Queue()

count = 0
while True:
    if(count % 100000) == 0:
        print("count {}".format(count))
        p = multiprocessing.Process(target=sleeping, args=(2,))
        p.start()
        p.join()
    count += 1

