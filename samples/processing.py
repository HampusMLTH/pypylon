from multiprocessing import Process, Event
import time

def print_always(event_killed):
    print("always")
    for i in range(1,1000):
        if event_killed.is_set():
            return
        print(i)
        time.sleep(0.2)
        

def print_func(event_done, continent='Asia'):
    for i in range(0,9):
        print('The name of continent is : ', continent, "index", i)
        time.sleep(0.5)
    event_done.set()

if __name__ == "__main__":  # confirms that the code is under main function
    event_done = Event()
    event_killed = Event()
    
    proc_always = Process(target=print_always, args=(event_killed,))
    proc_always.start()
    print("debug")
    time.sleep(3)
    event_killed.set()
    
    names = ['America', 'Europe', 'Africa']
    procs = []
    proc = Process(target=print_func, args=(event_done,))  # instantiating without any argument
    procs.append(proc)
    proc.start()
    event_done.wait()
    event_done.clear()

    # instantiating process with arguments
    for name in names:
        # print(name)
        proc = Process(target=print_func, args=(event_done, name,))
        procs.append(proc)
        proc.start()
        time.sleep(2)
        event_done.wait()

    # complete the processes
    for proc in procs:
        proc.join()