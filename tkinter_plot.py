# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	


# TODO: browse folder to initiate bc
#move variables to bc such as dynamic range
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import time
#from basler_controller import BaslerController
import sys
import numpy as np
import matplotlib.pyplot as plt

from queue import Queue
from queue import Empty
import threading

MAX_QSIZE = 10
LED_WAVELENGTHS = ["365 nm",
                   "405",
                   "430",
                   "490",
                   "525",
                   "630",
                   "810",
                   "940",]
LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
fig_image = f.add_subplot(211)
fig_hist = f.add_subplot(212)
#folder_path = "/home/pi/Desktop/BrickPi3-master/Software/Python/Testing Scripts/pypylon/images/" 
#folder_path = "/" + time.strftime("%Y%m%d-%H%M%S/")
folder_path = "sample_imgs/" + time.strftime("%Y%m%d-%H%M%S/")
q = Queue(maxsize=MAX_QSIZE)
bc = None#BaslerController(folder_path, q)
#bc = BaslerController(folder_path)






    

def animate(i):
    pass
    
            

class GoniometerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        

        self.nbr_exposures = 9
        self.led_background = -1
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Goniometer")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, ExposurePage, WhiteRefPage, MotorPage, MeasurementPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

      

       

        button1 = ttk.Button(self, text="1. Set exposure time",
                            command=lambda: controller.show_frame(ExposurePage))
        button1.pack()
        
        button2 = ttk.Button(self, text="2. Calibrate to white reference",
                            command=lambda: controller.show_frame(WhiteRefPage))
        button2.pack()
        
        button3 = ttk.Button(self, text="3. Calibrate goniometer motors",
                            command=lambda: controller.show_frame(MotorPage))
        button3.pack()
        
        butto4 = ttk.Button(self, text="4. Start measurement",
                            command=lambda: controller.show_frame(MeasurementPage))
        butto4.pack()


class MeasurementPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(MotorPage))
        button2.pack()

class WhiteRefPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas = FigureCanvasTkAgg(f, self)
        self.color_img = None
        self.calib_val_red = 1
        self.calib_val_green = 1
        self.calib_val_blue = 1
        
        
        label = tk.Label(self, text="WhiteRefPage!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Update color image",
                            command=lambda: self.show_color_image())
        button2.pack()
        button3 = ttk.Button(self, text="Chose calibration area",
                            command=lambda: self.get_area())
        button3.pack()


        
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def get_area(self):
        plt.imshow(self.color_img)
        plt.show(block=False)
        reference_coords = plt.ginput(2)
        self.x_start = int(round(reference_coords[0][0]))
        self.x_end = int(round(reference_coords[1][0]))
        self.y_start = int(round(reference_coords[0][1]))
        self.y_end = int(round(reference_coords[1][1]))
        print(reference_coords)

    def calibrate_area(self):
        white_ref = self.color_img[self.x_start:self.x_end, self.y_start, self.y_end,:]
        self.calib_val_red = white_ref[:,:,0].mean()
        self.calib_val_green = white_ref[:,:,1].mean()
        self.calib_val_blue = white_ref[:,:,2].mean()
        print(self.calib_val_red)
        print(self.calib_val_green)
        print(self.calib_val_blue)
        
        self.color_img[:,:,0] = self.color_img[:,:,0] / self.calib_val_red
        self.color_img[:,:,1] = self.color_img[:,:,1] / self.calib_val_green
        self.color_img[:,:,2] = self.color_img[:,:,2] / self.calib_val_blue
        self.color_img = self.color_img/np.max(self.color_img)

   




class MotorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(MeasurementPage))
        button2.pack()


