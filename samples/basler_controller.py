# LoadAndSaveConfig.py
from pypylon import pylon
import platform
import time
import threading
import shutil
import os

#import logging, sys

class BaslerController(object):
    """ blucontroller class for the basler camera """
    

    def __init__(self, folder_path):
        self.img = pylon.PylonImage()
        self.cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.nbr_im = 9
        timestr = time.strftime("%Y%m%d-%H%M%S/")
        self.folder_path = folder_path + timestr
        os.mkdir(self.folder_path) # unique folder for this measurement
        self.counter = 0
        
        
    def open_camera(self):
        self.cam.Open()
    
    def close_camera(self):
        self.cam.Close()
        
        
    def update_nodemap(self):
        # The name of the pylon file handle
        node_file = "daA1600-60um_1000_rp3.pfs"
        shutil.copy(node_file, self.folder_path + node_file) # make a copy of the settings used for this measurement
        # Print the model name of the camera.
        print("Using device ", self.cam.GetDeviceInfo().GetModelName())

        # featurePersistence = pylon.FeaturePersistence()

        # read the content of the file back to the camera's node map with enabled validation.
        print("Updating nodefile to camera's node map...")
        pylon.FeaturePersistence.Load(node_file, self.cam.GetNodeMap(), True)
        
    
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
        for i in range(1000000):
            if stop():
                print("stopping cont acq")
                break
            with self.cam.RetrieveResult(2000) as result:
                self.counter = self.counter + 1
                # Calling AttachGrabResultBuffer creates another reference to the
                # grab result buffer. This prevents the buffer's reuse for grabbing.
                self.img.AttachGrabResultBuffer(result)

                # In order to make it possible to reuse the grab result for grabbing
                # again, we have to release the image (effectively emptying the
                # image object).
                
                self.img.Release()
                if i % 10 == 0:
                    print(i)
                    print("counter at %d" % self.counter)
                    print("mod %d" % (self.counter % 9))
                    # Printing every 10 exposures
        self.cam.StopGrabbing()
        print("Continuous acquisition stopped after", time.time() - t_grab, "seconds")
    
    
    def save_images(self):
        """"Saving a number of images to the harddrive"""

        self.cam.StartGrabbing()
        t_grab = time.time()
        for i in range(self.nbr_im):
            with self.cam.RetrieveResult(2000) as result:
                self.counter = self.counter + 1

                # Calling AttachGrabResultBuffer creates another reference to the
                # grab result buffer. This prevents the buffer's reuse for grabbing.
                self.img.AttachGrabResultBuffer(result)
                filename = "%d.tiff" % (self.counter % 9) # Save with a filename corresponding to the same LED each time
                print("image %d saved with filename " % i + filename)
                self.img.Save(pylon.ImageFileFormat_Tiff , filename)

                # In order to make it possible to reuse the grab result for grabbing
                # again, we have to release the image (effectively emptying the
                # image object).
                print("counter at %d" % self.counter)
                print("mod %d" % (self.counter % 9))
                self.img.Release()
        print("time of only grabbing 9 im, (no startup): ", time.time() - t_grab)
        self.cam.StopGrabbing()
        t_move = time.time()
        timestr = time.strftime("%Y%m%d-%H%M%S/")
        os.mkdir(self.folder_path  + timestr)
        for i in range(self.nbr_im):
            shutil.move("%d.tiff" % i, self.folder_path  + timestr + "%d.tiff" % i)
        print(timestr)
        print("time of moving 9 images: ", time.time() - t_move)
        
