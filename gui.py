from basler_controller import BaslerController
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
from queue import Queue
from queue import Empty

def main():
    nbr_im=9
    
    #folder_path = "/home/pi/Desktop/BrickPi3-master/Software/Python/Testing Scripts/pypylon/images/" + time.strftime("%Y%m%d-%H%M%S/")
    gui_folder_name = "gui_test_1"
    folder_path = "sample_imgs/" + time.strftime("%Y%m%d-%H%M%S/")
    q = Queue(maxsize=MAX_QSIZE)
    bc = BaslerController(folder_path, q)
    
    #bc.close_camera()
    bc.open_camera()
    bc.update_nodemap()
    bc.cont_acq()
    print("cont")
    time.sleep(2)
    bc.save_images("gui_test_1")
    # make this wait a method
    while(not bc.thread_move):
        time.sleep(1)
        print("move not started")
    while(bc.thread_move.isAlive()):
        time.sleep(1) # todo make this sleep small or remove
        print("move ongoing")
    print("move done")
    
    lowest_mean = sys.maxsize
    index_off = -1
    
    for i in range(0, nbr_im):
        
        a = plt.imread(folder_path + gui_folder_name + "/{}.tiff".format(i))
        plt.hist(a.flatten(), 32, label='LED {}'.format(i), alpha=0.5)
        print("LED {} has a mean off: {}".format(i, a.mean()))
        if a.mean() < lowest_mean:
            lowest_mean = a.mean()
            index_off = i
    
    plt.legend(loc='upper right')
    plt.show()
#    print("input new exposure time in µs")
#    new_exp_time = input()
#    bc.update_value_nodemap("ExposureTimeRaw", new_exp_time)
#    bc.stop_cont_acq()
#    bc.update_nodemap()
#    
#    bc.cont_acq()
#    print("cont")
#    time.sleep(1)
#    bc.save_images("gui_test_2")
#    # make this wait a method
#    
#    while(bc.thread_move.isAlive()):
#        time.sleep(1) # todo make this sleep small or remove
#        print("move ongoing")
#    print("move done")
#    lowest_mean = sys.maxsize
#    index_off = -1
#    for i in range(0, nbr_im):
#        
#        a = plt.imread(folder_path + gui_folder_name + "/{}.tiff".format(i))
#        plt.hist(a.flatten(), 32, label='LED {}'.format(i), alpha=0.5)
#        print("LED {} has a mean off: {}".format(i, a.mean()))
#        if a.mean() < lowest_mean:
#            lowest_mean = a.mean()
#            index_off = i
#        
#    
#    plt.legend(loc='upper right')
#    plt.show()
    
    # create color_image
    #dark is 0
    # 1 365
    # 2 405
    # 3 430 (blue)
    # 4 490
    # 5 525 (green)
    # 6 630 (red)
    # 7 810
    # 8 940
    #
    #import pdb;pdb.set_trace()
    img_off = plt.imread(folder_path + gui_folder_name + "/{}.tiff".format(index_off))
    img_r = plt.imread(folder_path + gui_folder_name + "/{}.tiff".format((index_off + 6) % 9))
    img_g = plt.imread(folder_path + gui_folder_name + "/{}.tiff".format((index_off + 5) % 9))
    img_b = plt.imread(folder_path + gui_folder_name + "/{}.tiff".format((index_off + 3) % 9))
    
    dynamic_range = 65520
    
#    current_fig = plt.figure(1)
#    plt.imshow(img_off)
#    current_fig = plt.figure(2)
#    red = (img_r).astype(float)
#    red = red/dynamic_range
#    plt.imshow(red)
#    current_fig = plt.figure(3)
#    plt.imshow(img_g)
#    current_fig = plt.figure(4)
#    plt.imshow(img_b)
    
    
    
    color_img = np.ndarray(shape=(img_r.shape + (3,)),dtype=float)
    
#    red = (img_r - img_off).astype(float)
#    red = red/dynamic_range
#    green = (img_g - img_off).astype(float)
#    green = green/dynamic_range
#    blue = (img_b - img_off).astype(float)
#    blue = blue/dynamic_range
#    color_img[:,:,0] = red
#    color_img[:,:,1] = green
#    color_img[:,:,2] = blue
#    
#    current_fig = plt.figure(5)
#    plt.imshow(red)
#    current_fig = plt.figure(6)
#    plt.imshow(green)
#    current_fig = plt.figure(7)
#    plt.imshow(blue)
#    
#    current_fig = plt.figure(8)
#    
#    plt.imshow(color_img)
    
    current_fig = plt.figure(9)
    red = (img_r).astype(float)
    red = red/dynamic_range
    green = (img_g).astype(float)
    green = green/dynamic_range
    blue = (img_b).astype(float)
    blue = blue/dynamic_range
    color_img[:,:,0] = red
    color_img[:,:,1] = green
    color_img[:,:,2] = blue
    plt.imshow(color_img)
    plt.show(block=False)
    
    
#    print("input calibration values for red [0 - 1]:")
#    calib_red = input()
#    
#    print("input calibration values for green [0 - 1]:")
#    calib_green = input()
#    
#    print("input calibration values for blue [0 - 1]:")
#    calib_blue = input()
#
    print("click in the top left corner and the bottom right corner of a white reference area")
    reference_coords = plt.ginput(2)
    print(reference_coords)
    
    #import pdb; pdb.set_trace()
    white_ref = color_img[int(round(reference_coords[0][0])):int(round(reference_coords[1][0])),
                          int(round(reference_coords[0][1])):int(round(reference_coords[1][1])),:]
    
    calib_val_red = white_ref[:,:,0].mean()
    calib_val_green = white_ref[:,:,1].mean()
    calib_val_blue = white_ref[:,:,2].mean()
    print(calib_val_red)
    print(calib_val_green)
    print(calib_val_blue)
    
    color_img[:,:,0] = color_img[:,:,0] / calib_val_red
    color_img[:,:,1] = color_img[:,:,1] / calib_val_green
    color_img[:,:,2] = color_img[:,:,2] / calib_val_blue
    color_img = color_img/np.max(color_img)
    plt.imshow(color_img)
    plt.show()
    
    bc.stop_cont_acq()
    bc.close_camera()
    print("done")
    
    
if __name__ == '__main__':
    main()
    

