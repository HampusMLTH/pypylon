# Connect motors and sensor accordingly:
# Motor port A: Sample motor
# Motor port B: Stage motor
# Motor port C: LED motor
# Motor port D: Polarizer motor
# Sensor port 1: Push button

from goniometer_lib import *
protocole_file_name="protocol.csv"
#sample_name="test"
#####################################################
BP=init_motors()
#camera = init_cam()
protocole=read_csv(protocole_file_name)
#path1=make_folder(sample_name)
#save_csv(path1,protocole)
#fileNameSufix=0
welcome()
for d in protocole:
    led(BP,int(d[0]))
    stage(BP,int(d[1]))
    sample(BP,int(d[2]))
    #capture_cam(camera, int(d[0]),int(d[1]),path1+sample_name+"{:04d}.bmp".format(fileNameSufix))
    #fileNameSufix=fileNameSufix+1
#print("Finished, the files are saved in "+path1)
#camera.close()
BP.reset_all()