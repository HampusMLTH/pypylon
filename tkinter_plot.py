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


def update_graph(canvas):
    lowest_mean = sys.maxsize
    index_off = -1
    a.clear()

    for i in range(0, 9):
        
        img = plt.imread("sample_imgs/{}.tiff".format(i))
        a.hist(img.flatten(), 32, label='LED {}'.format(i), alpha=0.5)
        print("LED {} has a mean off: {}".format(i, img.mean()))
        if img.mean() < lowest_mean:
            lowest_mean = img.mean()
            index_off = i

    a.legend(loc='upper right')


    #print(message)
    # pullData = open("sampleText.txt","r").read()
    # dataList = pullData.split('\n')
    # xList = []
    # yList = []
    # for eachLine in dataList:
    #     if len(eachLine) > 1:
    #         x, y = eachLine.split(',')
    #         xList.append(int(x))
    #         yList.append(int(y))

    # a.clear()
    # a.plot(xList, yList)
    canvas.draw()

    
            

class GoniometerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
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
        label = tk.Label(self, text="WhiteRefPage!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(MotorPage))
        button2.pack()

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
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        canvas = FigureCanvasTkAgg(f, self)
        
        button2 = ttk.Button(self, text="update graph",
                            command=lambda: update_graph(canvas))
        button2.pack()

        
        
       
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = GoniometerApp()
#ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
        