class ExposurePage(tk.Frame):
    class_canvas = None
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        ExposurePage.class_canvas = FigureCanvasTkAgg(f, self)


        
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="draw",
                            command=lambda: self.draw())
        button1.pack()
        
        
        button2 = ttk.Button(self, text="update graph",
                            command=lambda: self.update_graph())
        button2.pack()

        label_exp_time = tk.Label(self, text="enter exposure time below")
        label_exp_time.pack()
        e = tk.Entry(self)
        e.pack()
        #e.delete(0, END)
        e.insert(0, "Exposure time")
        
        button3 = ttk.Button(self, text="update exposure time",
                            command=lambda: self.update_exposure_time(e.get()))
        button3.pack()
        
        button4 = ttk.Button(self, text="close camera",
                            command=lambda: self.close_camera())
        button4.pack()
         
        #button5 = ttk.Button(self, text="start live",
        #                    command=lambda: self.start_live_view())
        #button5.pack()
        
        #button6 = ttk.Button(self, text="stop live",
        #                    command=lambda: self.stop_live_view())
        #button6.pack()
        
        self.red_LED = ttk.Combobox(self, 
                            values=LED_WAVELENGTHS, state="readonly")
        self.green_LED = ttk.Combobox(self, 
                            values=LED_WAVELENGTHS, state="readonly")
        self.blue_LED = ttk.Combobox(self, 
                            values=LED_WAVELENGTHS, state="readonly")
        
        self.red_LED.pack()
        self.red_LED.current(2)
        self.green_LED.pack()
        self.green_LED.current(4)
        self.blue_LED.pack()
        self.blue_LED.current(5)
        


       
        ExposurePage.class_canvas.draw()
        ExposurePage.class_canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(ExposurePage.class_canvas, self)
        toolbar.update()
        ExposurePage.class_canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def draw(i):
        ExposurePage.class_canvas.draw()
        print("redrawing")
            
    
    def close_camera(self):
        self.stop_live_view()
        bc.stop_cont_acq()
        bc.close_camera()
    
    def consumer_thread(self, stop):
        #
        print("in thread")
        while not stop():
            
            print("----------stop is {}".format(stop()))
            i = 0
            images = []
            while i < 9:

                #img = plt.imread("sample_imgs/{}.tiff".format(i))

                try:
                    img = q.get(timeout=1)
                except Empty:
                    print("timeout reached, i is {}".format(i))
                    if stop():
                        break
                else:
                    #
                    images.append(img)
                    q.task_done()
                    
                    i += 1
             
            
           
            
            #self.canvas.draw()
            print("show images now")
            self.show_color_image(images)
        print("bottom")
            

    def show_color_image(self, images):
        #add option of chosing red green blue leds
        print("show colorim")
        print("red is {} green is {} blue is {}".format(self.red_LED.get(), 
                                                        self.green_LED.get(), 
                                                        self.blue_LED.get(),))
        #self.comboExample.current()
        
        dynamic_range = 4095#65520
        darkest_img_mean = sys.maxsize
        index_background = -1
        i = 0
        fig_hist.clear()
        for image in images:
            img_mean = image.mean()
            fig_hist.hist(image.flatten(), 32, label='LED {}'.format(i), alpha=0.5)
            print("LED {} has a mean off: {}".format(i, img_mean))
            if img_mean < darkest_img_mean:
                darkest_img_mean = img_mean
                index_background = i
            i += 1
        fig_hist.legend(loc='upper right')
        self.controller.led_background = index_background
        #todo fix what colors
        img_off =images[0]
        img_r =images[6]
        img_g =images[5]
        img_b =images[3]
        #img_r = plt.imread("sample_imgs/{}.tiff".format((self.controller.led_background + 6) % 9))
        #img_g = plt.imread("sample_imgs/{}.tiff".format((self.controller.led_background + 5) % 9))
        #img_b = plt.imread("sample_imgs/{}.tiff".format((self.controller.led_background + 3) % 9))
        self.color_img = np.ndarray(shape=(img_r.shape + (3,)),dtype=float)
        red = (img_r).astype(float)
        red = red/dynamic_range
        green = (img_g).astype(float)
        green = green/dynamic_range
        blue = (img_b).astype(float)
        blue = blue/dynamic_range
        self.color_img[:,:,0] = red
        self.color_img[:,:,1] = green
        self.color_img[:,:,2] = blue
        fig_image.clear()
        fig_image.imshow(self.color_img)
        #ExposurePage.draw(0)
       
    
    def update_exposure_time(self, exp_time):
        print("new exp time: " + exp_time)
        bc.update_value_nodemap("ExposureTimeRaw", exp_time)
        #nodemap etc
    
    def start_live_view(self):
        self.stop_threads = False
        self.cons_thread = threading.Thread(target=self.consumer_thread, args =(lambda : self.stop_threads, ))
        self.cons_thread.start()
    
    def stop_live_view(self):
        self.stop_threads = True
        #self.cons_thread.join()
        
    def update_graph(self):
        
        bc.open_camera()
        bc.update_nodemap()
        bc.cont_acq()
        stop_threads = False
        #consumer_thread = threading.Thread(target=self.consumer_thread, args =(lambda : stop_threads, ))
        #consumer_thread.start()
        print("thread started")
        self.start_live_view()
        #time.sleep(1)
        #stop_threads = True
        #consumer_thread.join()
        
        


    def help_method(self):
        self.controller.led_background = 0
        print(self.controller.led_background)


app = GoniometerApp()
#ani = animation.FuncAnimation(f, animate, interval=2000)
ani = animation.FuncAnimation(f, ExposurePage.draw, interval=2000)
app.mainloop()
        
