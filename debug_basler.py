from basler_controller import BaslerController
import time
from queue import Queue
from queue import Empty
import threading


MAX_QSIZE = 30

def main():
    i=1
    
    #folder_path = "/media/pi/DAPHNIA/goniometer/" + time.strftime("%Y%m%d-%H%M%S/")
    folder_path = "sample_imgs/" + time.strftime("%Y%m%d-%H%M%S/")
    q = Queue(maxsize=MAX_QSIZE)
    bc = BaslerController(folder_path, q)
    #bc.close_camera()
    bc.open_camera()
    bc.update_nodemap()
    bc.cont_acq()
    
    #display(q)
    print("cont")
    consumer = Consumer(q)
    stop_threads = False
    consumer_thread = threading.Thread(target=consumer.run, args =(lambda : stop_threads, ))
    consumer_thread.start()
    
    time.sleep(4)
    bc.save_images("test_1")
    time.sleep(13)
    bc.stop_cont_acq()
    stop_threads = True
    print("stop thre")
    consumer_thread.join()
    print("con joined")
    q.join()
    print("q join")
    bc.close_camera()
    print("done")
    
class Consumer:
    def __init__(self, queue):
        self.queue = queue

    def run(self, stop):
        print("inside consumer")
        print("queue size {}".format(self.queue.qsize()))
       
        while not stop():
            print("queue size {}".format(self.queue.qsize()))
            try:
                item = self.queue.get(timeout=1)
            except Empty:
                print("timeout reached")
            else:
                self.queue.task_done()
                print("mean: {}".format(item.mean()))
            # here we either display or display&save images
            
        print("bottom")
    
if __name__ == '__main__':
    main()
    
