#!/usr/bin/python
########################################################################################################################
# Joe's Python Experimente - Multithreading Test
#-----------------------------------------------------------------------------------------------------------------------
# \file       PythreadTest.py
# \creation   2015-03-04, Joe Merten
#-----------------------------------------------------------------------------------------------------------------------
# Ablauf, es werten:
# - ein (bzw. jetzt 4) Threads gestartet, der ohne sleep dauerhaft was tut (und zu gucken, ob es sowas wie Preemtion gibt)
#   - hat einer for-Schleife ebenso funktioniert wie auch mit perf_counter()
#   - offensichtlich wird nur 1 Cpu Kern verwendet
# - ein paar Signalhandler registriert (zum prüfen, ob simultan zum Rest, auf Signale reagiert wird)
# - 4 "WorkerThreads" instanziiert, die auf einer Queue lauschen und dort auf Arbeit warten
# - die Queue mit "Arbeit" gefüllt
# - auf Beendigung der Queue-Abarbeitung (durch die WorkerThreads) gewartet
########################################################################################################################

import threading
from queue import Queue
import time
import signal, os

# lock to serialize console output
lock = threading.Lock()

def doWork(item):
    time.sleep(item) # pretend to do some lengthy work.
    # Make sure the whole print completes or threads can mix up output in one line.
    with lock: print(threading.current_thread().name, item)

# The worker thread pulls an item from the queue and processes it
def workerThreadFunc():
    while True:
        item = q.get()
        doWork(item)
        q.task_done()

def startWorkerThreads():
    for i in range(4):
         t = threading.Thread(target=workerThreadFunc, name=i+1) #"bla"+str(i))
         t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
         t.start()

def fillQueue():
    for item in range(20): q.put(item)


def blockingThreadFunc():
    while True:
        start = time.perf_counter()
        while True:
            elapsed = time.perf_counter() - start
            if elapsed > 5: break
        #i=0
        #while True:
        #    i = i + 1
        #    if i > 10000000: break
        with lock: print(threading.current_thread().name, "Hellö 𝘑𝘰𝘦  😎")

def startBlockingThread():
    for i in range(4):
        bt = threading.Thread(target=blockingThreadFunc, name="Blocking " + str(i+1))
        bt.daemon = True
        bt.start()


def signalHandler(signum, frame):
    with lock: print('Signal handler called with signal', signum)
    signal.alarm(1)

def setSignalHandlers():
    signal.signal(signal.SIGALRM, signalHandler)
    signal.signal(signal.SIGUSR1, signalHandler)
    signal.signal(signal.SIGUSR2, signalHandler)


# Main
start = time.perf_counter()
setSignalHandlers()
startBlockingThread()
q = Queue()
startWorkerThreads()
fillQueue()
q.join()  # block until all tasks are done

print('time: ', time.perf_counter() - start)