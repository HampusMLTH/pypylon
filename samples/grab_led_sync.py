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
import time

import sys

# Number of images to be grabbed.
countOfImagesToGrab = 300

# The exit code of the sample application.
exitCode = 0

try:
    
    #    testing numpy
    a = np.array([1,2,3])
    
    # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    
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
    
    camera.LineSelector.SetValue(LineSelector_Line1)
    camera.LineMode.SetValue(LineMode_Output)
    camera.LineSource.SetValue(LineSource_ExposureActive)
    
    camera.StartGrabbingMax(countOfImagesToGrab)
    #camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)
    
    acq_time = 555.55 # arbitrary large float
    total_exp_time = 0
    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when c_countOfImagesToGrab images have been retrieved.
    i = 0
    while camera.IsGrabbing():
        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        start_time = time.time()
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        print("debug")
        # Image grabbed successfully?
        if grabResult.GrabSucceeded():
            # Access the image data.
            end_time = time.time()
            time_elapsed = end_time - start_time
            print("SizeX: ", grabResult.Width)
            print("SizeY: ", grabResult.Height)
            img = np.array(grabResult.Array)
            #print("Gray value of first pixel: ", img[0, 0])
            print("Gray value of ", img.mean())
            print("Time of acqusition: ", time_elapsed)
            total_exp_time = total_exp_time + time_elapsed
            if time_elapsed < acq_time:
                acq_time = time_elapsed
        else:
            print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
        i = i+1
        if i > 10:
            camera.StopGrabbing()
        
        grabResult.Release()
    print("\nFastest acq time: ", acq_time)
    print("mean time: ", total_exp_time/countOfImagesToGrab)
    camera.Close()

except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e.GetDescription())
    exitCode = 1

sys.exit(exitCode)
