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
FIELDS = ["ExposureTimeRaw",
          "GainRaw",
          "AccuisitionRateRaw"]
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

from tkinter import filedialog




    

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

        for F in (StartPage, ExposurePage):

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
        #label = tk.Label(self, text="Gonio", font=LARGE_FONT)
        #label.pack(pady=10,padx=10)

      

       

        button_start_cam = ttk.Button(self, text="start camera",
                            command=lambda: controller.show_frame(ExposurePage))
        button_start_cam.grid(row=0, column=0)
        
        button_stop_cam = ttk.Button(self, text="stop camera",
                            command=lambda: controller.show_frame(ExposurePage))
        button_stop_cam.grid(row=0, column=1)
        
        button_read_value = ttk.Button(self, text="read value",
                            command=lambda: controller.show_frame(WhiteRefPage))
        button_read_value.grid(row=1,column=0)
        
        button_set_value = ttk.Button(self, text="set value",
                            command=lambda: controller.show_frame(MotorPage))
        button_set_value.grid(row=1,column=1)


        field_combo = ttk.Combobox(self, values=FIELDS, state="readonly")
        field_combo.grid(row=2, column=0)
        field_combo.current(0)
        value_entry = tk.Entry(self)
        value_entry.grid(row=2,column=1)
        value_entry.insert(0, "value...")
        
        unit_label = tk.Label(self, text="ms")
        unit_label.grid(row=2,column=2)
        
        red_label = tk.Label(self, text="red")
        red_label.grid(row=3, column=0)
        self.red_LED = ttk.Combobox(self, values=LED_WAVELENGTHS, state="readonly")
        self.red_LED.grid(row=3,column=1, columnspan=2)
        self.red_LED.current(5)

        green_label = tk.Label(self, text="green")
        green_label.grid(row=4, column=0)
        self.green_LED = ttk.Combobox(self, values=LED_WAVELENGTHS, state="readonly")
        self.green_LED.grid(row=4,column=1, columnspan=2)
        self.green_LED.current(4)

        blue_label = tk.Label(self, text="blue")
        blue_label.grid(row=5, column=0)
        self.blue_LED = ttk.Combobox(self, values=LED_WAVELENGTHS, state="readonly")
        self.blue_LED.grid(row=5,column=1, columnspan=2)
        self.blue_LED.current(2)
    
        button_choose_protocol = ttk.Button(self, text="choose protocol file",
                            command=lambda: self.file_dialog())
        button_choose_protocol.grid(row=6,column=0,columnspan=3)
        self.label_protocol_filename =  blue_label = ttk.Label(self, text="")
        self.label_protocol_filename.grid(row=7,column=0,columnspan=3)
        
        self.display_cb = tk.IntVar()
        ttk.Checkbutton(self, text="display live image", variable=self.display_cb).grid(row=8, column=0, sticky=tk.E)
        self.save_cb = tk.IntVar()
        ttk.Checkbutton(self, text="save images", variable=self.save_cb).grid(row=8, column=1, sticky=tk.E)
        button_start_measurement = ttk.Button(self, text="start measurement",
                            command=lambda: self.file_dialog())
        button_start_measurement.grid(row=9,column=0,columnspan=3)
    


    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Choose protocol", filetype = (("CSV Files","*.csv"),))
        self.label_protocol_filename.configure(text=self.filename)





class ExposurePage(tk.Frame):
    class_canvas = None
    def __init__(self, parent, controller):
        pass
        tk.Frame.__init__(self, parent)

        self.controller = controller
        ExposurePage.class_canvas = FigureCanvasTkAgg(f, self)
##
##
##        
##        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
##        label.pack(pady=10,padx=10)
##
##        button1 = ttk.Button(self, text="draw",
##                            command=lambda: self.draw())
##        button1.pack()
##        
##        
##        button2 = ttk.Button(self, text="update graph",
##                            command=lambda: self.update_graph())
##        button2.pack()
##
##        label_exp_time = tk.Label(self, text="enter exposure time below")
##        label_exp_time.pack()
##        e = tk.Entry(self)
##        e.pack()
##        #e.delete(0, END)
##        e.insert(0, "Exposure time")
##        
##        button3 = ttk.Button(self, text="update exposure time",
##                            command=lambda: self.update_exposure_time(e.get()))
##        button3.pack()
##        
##        button4 = ttk.Button(self, text="close camera",
##                            command=lambda: self.close_camera())
##        button4.pack()
##         
##        #button5 = ttk.Button(self, text="start live",
##        #                    command=lambda: self.start_live_view())
##        #button5.pack()
##        
##        #button6 = ttk.Button(self, text="stop live",
##        #                    command=lambda: self.stop_live_view())
##        #button6.pack()
##        
##        self.red_LED = ttk.Combobox(self, 
##                            values=LED_WAVELENGTHS, state="readonly")
##        self.green_LED = ttk.Combobox(self, 
##                            values=LED_WAVELENGTHS, state="readonly")
##        self.blue_LED = ttk.Combobox(self, 
##                            values=LED_WAVELENGTHS, state="readonly")
##        
##        self.red_LED.pack()
##        self.red_LED.current(2)
##        self.green_LED.pack()
##        self.green_LED.current(4)
##        self.blue_LED.pack()
##        self.blue_LED.current(5)
##        
##
##
##       
##        ExposurePage.class_canvas.draw()
##        ExposurePage.class_canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
##
##        toolbar = NavigationToolbar2Tk(ExposurePage.class_canvas, self)
##        toolbar.update()
##        ExposurePage.class_canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
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
        
