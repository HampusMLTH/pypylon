# LoadAndSaveConfig.py
from pypylon import pylon
from queue import Queue
import platform
import time
import threading
import shutil
import os
import imageio

#import logging, sys

class BaslerController(object):
    """ Controller class for the basler camera """
    

    def __init__(self, folder_path, queue):
        self.queue = queue
        self.img = pylon.PylonImage()
        self.cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.nbr_im = 9
        self.folder_path = folder_path
        os.mkdir(self.folder_path) # unique folder for this measurement
        self.counter = 0
        self.thread_move = None
        self.nodefile = "acA1920-155um_bin_3.pfs"#"daA1600-60um_gain.pfs"#"acA1920-155um_bin_2.pfs"#"daA1600-60um_gain.pfs"
        
        
    def open_camera(self):
        self.cam.Open()
    
    def close_camera(self):
        self.cam.Close()
    
    def update_nodemap_value(self, field, new_value):
        file = open(self.nodefile, "r")
        new_file_contents = ""
        for line in file:
            if field in line:
                print(field + "updated from {} to {}".format(line.split()[1], str(new_value)))
                line = line.replace(line.split()[1], str(new_value))
            new_file_contents += line
        file.close()
        file = open(self.nodefile, "w")
        file.write(new_file_contents)
        file.close()
    
    def get_nodemap_value(self, field):
        file = open(self.nodefile, "r")
        for line in file:
             if field in line:
                print("{} is {}".format(field, line.split()[1]))
                value = float(line.split()[1])
                if value.is_integer():
                    value = int(value)
                return(value)
        raise KeyError("{} not in Nodefile {}".format(field, self.nodefile))
                    
    def update_nodemap(self):
        # The name of the pylon file handle
        
        shutil.copy(self.nodefile, self.folder_path + self.nodefile) # make a copy of the settings used for this measurement
        # Print the model name of the camera.
        print("Using device ", self.cam.GetDeviceInfo().GetModelName())

        # featurePersistence = pylon.FeaturePersistence()

        # read the content of the file back to the camera's node map with enabled validation.
        print("Updating nodefile {} to camera's node map.".format(self.nodefile))
        pylon.FeaturePersistence.Load(self.nodefile, self.cam.GetNodeMap(), True)
        
    
    def cont_acq(self):
        """starting a continuos exposure, stopped by setting the stop function"""
        self._stop_cont_acq = False
        self._save_images = False
        self.thread_cont = threading.Thread(target=self._cont_acq,
                                            args=(lambda : self._stop_cont_acq,
                                                  lambda : self._save_images,
                                                  lambda : self._folder_name,))
        self.thread_cont.start()
        
    def stop_cont_acq(self):
        self._stop_cont_acq = True
        print("stop sent")
        
        self.thread_cont.join()
    
    def save_images(self, folder_name):
        self._save_images = True
        self._folder_name = folder_name
        print("save sent")
    
    def _cont_acq(self, stop, save_images, folder_name):
        self.cam.StartGrabbing()
        t_grab = time.time()
        nbr_imgs_saved = 0
        while not stop():
                
            with self.cam.RetrieveResult(2000) as result:
                self.counter = self.counter + 1
                
                #print("putting")
                self.queue.put(result.Array)                
                print("bc queue size: {}".format(self.queue.qsize()))
                # Calling AttachGrabResultBuffer creates another reference to the
                # grab result buffer. This prevents the buffer's reuse for grabbing.
                
                #import pdb;pdb.set_trace()
                #self.img.AttachGrabResultBuffer(result)

                # In order to make it possible to reuse the grab result for grabbing
                # again, we have to release the image (effectively emptying the
                # image object).
               
                if save_images():
                    import pdb;pdb.set_trace()
                    print("save images")
                    #self.img.AttachGrabResultBuffer(result)
                    nbr_imgs_saved += 1
                    filename = "%d.tiff" % (self.counter % 9)
                    #self.img.Save(pylon.ImageFileFormat_Tiff , filename)
                    imageio.imwrite(filename, result.Array)
                    if nbr_imgs_saved == self.nbr_im:
                        self._save_images = False
                        #move images
                        #check if previous move images is done, otherwise throw error
                        if self.thread_move:
                            if self.thread_move.isAlive():
                                raise BufferError("last batch of are currently being moved, you should lower frame rate or get a faster harddrive.")
                        self.thread_move = threading.Thread(target=self._move_images, args=(folder_name(),))
                        self.thread_move.start()
                
                #if self.thread_move:
                 #   if self.thread_move.isAlive():
                  #      print("Moving thread active!")
                   # else:
                        #print("not active")
                #print(self.counter % 9, end = ',')
                
                #self.img.Release()
                #if i % 10 == 0:
                    #print(i)
                    #print("counter at %d" % self.counter)
                    #print("mod %d" % (self.counter % 9))
                    # Printing every 10 exposures
        self.cam.StopGrabbing()
        print("Continuous acquisition stopped after", time.time() - t_grab, "seconds")
    
    
    
    
    def _move_images(self, folder_name):
        t_move = time.time()
        #timestr = time.strftime("%Y%m%d-%H%M%S/")
        #coord_str = "led_{}_stage_{}_sample_{}/".format(coords[0], coords[1], coords[2])
        os.mkdir(self.folder_path  + folder_name)
        for i in range(self.nbr_im):
            print("moving {}".format(i))
            
            #shutil.move("{}.tiff".format((self.counter + i) % 9), self.folder_path  + coord_str + "{}.tiff".format((self.counter + i) % 9))
            shutil.move("{}.tiff".format(i), self.folder_path  + folder_name + "/{}.tiff".format(i))
        print("time of moving 9 images: ", time.time() - t_move)
    
    def move_images(self, coords):
        t_move = time.time()
        #timestr = time.strftime("%Y%m%d-%H%M%S/")
        coord_str = "led_{}_stage_{}_sample_{}/".format(coords[0], coords[1], coords[2])
        os.mkdir(self.folder_path  + coord_str)
        for i in range(self.nbr_im):
            print("moving {}".format((self.counter + i) % 9))
            print("counter is {}".format(self.counter))
            shutil.move("{}.tiff".format((self.counter + i) % 9), self.folder_path  + coord_str + "{}.tiff".format((self.counter + i) % 9))
        print("time of moving 9 images: ", time.time() - t_move)
        
