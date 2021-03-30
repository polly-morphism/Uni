import threading
from time import sleep
from multiprocessing import Process, current_process, Lock, Event
import logging
import sys
import random

GLOBAL_COUNTER = 0
print_to_logs = logging.getLogger()
print_to_logs.setLevel(logging.DEBUG)

output_file_handler = logging.FileHandler("shared.log")

print_to_logs.addHandler(output_file_handler)


class MultiThread(threading.Thread):
    def __init__(self, id, counter):
        print("Initializing thread")
        threading.Thread.__init__(self)
        self.process_id = id
        self.condition = False
        self.state = threading.Condition()
        self.type = "parallel"
        self.status = "run"
        self.counter = counter

    def run(self):
        print(f"\nThread {self.process_id} is started\n\t\t")
        t = threading.currentThread()
        while getattr(t, "run", True):
            with t.state:
                if getattr(t, "condition", True):
                    print_to_logs.info(f"Thread {self.process_id} stopped")
                    t.state.wait()
            global GLOBAL_COUNTER
            print_to_logs.info(
                f"Thread {self.process_id} is currently executing\t Result  = {GLOBAL_COUNTER + self.counter}\t counter = {self.counter}"
            )
            GLOBAL_COUNTER += self.counter
            sleep(5)

        print_to_logs.info(f"Thread {self.process_id} is killed")


class MultiProcess(Process):
    def __init__(self, id, counter):
        print("Initializing process")
        Process.__init__(self)
        self.process_id = id
        self.condition = False
        self.state = threading.Condition()
        self.type = "async"
        self.status = "run"
        self.event = Event()
        self.counter = counter

    def run(self):
        print(f"\nProcess {self.process_id} is started\n ")
        t = current_process()
        while getattr(t, "run", True):
            if getattr(t, "condition", True):
                print_to_logs.info(f"Process {self.process_id} stopped")
            global GLOBAL_COUNTER
            print_to_logs.info(
                f"Process {self.process_id} is working\t Result of working = {GLOBAL_COUNTER + self.counter}\t counter = {self.counter}"
            )
            GLOBAL_COUNTER += self.counter
            sleep(5)

        print_to_logs.info(f"Process {self.process_id} killed")


menu = """
    new thread command - adding a new thread
    new process - adding a new process
    stop thread - stopping thread
    delete
    resume
    show - show all
    ----
    """
identities = {}
identities_n = 1
stopped_n = []
while True:
    sleep(1)
    command = str(input(menu))
    if command == "new thread":
        thread = MultiThread(identities_n, 1)
        thread.start()

        identities[identities_n] = thread
        identities_n += 1

    elif command == "new process":
        process = MultiProcess(identities_n, 1)
        process.start()

        identities[identities_n] = process

        identities_n += 1

    elif command == "delete":
        thread_numbers = list(identities.keys())
        m = int(input(f"Input the number of identity to stop {thread_numbers} "))
        if m in thread_numbers:
            print_to_logs.info(f"Deleting identity {m}...")
            if identities[m].type == "parallel":
                identities[m].run = False
                del identities[m]
            elif identities[m].type == "async":
                identities[m].terminate()
                del identities[m]
        else:
            print(f"Identity {m} doesn't exist")

    elif command == "stop thread":
        thread_numbers = list(identities.keys())
        m = int(input(f"Input number of thread you want to stop {thread_numbers} "))
        if m in thread_numbers:
            stopped_n.append(m)
            print_to_logs.info(f"Stopping thread {m}...")
            identities[m].status = "stop"
            if identities[m].type == "parallel":
                with identities[m].state:
                    identities[m].condition = True
            else:
                identities[m].terminate()
        else:
            print(f"Thread {m} doesn't exist")

    elif command == "resume":
        m = int(input(f"Input number of thread you want to resume {stopped_n} "))
        if m in stopped_n:
            identities[m].status = "run"

            if identities[m].type == "parallel":
                with identities[m].state:
                    identities[m].condition = False
                    identities[m].state.notify()
                    stopped_n.remove(m)
            else:
                identities[m].event.set()
        else:
            print(f"Thread {m} doesn't exist or it is running now")

    elif command == "show":
        for key in identities:
            print(key, "-", identities[key])

    else:
        print("No such command\n")
