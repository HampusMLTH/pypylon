# LoadAndSaveConfig.py
from pypylon import pylon
import platform
import time
from multiprocessing import Process, Event
#import logging, sys
   
    
def update_nodemap():
    # TODO: Change all prints to logging debug
    #logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    #logging.debug('A debug message!')
    #logging.info('We processed %d records', len(processed_records)) 
    # The name of the pylon file handle
    nodeFile = "daA1600-60um_exp_1000.pfs"

    # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    # featurePersistence = pylon.FeaturePersistence()


    # Just for demonstration, read the content of the file back to the camera's node map with enabled validation.
    print("Updating nodefile to camera's node map...")
    pylon.FeaturePersistence.Load(nodeFile, camera.GetNodeMap(), True)
    # Close the camera.
    camera.Close()
    
def save_images(num_img_to_save = 9):
    img = pylon.PylonImage()
    tlf = pylon.TlFactory.GetInstance()

    cam = pylon.InstantCamera(tlf.CreateFirstDevice())
    cam.Open()
    cam.StartGrabbing()
    t_grab = time.time()
    for i in range(num_img_to_save):
        with cam.RetrieveResult(2000) as result:

            # Calling AttachGrabResultBuffer creates another reference to the
            # grab result buffer. This prevents the buffer's reuse for grabbing.
            img.AttachGrabResultBuffer(result)

            if platform.system() == 'Windows':
                # The JPEG format that is used here supports adjusting the image
                # quality (100 -> best quality, 0 -> poor quality).
                #ipo = pylon.ImagePersistenceOptions()
                #quality = 90 - i * 10
                #ipo.SetQuality(quality)

                filename = "saved_pypylon_img_%d.tiff" % i
                img.Save(pylon.ImageFileFormat_Tiff, filename)
            else:
                filename = "saved_pypylon_img_%d.tiff" % i
                img.Save(pylon.ImageFileFormat_Tiff , filename)

            # In order to make it possible to reuse the grab result for grabbing
            # again, we have to release the image (effectively emptying the
            # image object).
            img.Release()
    print("time of only grabbing 9 im, (no startup): ", time.time() - t_grab)
    cam.StopGrabbing()
    cam.Close()
    
def cont_acq(event_stop):
    img = pylon.PylonImage()
    tlf = pylon.TlFactory.GetInstance()

    cam = pylon.InstantCamera(tlf.CreateFirstDevice())
    cam.Open()
    cam.StartGrabbing()
    t_grab = time.time()
    for i in range(1000):
        if event_stop.is_set():
            event_stop.clear()
            break
        with cam.RetrieveResult(2000) as result:

            # Calling AttachGrabResultBuffer creates another reference to the
            # grab result buffer. This prevents the buffer's reuse for grabbing.
            img.AttachGrabResultBuffer(result)

           
            # In order to make it possible to reuse the grab result for grabbing
            # again, we have to release the image (effectively emptying the
            # image object).
            img.Release()
            if i % 10 == 0:
                print(i)
    print("Continuous acquisition stopped after", time.time() - t_grab, "seconds")
    cam.StopGrabbing()
    cam.Close()

    