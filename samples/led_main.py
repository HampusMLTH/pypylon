# LoadAndSaveConfig.py
from pypylon import pylon
import platform

def main():
    print("---updating nodemap---")
    update_nodemap()
    print("---saving images---")
    save_images()
    
    
def update_nodemap():
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
    
def save_images():
    num_img_to_save = 9
    img = pylon.PylonImage()
    tlf = pylon.TlFactory.GetInstance()

    cam = pylon.InstantCamera(tlf.CreateFirstDevice())
    cam.Open()
    cam.StartGrabbing()
    for i in range(num_img_to_save):
        with cam.RetrieveResult(2000) as result:

            # Calling AttachGrabResultBuffer creates another reference to the
            # grab result buffer. This prevents the buffer's reuse for grabbing.
            img.AttachGrabResultBuffer(result)

            if platform.system() == 'Windows':
                # The JPEG format that is used here supports adjusting the image
                # quality (100 -> best quality, 0 -> poor quality).
                ipo = pylon.ImagePersistenceOptions()
                quality = 90 - i * 10
                ipo.SetQuality(quality)

                filename = "saved_pypylon_img_%d.jpeg" % quality
                img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)
            else:
                filename = "saved_pypylon_img_%d.png" % i
                img.Save(pylon.ImageFileFormat_Png, filename)

            # In order to make it possible to reuse the grab result for grabbing
            # again, we have to release the image (effectively emptying the
            # image object).
            img.Release()

    cam.StopGrabbing()
    cam.Close()

if __name__ == '__main__':
    main()
    