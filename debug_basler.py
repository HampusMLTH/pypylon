from basler_controller import BaslerController
import time

def main():
    i=1
    
    folder_path = "/media/pi/DAPHNIA/goniometer/" + time.strftime("%Y%m%d-%H%M%S/")
    bc = BaslerController(folder_path)
    #bc.close_camera()
    bc.open_camera()
    bc.update_nodemap()
    bc.cont_acq()
    print("cont")
    time.sleep(4)
    bc.save_images("test_1")
    time.sleep(13)
    bc.stop_cont_acq()
    bc.close_camera()
    print("done")
    
    
if __name__ == '__main__':
    main()
    
