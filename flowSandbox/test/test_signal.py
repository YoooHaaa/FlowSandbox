import signal
import threading

import time



def sigint_handler(signum, frame):
    print("sigint_handler()............")
    exit(0)


print(threading.enumerate())

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGHUP, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)
while True:
    time.sleep(1)

