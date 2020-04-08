# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	


# TODO: browse folder to initiate bc
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import time
from basler_controller import BaslerController
import sys
import numpy as np
import matplotlib.pyplot as plt

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
#folder_path = "/home/pi/Desktop/BrickPi3-master/Software/Python/Testing Scripts/pypylon/images/" 
folder_path = "/" + time.strftime("%Y%m%d-%H%M%S/")
#bc = BaslerController(folder_path)


def update_exposure_time(exp_time):
    print(exp_time)
    #nodemap etc


    


    
            

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
        
        
        label = tk.Label(self, text="WhiteRefPage!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Update color image",
                            command=lambda: self.show_color_image())
        button2.pack()


        
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def show_color_image(self):
        #add option of chosing red green blue leds
        print("show colorim")
        dynamic_range = 256#65520
        img_off = plt.imread("sample_imgs/{}.tiff".format(self.controller.led_background))
        img_r = plt.imread("sample_imgs/{}.tiff".format((self.controller.led_background + 6) % 9))
        img_g = plt.imread("sample_imgs/{}.tiff".format((self.controller.led_background + 5) % 9))
        img_b = plt.imread("sample_imgs/{}.tiff".format((self.controller.led_background + 3) % 9))
        color_img = np.ndarray(shape=(img_r.shape + (3,)),dtype=float)
        red = (img_r).astype(float)
        red = red/dynamic_range
        green = (img_g).astype(float)
        green = green/dynamic_range
        blue = (img_b).astype(float)
        blue = blue/dynamic_range
        color_img[:,:,0] = red
        color_img[:,:,1] = green
        color_img[:,:,2] = blue
        a.clear()
        a.imshow(color_img)
        self.canvas.draw()




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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.canvas = FigureCanvasTkAgg(f, self)


        
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
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
                            command=lambda: update_exposure_time(e.get()))
        button3.pack()


       
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_graph(self):
        darkest_img_mean = sys.maxsize
        index_background = -1
        a.clear()

        for i in range(0, 9):
            
            img = plt.imread("sample_imgs/{}.tiff".format(i))
            a.hist(img.flatten(), 32, label='LED {}'.format(i), alpha=0.5)
            print("LED {} has a mean off: {}".format(i, img.mean()))
            if img.mean() < darkest_img_mean:
                darkest_img_mean = img.mean()
                index_background = i
        self.controller.led_background = index_background
        a.legend(loc='upper right')
        self.canvas.draw()


    def help_method(self):
        self.controller.led_background = 0
        print(self.controller.led_background)


app = GoniometerApp()
#ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
        