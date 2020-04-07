from basler_controller import BaslerController
from goniometer_obj import GoniometerObject
import time

def main():
    #folder_path = "/media/pi/DAPHNIA/goniometer/" + time.strftime("%Y%m%d-%H%M%S/")
    folder_path = "/media/pi/DAPHNIA/goniometer/" + time.strftime("%Y%m%d-%H_%M_%S/")
    bc = BaslerController(folder_path)
    bc.open_camera()
    bc.update_nodemap()
    bc.cont_acq()
    
    protocol_filename="protocol_test.csv"
    protocol = GoniometerObject.read_csv(protocol_filename)
    go = GoniometerObject()
    go.copy_csv(protocol_filename, folder_path)
    
    time.sleep(10)
    bc.stop_cont_acq()
    d= [0,0,0]
    bc.nbr_im = 1
    #for d in protocol:
    for i in range(0, 3):
        print("led:", d[0])
        go.led_angle = int(d[0])
        print("stage:", d[1])
        go.stage_angle = int(d[1])
        print("sample:", d[2])
        go.sample_angle = int(d[2])
        go.done_moving(go.LED)
        go.done_moving(go.STAGE)
        go.done_moving(go.SAMPLE)
        
        #bc.stop_cont_acq()
        bc.save_images()
        print("--------------counter at {} mod {}".format(bc.counter, bc.counter % 9))
        
        #bc.cont_acq() # before move im to make continuous
        #
        #tmp = d
        #tmp[0] = i
        
        bc.move_images([i, i, i])
        time.sleep(2)
        #bc.cont_acq()
        
    
    
    #go.led_angle = 15
    #go.done_moving(go.LED)
    print("done main")
    go.BP.reset_all()
    
    # Here we do calibration
    # save csv in folder
    
    # in for 
    # Move to position
    # save images (put in current csv angles)
    #bc.stop_cont_acq()
    
if __name__ == '__main__':
    main()
    