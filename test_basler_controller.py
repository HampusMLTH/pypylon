from basler_controller import BaslerController
import time

def main():
    folder_path = "/media/pi/DAPHNIA/goniometer/"
    bc = BaslerController(folder_path)
    #bc.close_camera()
    bc.open_camera()
    bc.update_nodemap()
    bc.cont_acq()
    print("cont")
    time.sleep(2)
    bc.stop_cont_acq()
    bc.save_images()
    bc.cont_acq() #maybe this one should be started in save images, alt move the files in a separate method
    print("cont")
    time.sleep(2)
    bc.stop_cont_acq()
    bc.close_camera()
    print("done")
    
    
if __name__ == '__main__':
    main()
    