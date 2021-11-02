import logging
import threading
import time


def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

def write2console(buffer):
    """ asdasd """
    while RUN_FLAG:
        if len(buffer) != 0:
            data = buffer.pop(0)
            print(data)
        time.sleep(0.5)

if __name__ == "__main__":
    RUN_FLAG = True
    BUFFER = list()
    format = "[%(asctime)s] %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")

    x = threading.Thread(target=write2console, args=(BUFFER,))
    BUFFER.append("hello")
    x.start()
    time.sleep(1)
    BUFFER.append("world")
    time.sleep(1)
    RUN_FLAG = False
    x.join()
    logging.info("Main    : all done")