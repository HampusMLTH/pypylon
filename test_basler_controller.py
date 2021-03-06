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
    time.sleep(2)
    bc.stop_cont_acq()
    bc.save_images()
    bc.move_images([i, i, i])
    bc.cont_acq() #maybe this one should be started in save images, alt move the files in a separate method
    print("cont")
    time.sleep(5)
    bc.stop_cont_acq()
    bc.close_camera()
    print("done")
    
    
if __name__ == '__main__':
    main()
    