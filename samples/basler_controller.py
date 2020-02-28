# LoadAndSaveConfig.py
from pypylon import pylon
import platform
import time
import threading

#import logging, sys

class BaslerController(object):
    """ blucontroller class for the basler camera """

    def __init__(self):
        self.img = pylon.PylonImage()
        self.cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.nbr_im = 9
        
        
    def open_camera(self):
        self.cam.Open()
    
    def close_camera(self):
        self.cam.Close()
        
        
    def update_nodemap(self):
        # The name of the pylon file handle
        nodeFile = "daA1600-60um_exp_1000.pfs"

        # Print the model name of the camera.
        print("Using device ", self.cam.GetDeviceInfo().GetModelName())

        # featurePersistence = pylon.FeaturePersistence()

        # read the content of the file back to the camera's node map with enabled validation.
        print("Updating nodefile to camera's node map...")
        pylon.FeaturePersistence.Load(nodeFile, self.cam.GetNodeMap(), True)
        
    
    def cont_acq(self):
        """starting a continuos exposure, stopped by setting the stop function"""
        self._stop_cont_acq = False
        self.thread_cont = threading.Thread(target=self.__cont_acq, args=(lambda : self._stop_cont_acq,))
        self.thread_cont.start()
        
    def stop_cont_acq(self):
        self._stop_cont_acq = True
        print("stop sent")
        self.thread_cont.join()
    
    def __cont_acq(self, stop):
        self.cam.StartGrabbing()
        t_grab = time.time()
        for i in range(1000):
            if stop():
                print("STOP!!!!!!")
                break
            with self.cam.RetrieveResult(2000) as result:
                # Calling AttachGrabResultBuffer creates another reference to the
                # grab result buffer. This prevents the buffer's reuse for grabbing.
                self.img.AttachGrabResultBuffer(result)

                # In order to make it possible to reuse the grab result for grabbing
                # again, we have to release the image (effectively emptying the
                # image object).
                self.img.Release()
                if i % 10 == 0:
                    print(i)
                    # Printing every 10 exposures
        self.cam.StopGrabbing()
        print("Continuous acquisition stopped after", time.time() - t_grab, "seconds")
    
    
    def save_images(self):
        """"Saving a number of images to the harddrive"""

        self.cam.StartGrabbing()
        t_grab = time.time()
        for i in range(self.nbr_im):
            with self.cam.RetrieveResult(2000) as result:

                # Calling AttachGrabResultBuffer creates another reference to the
                # grab result buffer. This prevents the buffer's reuse for grabbing.
                self.img.AttachGrabResultBuffer(result)
                filename = "saved_pypylon_img_%d.tiff" % i
                self.img.Save(pylon.ImageFileFormat_Tiff , filename)

                # In order to make it possible to reuse the grab result for grabbing
                # again, we have to release the image (effectively emptying the
                # image object).
                self.img.Release()
        print("time of only grabbing 9 im, (no startup): ", time.time() - t_grab)
        self.cam.StopGrabbing()
        
