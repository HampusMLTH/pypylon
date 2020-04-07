# ===============================================================================
#    This sample illustrates how to grab and process images using the CInstantCamera class.
#    The images are grabbed and processed asynchronously, i.e.,
#    while the application is processing a buffer, the acquisition of the next buffer is done
#    in parallel.
#
#    The CInstantCamera class uses a pool of buffers to retrieve image data
#    from the camera device. Once a buffer is filled and ready,
#    the buffer can be retrieved from the camera object for processing. The buffer
#    and additional image data are collected in a grab result. The grab result is
#    held by a smart pointer after retrieval. The buffer is automatically reused
#    when explicitly released or when the smart pointer object is destroyed.
# ===============================================================================
from pypylon import pylon
from pypylon import genicam
import numpy as np
import matplotlib.pyplot as plt
import time

import sys

nodemap_uploaded = 0

def main():
    img_list = grab_im()
    img_list2 = grab_im()
    img_list3 = grab_im()
    img_list4 = grab_im()
    i = 0
    mean_vals = []
    mean_vals2 = []
    mean_vals3 = []
    mean_vals4 = []
    figure_hist = plt.figure(1)

    for img in img_list2:
       mean_vals2.append(img.mean())
    for img in img_list3:
       mean_vals3.append(img.mean())
    for img in img_list4:
       mean_vals4.append(img.mean())
    for img in img_list:
        plt.hist(img[i].flatten(), 32, range=[0,256], label='LED {}'.format(i), alpha=0.5)
        #plt.hist(img[-1,:], 32, range=[0,256], label='last row', alpha=0.5)
        #plt.legend(loc='upper right')
        i += 1
        mean_vals.append(img.mean())
    
    print("Mean Values:")
    
    print(mean_vals2)
    print(mean_vals3)
    print(mean_vals4)
    print(mean_vals)
    plt.legend(loc='upper right')
    darkest_led = mean_vals.index(min(mean_vals))
    brightest_led = mean_vals.index(max(mean_vals))
    print("darkest is LED {}".format(darkest_led))
    print("brightest is LED {}".format(brightest_led))
    print("diff is {}".format(mean_vals[brightest_led] - mean_vals[darkest_led]))
    figure_darkest_image = plt.figure(2)
    plt.imshow(img_list[darkest_led])
    figure_brightest_image = plt.figure(3)
    plt.imshow(img_list[brightest_led])
    
    red = (darkest_led + 6) % 9
    print("red is {}".format(red))
    
    
    green = (darkest_led + 5) % 9
    print("green is {}".format(green))
    
    
    blue = (darkest_led + 3) % 9
    print("blue is {}".format(blue))
    #make color image
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
    
    color_fig = plt.figure(4)
    #import pdb;pdb.set_trace()
    #color_im = [img_list[red], img_list[green], img_list[blue]]
    #print(color_im.shape)
    cim = np.ndarray(shape=(1200,1586,3),dtype=int)


    cim[:,:,0] = img_list[red]
    cim[:,:,1] = img_list[green]
    cim[:,:,2] = img_list[blue]
    
    #scale down red
    cim[:,:,0] = cim[:,:,0]*140/180
    plt.imshow(cim)
    
    #plt.imshow()
    plt.show()
    
    
def nodemap(cam):
    print("Updating nodefile to camera's node map...")
    node_file = "daA1600-60um_gain.pfs"
    pylon.FeaturePersistence.Load(node_file, cam.GetNodeMap(), True)

def grab_im():
    global nodemap_uploaded
    # Number of images to be grabbed.
    countOfImagesToGrab = 9

    # The exit code of the sample application.
    exitCode = 0

    try:
        # Create an instant camera object with the camera device found first.
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()
        if not nodemap_uploaded:
            nodemap(camera)
            nodemap_uploaded = 1

        # Print the model name of the camera.
        print("Using device ", camera.GetDeviceInfo().GetModelName())

        # demonstrate some feature access
        new_width = camera.Width.GetValue() - camera.Width.GetInc()
        if new_width >= camera.Width.GetMin():
            camera.Width.SetValue(new_width)

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer = 5

        # Start the grabbing of c_countOfImagesToGrab images.
        # The camera device is parameterized with a default configuration which
        # sets up free-running continuous acquisition.
        camera.StartGrabbingMax(countOfImagesToGrab)

        # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        # when c_countOfImagesToGrab images have been retrieved.
        img_list = []
        while camera.IsGrabbing():
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            # Image grabbed successfully?
            if grabResult.GrabSucceeded():
                # Access the image data.
                #print("SizeX: ", grabResult.Width)
                #print("SizeY: ", grabResult.Height)
                img = grabResult.Array
                #print("Gray value of first pixel: ", img[0, 0])
                #print(type(img))
                img_list.append(img)
                #import pdb;pdb.set_trace()
                #plt.hist(img[0,:], 32, range=[0,256], label='first row', alpha=0.5)
                #plt.hist(img[-1,:], 32, range=[0,256], label='last row', alpha=0.5)
                #plt.legend(loc='upper right')
                #plt.show()
                time.sleep(1)
            else:
                print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
            grabResult.Release()
        camera.Close()
        #import pdb;pdb.set_trace()
        return img_list

    except genicam.GenericException as e:
        # Error handling.
        print("An exception occurred.")
        print(e.GetDescription())
        exitCode = 1

if __name__ == '__main__':
    main()
    

