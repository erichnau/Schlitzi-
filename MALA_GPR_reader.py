from tkinter import *
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt
import numpy as np
import os
from PIL import ImageTk, Image


class MalaRd7(Frame, object):
    def __init__(self, master):
        super(MalaRd7, self). \
            __init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.tool_frame = Frame(self.master, borderwidth=5, relief='sunken')
        self.tool_frame.pack(ipady=20, fill='x')

        self.button_open = Button(self.tool_frame, text='Open file', command=self.openRD7)
        self.button_open.grid(row=0)

        self.button_exit = Button(self.tool_frame, text='Exit', command=self.exit_viewer)
        self.button_exit.grid(row=0, column=1)

        self.contrast_frame = Frame(self.tool_frame, bg="white", width=150, height=25, highlightbackground="black",
                        highlightthickness=1)
        self.contrast_frame.grid(row=1, column=0)

        self.button_increase_contrast = Button(self.contrast_frame, text='+', command=self.increase_contrast)
        self.button_increase_contrast.grid(row=1, column=2)

        self.button_decrease_contrast = Button(self.contrast_frame, text='-', command=self.decrease_contrast)
        self.button_decrease_contrast.grid(row=1, column=0)

        self.contrast_slider = Scale(self.tool_frame, from_=1, to=100, length=200, orient=HORIZONTAL, command=self.slide_contrast)
        self.contrast_slider.set(1)
        self.contrast_slider.grid(row=1, column=1)

        self.label_contrast = Label(self.contrast_frame, text='Contrast')
        self.label_contrast.grid(row=1, column=1)

        self.img_frame = Frame(self.master)
        self.img_frame.pack()

        self.fig = plt.figure(figsize=(25, 5), dpi=100)
        self.fig.add_subplot()
        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=self.img_frame)
        self.fig_canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, self.img_frame)
        self.toolbar.update()

        self.toolbar.pack(side=tk.TOP)

        self.fig_canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
        self.fig_canvas.mpl_connect("key_press_event", key_press_handler)

    '_______________________________________User interface functions_________________________________________________'

    def openRD7(self):
        self.file = filedialog.askopenfilename(initialdir="/", title="Select MALÅ GPR file", filetypes=[("RD3", "*.rd3"),('RD7', '*.rd7')], parent=root_3)
        if self.file:
            self.filename = str(self.file)[:-4]
            self.max_data = self.readMALA(file_name=self.filename)[2]
            self.min_data = self.readMALA(file_name=self.filename)[3]
            self.show_profile(filename=self.filename, vmax=self.max_data, vmin=self.min_data)

            'new sliders for sinle adjustment of min and max values, maybe needed for arbitrary sections from full trace analysis'
            #self.set_new_slider()
            'new sliders for sinle adjustment of min and max values, maybe needed for arbitrary sections from full trace analysis'

    def show_profile(self, filename, vmax, vmin):
        self.fig.clear()
        self.data = self.readMALA(file_name=self.filename)[0]
        self.fig.add_subplot().imshow(self.data, cmap='gray', vmax=vmax, vmin=vmin)
        self.fig_canvas.draw()
        self.vmin = vmin
        self.vmax = vmax

        'new sliders for sinle adjustment of min and max values, maybe needed for arbitrary sections from full trace analysis'
    #def set_new_slider(self):
        #self.contrast_slider_max = Scale(self.tool_frame, from_=0, to=self.vmax, length=200, orient=HORIZONTAL, command=self.slide_contrast_single)
        #self.contrast_slider_max.set(self.max_data)
        #self.contrast_slider_max.grid(row=2, column=1)

        #self.contrast_slider_min = Scale(self.tool_frame, from_=self.vmin, to=0, length=200, orient=HORIZONTAL, command=self.slide_contrast_single)
        #self.contrast_slider_min.set(self.min_data)
        #self.contrast_slider_min.grid(row=2, column=2)
        'new sliders for sinle adjustment of min and max values, maybe needed for arbitrary sections from full trace analysis'

    def increase_contrast(self):
        vmax_inc = self.vmax / 1.25
        vmin_inc = self.vmin / 1.25
        self.show_profile(self.filename, vmax_inc, vmin_inc)

    def decrease_contrast(self):
        vmax_dec = self.vmax * 1.25
        vmin_dec = self.vmin * 1.25
        self.show_profile(self.filename, vmax_dec, vmin_dec)

    def slide_contrast(self, value):
        if int(value) < 30:
            vmax_slide = int(self.max_data) / (1.1 * int(value))
            vmin_slide = int(self.min_data) / (1.1 * int(value))
        elif int(value) < 60:
            vmax_slide = int(self.max_data) / (1.5 * int(value))
            vmin_slide = int(self.min_data) / (1.5 * int(value))
        else:
            vmax_slide = int(self.max_data) / (2 * int(value))
            vmin_slide = int(self.min_data) / (2 * int(value))

        self.show_profile(self.filename, vmax_slide, vmin_slide)

    def slide_contrast_single(self, value):
        vmax = self.contrast_slider_max.get()
        vmin = self.contrast_slider_min.get()
        self.show_profile(self.filename, vmax, vmin)

    def exit_viewer(self):
        self.master.destroy()



    '_______________________________________User interface functions_________________________________________________'


    '__________________________________________GPR processes_______________________________________________________'

    def readMALA(self, file_name):
        info = self.readGPRhdr(file_name + '.rad')
        try:
            filename = file_name + '.rd3'
            data = np.fromfile(filename, dtype=np.int16)
        except:
            filename = file_name + '.rd7'
            data = np.fromfile(filename, dtype=np.int32)

        nrows = int(len(data) / int(info['SAMPLES']))

        data = (np.asmatrix(data.reshape(nrows, int(info['SAMPLES'])))).transpose()
        vmax = np.max(data)
        vmin = np.min(data)

        return data, info, vmax, vmin

    def readGPRhdr(self, filename):
        info = {}
        with open(filename) as f:
            for line in f:
                strsp = line.split(':')
                info[strsp[0]] = strsp[1].rstrip()
        return info

    '__________________________________________GPR processes_______________________________________________________'

def start_mala_reader():
    global root_3

    os.chdir(str(__file__).rsplit('\\', 1)[0])
    root_3 = tk.Tk()
    root_3.title('MALÅ GPR reader')
    root_3.state('zoomed')
    root_3.iconbitmap('Gjellestad.ico')
    root_3.attributes('-topmost', True)

    app = MalaRd7(root_3)
    app.mainloop()

def start_mala_reader_VEMOP(filename):
    global root_3
    global file_name

    file_name = filename

    os.chdir(str(__file__).rsplit('\\', 1)[0])
    root_3 = tk.Tk()
    root_3.title('MALÅ GPR reader')
    root_3.state('zoomed')
    root_3.iconbitmap('Gjellestad.ico')
    root_3.attributes('-topmost', True)

    app = MalaRd7(root_3)
    app.mainloop()



