import threading
import time
import queue
import datetime


lock = threading.Lock()

def thread_task(q):
    while True:
        # Get the next available task
        task = q.get()
        # Process this task
        simulate(task)
        # Mark task as complete
        q.task_done()

def simulate(task, thread=True):
    # Some complicated simulation
    counter = 0
    for i in range(4000000):
        counter = counter ** 0.12342
        counter = counter ** 123.42342
    #time.sleep(1)
    # Store the value
    with lock:
        print("Task {} completed by {} ".format(task,threading.current_thread().name))


def create_threads(num, target, q):
    t = []
    for i in range(num):
        t.append(threading.Thread(target=target, name="Thread:{}".format(i), args=(q,), daemon=True))
        t[i].start()
    return t

def main_serial():
    # Start timer
    start = datetime.datetime.now()

    # Work on each thread
    for task in range(10):
        simulate(task, False)

    print('Finished job in {}'.format(datetime.datetime.now()-start))

def main_thread():
    # Create a queue of tasks
    q = queue.Queue()
    for task in range(10):
        q.put(task)

    # Start timer
    start_t = datetime.datetime.now()

    # Create threads
    threads = create_threads(2, thread_task, q)

    # Finishing
    q.join()
    print('Finished job in {}'.format(datetime.datetime.now()-start_t))

if __name__ == '__main__':
    main_thread()
    main_serial()
