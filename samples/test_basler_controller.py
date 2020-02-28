from basler_controller import BaslerController
import time

def main():
    
    bc = BaslerController()
    #bc.close_camera()
    bc.open_camera()
    bc.update_nodemap()
    bc.cont_acq()
    print("cont")
    time.sleep(2)
    bc.stop_cont_acq()
    bc.save_images()
    bc.cont_acq()
    print("cont")
    time.sleep(2)
    bc.stop_cont_acq()
    bc.close_camera()
    print("done")
    
    
if __name__ == '__main__':
    main()
    