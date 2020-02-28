# LoadAndSaveConfig.py
from pypylon import pylon
import platform
import time
#from multiprocessing import Process, Event
import threading

def main():
    
    cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    cam.Open()
    t0 = time.time()
    
    print("---updating nodemap---")
    update_nodemap(cam)
    print("time updating nodemap:", time.time() - t0)
    # add option of setting exp time etc?

    print("start continuos acq..")
    event_stop = False
    thread_cont = threading.Thread(target=cont_acq, args=(lambda : event_stop, cam,))
    thread_cont.start()
    print("cont acq started, sleep abit..")    
    #print("cont_test->")
    #cont_test(event_stop)
    time.sleep(3)
    
    event_stop = True
    print("stop cont acq")
    thread_cont.join()
    
    t0 = time.time()
    print("---saving  9 images---")
    save_images(cam)

    t_elapsed = time.time() - t0
    print("time saving 9 images:", t_elapsed)
    
    print("start cont acq again")

    event_stop = False
    thread_cont = threading.Thread(target=cont_acq, args=(lambda : event_stop, cam,))

    thread_cont.start()
    time.sleep(6)
    
    event_stop = True
    thread_cont.join()
    cam.Close()
    
    
    
    
    
def update_nodemap(cam):
    # The name of the pylon file handle
    nodeFile = "daA1600-60um_exp_1000.pfs"

    # Create an instant camera object with the camera device found first.
    
    
    # Print the model name of the camera.
    print("Using device ", cam.GetDeviceInfo().GetModelName())

    # featurePersistence = pylon.FeaturePersistence()


    # Just for demonstration, read the content of the file back to the camera's node map with enabled validation.
    print("Updating nodefile to camera's node map...")
    pylon.FeaturePersistence.Load(nodeFile, cam.GetNodeMap(), True)
    # Close the camera.
    #cam.Close()
    
def save_images(cam):
    num_img_to_save = 9
    img = pylon.PylonImage()
    #tlf = pylon.TlFactory.GetInstance()

    #cam = pylon.InstantCamera(tlf.CreateFirstDevice())
    #cam.Open()
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
    #cam.Close()
    
def cont_acq(stop, cam):
    #import pdb
    #pdb.set_trace()
    #print("inside cont_acq")
    img = pylon.PylonImage()
    #tlf = pylon.TlFactory.GetInstance()

    #cam = pylon.InstantCamera(tlf.CreateFirstDevice())
    #cam.Open()
    cam.StartGrabbing()
    t_grab = time.time()
    for i in range(1000):
        if stop():
            print("STOP!!!!!!")
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
    
    cam.StopGrabbing()
    print("Continuous acquisition stopped after", time.time() - t_grab, "seconds")
    #cam.Close()



if __name__ == '__main__':
    main()
    