from basler_controller import BaslerController
from goniometer_obj import GoniometerObject
import time

def main():
    folder_path = "/media/pi/DAPHNIA/goniometer/" + time.strftime("%Y%m%d-%H%M%S/")
    
    bc = BaslerController(folder_path)
    bc.open_camera()
    bc.update_nodemap()
    bc.cont_acq()
    
    protocol_filename="protocol_test.csv"
    protocol = GoniometerObject.read_csv(protocol_filename)
    go = GoniometerObject()
    go.copy_csv(protocol_filename, folder_path)
    
    for d in protocol:
        print("led:", d[0])
        go.led_angle = int(d[0])
        print("stage:", d[1])
        go.stage_angle = int(d[1])
        print("sample:", d[2])
        go.sample_angle = int(d[2])
        go.done_moving(go.LED)
        go.done_moving(go.STAGE)
        go.done_moving(go.SAMPLE)
        
        bc.stop_cont_acq()
        bc.save_images()
        bc.cont_acq()
        bc.move_images(d)
        
    
    
    #go.led_angle = 15
    #go.done_moving(go.LED)
    print("done main")
    go.BP.reset_all()
    
    # Here we do calibration
    # save csv in folder
    
    # in for 
    # Move to position
    # save images (put in current csv angles)
    bc.stop_cont_acq()
    
if __name__ == '__main__':
    main()
    