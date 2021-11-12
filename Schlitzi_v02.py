import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image
from tkinter import filedialog
import os, glob
import os.path
from tkinter import Frame, Button, Label, Text, Checkbutton, Canvas, Entry, Event, Toplevel, Scrollbar, Tk, INSERT, END, BOTH
from os import path
from win32api import GetSystemMetrics
from matplotlib import pyplot as plt
import xarray as xr
from scipy.spatial import KDTree
from scipy.fft import fft
from fiona import collection
import numpy as np
from math import sqrt
import shapefile
from tkinter.filedialog import asksaveasfile
from datetime import date, datetime
import net_cdf_variables
from net_cdf_variables import find_nth, remove_values_from_list, open_trace
from define_VEMOP_project import start_define_vemop
from shp_tools import nn_from_file, kd_int_to_point_info
#from trace_viewer import start_trace_viewer
from MALA_GPR_reader import start_mala_reader, start_mala_reader_VEMOP
from GPR_proc import DC_shift, timezero_adjust

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')

class MainWindow(Frame, object):
    def __init__(self, master):
        super(MainWindow, self). \
            __init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.mainframe = Frame(self, bg="white", width=600, height=200, highlightbackground="black", highlightthickness=1)
        self.mainframe.grid(row=0, column=0, sticky="NW")
        self.mainframe.grid_propagate(0)
        self.greyscale_frame = Frame(self.mainframe, bg="white", width=150, height=25, highlightbackground="black", highlightthickness=1)
        self.greyscale_frame.grid(row=4, column=1, sticky='w')
        self.progress = Progressbar(self.mainframe, orient='horizontal', length=100, mode='determinate')
        self.progress.grid(row=5, column=0)

        '----------------------------------Buttons mainframe ----------------------------------------'
        self.open_schlizi = Button(self.mainframe, text="Open Schlitzi+", command=self.schlizi_plus, state='disabled')
        self.open_schlizi.grid(row=6, column=0)
        self.select_netCDF = Button(self.mainframe, text="Select NetCDF file", command=self.open_NetCDF)
        self.select_netCDF.grid(row=1, column=0)
        self.convert_nc = Button(self.mainframe, text="Convert from NetCDF", command=self.convert_NetCDF, state='disabled')
        self.convert_nc.grid(row=3, column=1, sticky='w')
        self.locate_DS = Button(self.mainframe, text="Locate depht-slice folder manually", command=self.open_ds_folder, state='disabled')
        self.locate_DS.grid(row=3, column=0, sticky='w')
        self.exit_button = Button(self.mainframe, text="Exit", command=root.destroy)
        self.exit_button.grid(row=6, column=1, sticky='w')
        self.edit_VEMOP_project = Button(self.mainframe, text='Define VEMOP project', command=self.start_vemop)
        self.edit_VEMOP_project.grid(row=7, column=0, sticky='we')
        self.profile_viewer = Button(self.mainframe, text='Profile viewer', command=self.start_mala_viewer)
        self.profile_viewer.grid(row=7, column=1, sticky='w')
        '----------------------------------Buttons mainframe ----------------------------------------'

        '----------------------------------Text and Entry mainframe----------------------------------'
        self.netCDF = Text(self.mainframe, bg='light grey', width=80, height=1)
        self.netCDF.tag_configure('center', justify='center')
        self.netCDF.grid(row=1, column=1)
        self.folder_ds = Text(self.mainframe, bg='light grey', width=80, height=1)
        self.folder_ds.grid(row=2, column=1)
        self.ds_folder = Label(self.mainframe, bg='light grey', width=20, height=1, text="Depth-slice folder:")
        self.ds_folder.grid(row=2, column=0)
        self.greyscalerange = Label(self.mainframe, bg='light grey', width=20, height=1, text="Greyscale range:")
        self.greyscalerange.grid(row=4, column=0)
        '----------------------------------Text and Entry mainframe----------------------------------'

        '----------------------------------Buttons greyscale Frame-----------------------------------'
        self.decrease1 = Button(self.greyscale_frame, text='-', command=self.decrease_lower)
        self.decrease1.grid(row=0, column=0)
        self.decrease2 = Button(self.greyscale_frame, text='-', command=self.decrease_upper)
        self.decrease2.grid(row=0, column=4)
        self.increase1 = Button(self.greyscale_frame, text='+', command=self.increase_lower)
        self.increase1.grid(row=0, column=2)
        self.increase2 = Button(self.greyscale_frame, text='+', command=self.increase_upper)
        self.increase2.grid(row=0, column=6)
        '----------------------------------Buttons greyscale Frame-----------------------------------'

        '----------------------------------Text and label greyscale Frame----------------------------'
        self.lower_value = Text(self.greyscale_frame, bg='light grey', width=3, height=1)
        self.lower_value.tag_configure('center', justify='center')
        self.lower_value.insert(INSERT, '2')
        self.lower_value.tag_add("center", "1.0", "end")
        self.lower_value.grid(row=0, column=1)
        self.upper_value = Text(self.greyscale_frame, bg='light grey', width=3, height=1)
        self.upper_value.tag_configure('center', justify='center')
        self.upper_value.insert(INSERT, '24')
        self.upper_value.tag_add("center", "1.0", "end")
        self.upper_value.grid(row=0, column=5)
        self.l2 = Label(self.greyscale_frame, bg='white', width=3, height=1)
        self.l2.grid(row=0, column=3)
        '----------------------------------Text and label greyscale Frame----------------------------'

        self.mainframe.update()

    def schlizi_plus(self):
        self.toplevel_1_schlizi = Toplevel(relief='raised')
        self.toplevel_1_schlizi.title("Schlitzi+")
        self.toplevel_1_schlizi.geometry("1500x700+0+0")
        self.toplevel_1_schlizi.iconbitmap('c:/01_privat/01_Prog/VEMOP/02_development/Schlizi/Gjellestad.ico')
        self.toplevel_1_schlizi.state('zoomed')
        self.appc = Schlizi_plus(self.toplevel_1_schlizi, self.toplevel_1_schlizi, self.folder_ds, self.netCDF)

    def open_NetCDF(self):
        self.netcdf_file = filedialog.askopenfilename(initialdir="/", title="Select file",
                                       filetypes=[("NetCDF file", "*.nc")], parent=root)
        if self.netcdf_file:
            self.netCDF.delete('1.0', END)
            self.netCDF.insert(INSERT, self.netcdf_file)

        self.check_ds_folder()

    def open_ds_folder(self):
        self.depthsl_folder = filedialog.askdirectory(initialdir="/", title="Select folder", parent=root)
        if self.depthsl_folder:
            self.folder_ds.delete('1.0', END)
            self.folder_ds.insert(INSERT, self.depthsl_folder)

        self.check_ds_folder2()

    def check_ds_folder2(self):
        folder = self.depthsl_folder
        os.chdir(folder)
        if glob.glob('*.jpg'):
            self.folder_ds.configure(bg='light grey')
            self.open_schlizi.configure(state='active')
        else:
            self.folder_ds.delete('1.0', END)
            self.folder_ds.insert(INSERT, 'Folder contains no jpg images')

    def check_ds_folder(self):
        folder = self.netcdf_file.rsplit('/', 1)[0]
        filename = self.netcdf_file.rsplit('/', 1)[1].rsplit('.', 1)[0]
        folder_new = folder + '/05cm'
        file = folder_new + filename + '_000-005.tif'
        folder_new2 = folder + '/depth_slices_' + filename
        depthsl_folder = folder_new2 + '/' + filename + '_000_005.jpg'
        file4 = folder_new2 + '/' + filename + '_0000_0005.jpg'
        folder_new3 = folder + '/NetCDF_img_' + filename
        file3 = folder_new3 + '/' + filename + '_000_005.jpg'
        file5 = folder_new3 + '/' + filename + '_0000_0005.jpg'
        self.folder_ds.configure(bg='light grey')
        self.convert_nc.configure(state='disabled')
        self.locate_DS.configure(state='disabled')
        if path.exists(folder_new):
            if path.exists(file):
                self.folder_ds.delete('1.0', END)
                self.folder_ds.insert(INSERT, folder_new)
                self.open_schlizi.configure(state='active')
            else:
                self.folder_ds.delete('1.0', END)
                self.folder_ds.insert(INSERT, 'No corresponding depth-slice folder found1')
                self.folder_ds.configure(bg='red')
                self.convert_nc.configure(state='active')
                self.locate_DS.configure(state='active')

        elif path.exists(folder_new2):
            if path.exists(depthsl_folder):
                self.folder_ds.delete('1.0', END)
                self.folder_ds.insert(INSERT, folder_new2)
                self.open_schlizi.configure(state='active')

            elif path.exists(file4):
                self.folder_ds.delete('1.0', END)
                self.folder_ds.insert(INSERT, folder_new3)
                self.open_schlizi.configure(state='active')

            else:
                self.folder_ds.delete('1.0', END)
                self.folder_ds.insert(INSERT, 'No coresponding depth-slice folder found2')
                self.folder_ds.configure(bg='red')
                self.convert_nc.configure(state='active')
                self.locate_DS.configure(state='active')

        elif path.exists(folder_new3):
            if path.exists(file3):
                self.folder_ds.delete('1.0', END)
                self.folder_ds.insert(INSERT, folder_new3)
                self.open_schlizi.configure(state='active')

            elif path.exists(file5):
                self.folder_ds.delete('1.0', END)
                self.folder_ds.insert(INSERT, folder_new3)
                self.open_schlizi.configure(state='active')

            else:
                self.folder_ds.delete('1.0', END)
                self.folder_ds.insert(INSERT, 'No corresponding depth-slice folder found3')
                self.folder_ds.configure(bg='red')
                self.convert_nc.configure(state='active')
                self.locate_DS.configure(state='active')

        else:
            self.folder_ds.delete('1.0', END)
            self.folder_ds.insert(INSERT, 'No corresponding depth-slice folder found')
            self.folder_ds.configure(bg='red')
            self.convert_nc.configure(state='active')
            self.locate_DS.configure(state='active')

    def decrease_lower(self):
        newvalue = int(self.lower_value.get('1.0', END)) - 1
        self.lower_value.delete('1.0', END)
        self.lower_value.tag_configure('center', justify='center')
        self.lower_value.insert(INSERT, newvalue)
        self.lower_value.tag_add("center", "1.0", "end")

    def increase_lower(self):
        newvalue = int(self.lower_value.get('1.0', END)) + 1
        self.lower_value.delete('1.0', END)
        self.lower_value.tag_configure('center', justify='center')
        self.lower_value.insert(INSERT, newvalue)
        self.lower_value.tag_add("center", "1.0", "end")

    def decrease_upper(self):
        newvalue = int(self.upper_value.get('1.0', END)) - 1
        self.upper_value.delete('1.0', END)
        self.upper_value.tag_configure('center', justify='center')
        self.upper_value.insert(INSERT, newvalue)
        self.upper_value.tag_add("center", "1.0", "end")

    def increase_upper(self):
        newvalue = int(self.upper_value.get('1.0', END)) + 1
        self.upper_value.delete('1.0', END)
        self.upper_value.tag_configure('center', justify='center')
        self.upper_value.insert(INSERT, newvalue)
        self.upper_value.tag_add("center", "1.0", "end")

    def convert_NetCDF(self):
        self.progress['value'] += 0
        vmin = self.lower_value.get('1.0', END)
        vmax = self.upper_value.get('1.0', END)
        filepath = self.netCDF.get('1.0', END)
        depth_range_top = 0
        nc_noExt = filepath.rsplit('/', 1)[1].rsplit('.', 1)[0]
        zpixels = net_cdf_variables.define_NetCDF_variables(filepath)[2]

        for i in range(depth_range_top, zpixels):
            net_cdf_variables.convert_NetCDF(vmin, vmax, filepath, i)

            root.update_idletasks()
            prog = 100/zpixels
            self.progress['value'] += prog

        self.folder_ds.delete('1.0', END)
        self.folder_ds.insert(INSERT, filepath.rsplit('/', 1)[0] + '/NetCDF_img_%s' % nc_noExt)
        self.folder_ds.configure(bg='light grey')
        self.open_schlizi.configure(state='active')

    def start_vemop(self):
        start_define_vemop()

    def start_mala_viewer(self):
        start_mala_reader()

class Schlizi_plus(object):
    def __init__(self, master, toplevel_1_schlizi, folder_ds, netCDF):
        self.master = master
        self.toplevel_1_schlizi = toplevel_1_schlizi
        self.folder_ds = folder_ds
        self.netCDF = netCDF
        self.netcdf_variables(netcdf_dataset=self.netCDF.get('1.0', END))
        self.main_window()
        self.test(Button)

    def main_window(self):

        height_frame = (GetSystemMetrics(1)/100)*90
        width_frame = GetSystemMetrics(0)/2

        self.frame = Frame(self.toplevel_1_schlizi, bg="grey", width=width_frame, height=height_frame, highlightbackground="black",
                        highlightthickness=3)
        self.frame.place(x=5, y=5)

        self.frame2 = Frame(self.toplevel_1_schlizi, bg="pink", width=200, height=600, highlightbackground="black",
                           highlightthickness=1)
        self.frame2.place(x=width_frame+28, y=5)

        """FRame 3 _______________________________________________________________________________"""


        """FRame 3 _______________________________________________________________________________"""

        """FRame 4 _______________________________________________________________________________"""



        """FRame 4 _______________________________________________________________________________"""

        """FRame 5 _______________________________________________________________________________"""
        """FRame 5 _______________________________________________________________________________"""


        "Buttons -----------------------------------------------------------------------------------------"
        "Buttons -----------------------------------------------------------------------------------------"
        self.plot = Button(self.frame2, text='Trace', command=self.plot_trace)
        self.plot.grid(row=13, sticky='sw')


        self.plotX = Button(self.frame2, text="Plot section X", command=self.plot_profile_X)
        self.plotX.grid(row=14, column=0, sticky='sw')


        self.plotY = Button(self.frame2, text="Plot section Y", command=self.plot_profile_Y)
        self.plotY.grid(row=15, column=0, sticky='sw')

        self.arbitrary = Button(self.frame2, text="Plot arbitrary section", command=self.plot_arbitrary, state='disabled')
        self.arbitrary.grid(row=16, column=0, sticky='sw')

        self.save_shp = Button(self.frame2, text='Export section to shp', command=self.save_profile_shp, state='disabled')
        self.save_shp.grid(row=17, column=0, sticky='sw')

        self.exit = Button(self.frame2, text='Exit', command=self.exit_schlitzi)
        self.exit.grid(row=18, column=0, sticky='sw')

        self.open_vemop = Button(self.frame2, text='Open VEMOP', command=self.open_vemop_project)
        self.open_vemop.grid(row=19, column=0, sticky='sw')

        "Buttons -----------------------------------------------------------------------------------------"
        "Buttons -----------------------------------------------------------------------------------------"

        "Text fields -----------------------------------------------------------------------------------------"
        "Text fields -----------------------------------------------------------------------------------------"
        self.text1 = Text(self.frame2, bg='light grey', width=15, height=1)
        self.text1.tag_configure('center', justify='center')
        self.text1.grid(row=0, column=0)
        self.text1.insert(INSERT, self.list_depthslices(self.folder_ds.get('1.0', END).strip("\n"))[0])

        self.texfolder_ds = Text(self.frame2, bg='light grey', width=15, height=1)
        self.texfolder_ds.tag_configure('center', justify='center')
        self.texfolder_ds.grid(row=2, column=0, sticky='w')
        self.text3 = Text(self.frame2, bg='light grey', width=15, height=1)
        self.text3.tag_configure('center', justify='center')
        self.text3.grid(row=3, column=0, sticky='w')

        self.text4 = Text(self.frame2, bg='light grey', width=15, height=1)
        self.text4.tag_configure('center', justify='center')
        self.text4.grid(row=4, column=0, sticky='w')
        self.text5 = Text(self.frame2, bg='light grey', width=15, height=1)
        self.text5.tag_configure('center', justify='center')
        self.text5.grid(row=5, column=0, sticky='w')

        self.text6 = Text(self.frame2, bg='light grey', width=15, height=1)
        self.text6.tag_configure('center', justify='center')
        self.text6.grid(row=6, column=0, sticky='w')
        self.text7 = Text(self.frame2, bg='light grey', width=15, height=1)
        self.text7.tag_configure('center', justify='center')
        self.text7.grid(row=7, column=0, sticky='w')

        self.text8 = Text(self.frame2, bg='light grey', width=15, height=1)
        self.text8.tag_configure('center', justify='center')
        self.text8.grid(row=8, column=0, sticky='w')
        self.text9 = Text(self.frame2, bg='light grey', width=15, height=1)
        self.text9.tag_configure('center', justify='center')
        self.text9.grid(row=9, column=0, sticky='w')

        self.text10 = Text(self.frame2, bg='light grey', width=15, height=1)
        self.text10.tag_configure('center', justify='center')
        self.text10.grid(row=10, column=0, sticky='w')

        self.text11 = Text(self.frame2, bg='light grey', width=15, height=1)
        self.text11.tag_configure('center', justify='center')
        self.text11.grid(row=11, column=0, sticky='w')
        self.text11.insert(INSERT, '1.0')

        self.text12 = Text(self.frame2, bg='light grey', width=15, height=1)
        self.text12.tag_configure('center', justify='center')
        self.text12.grid(row=12, column=0, sticky='w')
        "Text fields -----------------------------------------------------------------------------------------"
        "Text fields -----------------------------------------------------------------------------------------"


        input = self.text1.get('1.0', 'end-1c')
        self.image = Image.open(input)

        vbar = Scrollbar(self.frame, orient='vertical')
        hbar = Scrollbar(self.frame, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='ew')

        self.canvas = Canvas(self.frame, bg='white', highlightthickness=0, width=width_frame, height=height_frame,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.canvas.grid(row=0, column=0, sticky='nswe')

        self.canvas.grid_propagate()
        self.canvas.addtag_all('test')
        vbar.configure(command=self.canvas.yview)  # bind scrollbars to the canvas
        hbar.configure(command=self.canvas.xview)
        # Make the canvas expandable
        #self.master.rowconfigure(0, weight=1)
        #self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>', self.move_to)
        self.canvas.bind("<Configure>", self.move_from)
        #self.canvas.bind('<Button 1>', self.callback)
        self.canvas.bind("<Button-3>", self.printcoords)
        self.canvas.bind("<ButtonRelease-3>", self.printcoords2)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        #self.canvas.bind('<Button-5>', self.wheel)  # only with Linux, wheel scroll down
        #self.canvas.bind('<Button-4>', self.wheel)  # only with Linux, wheel scroll up
        # Show image and plot some random test rectangles on the canvas
        self.imscale = 1.0
        self.imageid = None
        self.delta = 0.75
        width, height = self.image.size
        minsize, maxsize = 5, 20

        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.create_single_interface()
        self.list_depthslices(depthslice_folder=self.folder_ds.get('1.0', END).strip("\n"))

    def create_single_interface(self):
        height_frame = (GetSystemMetrics(1) / 100) * 90
        width_frame = GetSystemMetrics(0) / 2

        self.frame3 = Frame(self.toplevel_1_schlizi, bg="blue", width=100, height=600, highlightbackground="black",
                            highlightthickness=1)

        self.frame3.place(x=width_frame + 234, y=5)

        self.open_mira = Button(self.frame3, text='Select MIRA project', command=self.open_mira)
        self.open_mira.grid(row=0, sticky='nw')

        self.open_shp = Button(self.frame3, text='Selecte shpfile', command=self.open_shp)
        self.open_shp.grid(row=1, sticky='nw')

        self.get_nearest = Button(self.frame3, text='Get closest trace', command=self.nearest_features)
        self.get_nearest.grid(row=2, sticky='nw')

        self.get_nearest5 = Button(self.frame3, text='Get closest 5 traces', command=self.nearest_features_5)
        self.get_nearest5.grid(row=3, sticky='nw')

        self.plot_nearest = Button(self.frame3, text='Plot closest trace', command=self.read_mala_single)
        self.plot_nearest.grid(row=4, sticky='nw')

        self.save_traces = Button(self.frame3, text='Save traces', command=self.save_mala_multiple)
        self.save_traces.grid(row=5, sticky='nw')

        self.plot_nearest5 = Button(self.frame3, text='Plot 5 traces', command=self.read_mala_multiple)
        self.plot_nearest5.grid(row=6, sticky='nw')

        self.DC_adjust = Button(self.frame3, text='DC shift', command=self.DC_shift)
        self.DC_adjust.grid(row=7, sticky='nw')

        self.timezero_adjust = Button(self.frame3, text='Timezero adjustment', command=self.timezero_adjustment)
        self.timezero_adjust.grid(row=8, sticky='nw')

        self.frame4 = Frame(self.toplevel_1_schlizi, bg="green", width=200, height=600, highlightbackground="black",
                           highlightthickness=1)

        self.frame4.place(x=width_frame+355, y=5)

        self.project = Text(self.frame4, bg='light grey', width=50, height=1)
        self.project.tag_configure('center', justify='center')
        self.project.grid(row=0, column=1)

        self.filename = Text(self.frame4, bg='light grey', width=50, height=1)
        self.filename.tag_configure('center', justify='center')
        self.filename.grid(row=1, column=1)

        self.nearest_Text = Text(self.frame4, bg='light grey', width=50, height=5)
        self.nearest_Text.tag_configure('center', justify='center')
        self.nearest_Text.grid(row=2, column=1)

    def list_depthslices(self, depthslice_folder):
        self.lst = tk.Listbox(self.frame2, height=20)
        self.lst.grid(row=1, column=0, sticky='w')
        os.chdir(depthslice_folder)
        self.namelist = [i for i in glob.glob ("*jpg")]
        for fname in self.namelist:
            self.lst.insert(tk.END, fname)
        self.lst.bind("<<ListboxSelect>>", self.test)

        return self.namelist

    def destroy_single_interface(self):
        self.frame3.destroy()
        self.frame4.destroy()

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def printcoords(self, event):

        self.centerx = float(self.x_coor) + (int(self.xpixels)/2)*self.pixelsize
        self.centery = float(self.y_coor) + (int(self.ypixels)/2)*self.pixelsize

        try:
            if self.ivar_viewer.get() == 1 or self.ivar_analysis.get() == 1:
                scale_new = float(self.text11.get('1.0', END))
                list_on = []

                for item in self.checkbutton_list:
                    list_on.append(item.get())

                list_on = remove_values_from_list(list_on, 'off')

                self.x_off, self.y_off = round((self.offsets[int(list_on[0]) - 1][0] / self.pixelsize) * scale_new), round((self.offsets[int(list_on[0]) - 1][1] / self.pixelsize) * scale_new)


            else:
                self.x_off, self.y_off = 0, 0
        except AttributeError:
            self.x_off, self.y_off = 0, 0

        self.can_x = self.canvas.canvasx(event.x)
        self.can_y = self.canvas.canvasy(event.y)

        self.imgx_can = round(self.centerx + (((self.can_x - self.x_off)*self.pixelsize)/self.imscale), 3)
        self.imgy_can = round(self.centery - (((self.can_y - self.y_off)*self.pixelsize)/self.imscale), 3)
        self.texfolder_ds.delete('1.0', END)
        self.texfolder_ds.insert(INSERT, self.imgx_can)
        self.text3.delete('1.0', END)
        self.text3.insert(INSERT, self.imgy_can)

        try:
            self.point1
            if self.point1:
                self.canvas.delete(self.point1)
                self.canvas.delete(self.section)
                self.text4.delete('1.0', 'end')
                self.text5.delete('1.0', 'end')
                self.text8.delete('1.0', 'end')
                self.text9.delete('1.0', 'end')
                self.text10.delete('1.0', 'end')

        except AttributeError:
            'do nothing'

        try:
            if self.point:
                self.canvas.delete(self.point)
                self.point = self.canvas.create_oval(self.can_x + 2.5, self.can_y + 2.5, self.can_x - 2.5, self.can_y - 2.5, fill='red')
        except AttributeError:
            self.point = self.canvas.create_oval(self.can_x + 2.5, self.can_y + 2.5, self.can_x - 2.5, self.can_y - 2.5, fill='red')

        self.text6.delete('1.0', END)
        self.text6.insert(INSERT, self.canvas.coords(self.point)[0])
        self.text7.delete('1.0', END)
        self.text7.insert(INSERT, self.canvas.coords(self.point)[1])

    def printcoords2(self, event):

        self.centerx = float(self.x_coor) + (int(self.xpixels)/2)*self.pixelsize
        self.centery = float(self.y_coor) + (int(self.ypixels)/2)*self.pixelsize

        self.can_x1 = self.canvas.canvasx(event.x)
        self.can_y1 = self.canvas.canvasy(event.y)

        try:
            if self.ivar_viewer.get() == 1 or self.ivar_analysis.get() == 1:
                scale_new = float(self.text11.get('1.0', END))
                list_on = []

                for item in self.checkbutton_list:
                    list_on.append(item.get())

                list_on = remove_values_from_list(list_on, 'off')

                self.x_off, self.y_off = round(
                    (self.offsets[int(list_on[0]) - 1][0] / self.pixelsize) * scale_new), round(
                    (self.offsets[int(list_on[0]) - 1][1] / self.pixelsize) * scale_new)
                self.x_off_switch, self.y_off_switch = round(
                    (self.offsets[int(list_on[0]) - 1][0] / self.pixelsize)), round(
                    (self.offsets[int(list_on[0]) - 1][1] / self.pixelsize))

            else:
                self.x_off, self.y_off = 0, 0
        except AttributeError:
            self.x_off, self.y_off = 0, 0

        self.imgx_can1 = round(self.centerx + (((self.can_x1 - self.x_off)*self.pixelsize)/self.imscale), 3)
        self.imgy_can1 = round(self.centery - (((self.can_y1 - self.y_off)*self.pixelsize)/self.imscale), 3)

        self.dist = round(sqrt(((float(self.text3.get('1.0', 'end')) - self.imgy_can1)**2)+((float(self.texfolder_ds.get('1.0', 'end')) - self.imgx_can1)**2)), 2)


        self.text10.delete('1.0', 'end')
        self.text10.insert(INSERT, str(self.dist) + ' m')

        if self.dist == 0:
            self.save_shp['state'] = 'disabled'
            self.arbitrary['state'] = 'disabled'
        else:
            self.save_shp["state"] = "normal"
            self.arbitrary['state'] = 'normal'

        if self.dist > 0.25:
            self.text4.delete('1.0', END)
            self.text4.insert(INSERT, self.imgx_can1)
            self.text5.delete('1.0', END)
            self.text5.insert(INSERT, self.imgy_can1)
            try:
                self.point1
                if self.point1:
                    self.canvas.delete(self.point1)
                    self.point1 = self.canvas.create_oval(self.can_x1 + 2.5, self.can_y1 + 2.5, self.can_x1 - 2.5, self.can_y1 - 2.5, fill='green')
            except AttributeError:
                self.point1 = self.canvas.create_oval(self.can_x1 + 2.5, self.can_y1 + 2.5, self.can_x1 - 2.5, self.can_y1 - 2.5, fill='green')

            try:
                self.section
                if self.section:
                    self.canvas.delete(self.section)
                    self.section = self.canvas.create_line(self.can_x, self.can_y, self.can_x1, self.can_y1)
            except AttributeError:
                self.section = self.canvas.create_line(self.can_x, self.can_y, self.can_x1, self.can_y1)

            self.text8.delete('1.0', END)
            self.text8.insert(INSERT, self.canvas.coords(self.point1)[0])
            self.text9.delete('1.0', END)
            self.text9.insert(INSERT, self.canvas.coords(self.point1)[1])

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def wheel(self, event):
        scale = 1.0

        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            scale        *= self.delta
            self.imscale *= self.delta

        if event.num == 4 or event.delta == 120:
            scale        /= self.delta
            self.imscale /= self.delta

        # Rescale all canvas objects
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        #print(x, y)
        self.canvas.scale('all', x, y, scale, scale)
        scale_orig = float(self.text11.get('1.0', END))
        self.scale_new = scale * scale_orig
        self.text11.delete('1.0', END)
        self.text11.insert(INSERT, self.scale_new)

        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        "rescale point object drawn by get coordinates"

        self.redraw_zoom()
        'do nothing'

        "rescale point object drawn by get coordinates"

    def show_image(self):
        input = self.text1.get('1.0', 'end-1c')
        self.image = Image.open(input)

        x_off, y_off = 0, 0
        scale_new = float(self.text11.get('1.0', END))

        try :
            if self.ivar_viewer.get() == 1 or self.ivar_analysis.get() == 1:
                list_on = []

                for item in self.checkbutton_list:
                    list_on.append(item.get())

                list_on = remove_values_from_list(list_on, 'off')

                x_off, y_off = round((self.offsets[int(list_on[0])-1][0] / self.pixelsize) * scale_new), round((self.offsets[int(list_on[0])-1][1] / self.pixelsize) * scale_new)
        except:
            'do nothing'

        if self.imageid:
            self.canvas.delete(self.imageid)
            self.imageid = None
            self.canvas.imagetk = None  # delete previous image from the canvas
        width, height = self.image.size
        new_size = int(self.imscale * width), int(self.imscale * height)

        '''for VEMOP project to get the same image size in viewer - should be removed if possible - rather use data with the same resolution'''
        #if self.pixelsize == 0.1:
        #    new_size = int(self.imscale * width)*2, int(self.imscale * height)*2
        '''for VEMOP project to get the same image size in viewer - should be removed if possible - rather use data with the same resolution'''

        imagetk = ImageTk.PhotoImage(self.image.resize(new_size))
        # Use self.text object to set proper coordinates
        self.imageid = self.canvas.create_image(x_off, y_off, image=imagetk) #maybe add anchor here
        self.canvas.lower(self.imageid)  # set it into background
        self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    def redraw_zoom(self):
        try:
            if self.ivar_viewer.get() == 1 or self.ivar_analysis.get() == 1:
                print('here')
                list_on = []

                for item in self.checkbutton_list:
                    list_on.append(item.get())

                list_on = remove_values_from_list(list_on, 'off')

                if self.last != int(list_on[0]) - 1:
                    x_off, y_off = self.x_off_switch, self.y_off_switch
                else:
                    x_off, y_off = self.x_off_switch, self.y_off_switch

            else:
                x_off, y_off = 0, 0
                print('fal')
        except:
            x_off, y_off = 0, 0
            print('ssse')

        try:
            canXpoint = (((float(self.texfolder_ds.get('1.0', 'end')) - self.centerx) * self.imscale) / self.pixelsize)
            canXXpoint = round(canXpoint, 0) + (x_off * self.imscale)

            canYpoint = (((float(self.text3.get('1.0', 'end')) - self.centery) * self.imscale) / self.pixelsize)
            canYYpoint = round(-canYpoint, 0) + (y_off * self.imscale)
            self.canvas.coords(self.point, canXXpoint - 2.5, canYYpoint - 2.5, canXXpoint + 2.5, canYYpoint + 2.5)

            canXpoint1 = ((float(self.text4.get('1.0', 'end')) - self.centerx) * self.imscale) / self.pixelsize
            canXXpoint1 = round(canXpoint1, 0)  + (x_off * self.imscale)
            canYpoint1 = ((float(self.text5.get('1.0', 'end')) - self.centery) * self.imscale) / self.pixelsize
            canYYpoint1 = round(-canYpoint1, 0)  + (y_off * self.imscale)
            self.canvas.coords(self.point1, canXXpoint1 - 2.5, canYYpoint1 - 2.5, canXXpoint1 + 2.5, canYYpoint1 + 2.5)

            self.canvas.coords(self.section, canXXpoint, canYYpoint, canXXpoint1, canYYpoint1)
        except ValueError:
            'do nothing'

    def redraw_switch(self):
        try:
            if self.ivar_viewer.get() == 1 or self.ivar_analysis.get() == 1:
                scale_new = float(self.text11.get('1.0', END))
                list_on = []

                for item in self.checkbutton_list:
                    list_on.append(item.get())

                list_on = remove_values_from_list(list_on, 'off')

                if self.last != int(list_on[0]) - 1:
                    x_off, y_off = self.x_off_switch, self.y_off_switch
                elif self.last == int(list_on[0]) - 1:
                    x_off, y_off = self.x_off_switch, self.y_off_switch

            else:
                x_off, y_off = 0, 0

        except:
            x_off, y_off = 0, 0

        try:
            canXpoint = ((float(self.texfolder_ds.get('1.0', 'end')) - self.centerx) * self.imscale) / self.pixelsize
            canXXpoint = round(canXpoint, 0) + (x_off * self.imscale)
            canYpoint = ((float(self.text3.get('1.0', 'end')) - self.centery) * self.imscale) / self.pixelsize
            canYYpoint = round(-canYpoint, 0) + (y_off * self.imscale)
            self.canvas.coords(self.point, canXXpoint - 2.5, canYYpoint - 2.5, canXXpoint + 2.5, canYYpoint + 2.5)

            canXpoint1 = ((float(self.text4.get('1.0', 'end')) - self.centerx) * self.imscale) / self.pixelsize
            canXXpoint1 = round(canXpoint1, 0) + (x_off * self.imscale)
            canYpoint1 = ((float(self.text5.get('1.0', 'end')) - self.centery) * self.imscale) / self.pixelsize
            canYYpoint1 = round(-canYpoint1, 0) + (y_off * self.imscale)
            self.canvas.coords(self.point1, canXXpoint1 - 2.5, canYYpoint1 - 2.5, canXXpoint1 + 2.5, canYYpoint1 + 2.5)

            self.canvas.coords(self.section, canXXpoint, canYYpoint, canXXpoint1, canYYpoint1)
        except ValueError:
            'do nothing'

    def onSubmifolder_ds(self):
        self.t3.delete(1.0, END)
        self.t3.config(bg="red")
        self.folder_ds.config(bg="green")
        self.folder_ds.insert(INSERT, self.c2.selection_get())

    def test(self, event):

        if self.lst.curselection() != ():
            fname = self.lst.get(self.lst.curselection())
            self.text1.delete('1.0', END)
            self.text1.insert(INSERT, fname)
            self.image = ImageTk.PhotoImage(Image.open(fname))
            self.show_image()

    def plot_trace(self):
        file = self.NETCDF_dataset.strip('\n')
        dset = xr.open_dataset(file)

        inputx = float(self.texfolder_ds.get('1.0', 'end'))
        inputy = float(self.text3.get('1.0', 'end'))
        loc = dset.sel(x=inputx, y=inputy, method='nearest')

        x = loc.variables['z']
        y = loc.variables['gpr']
        plt.plot(y, x)
        plt.show()

    def plot_profile_X(self):
        file2 = self.NETCDF_dataset.strip('\n')
        dsefolder_ds = xr.open_dataset(file2)
        gpr2 = dsefolder_ds.gpr

        x_section_temp = (float(self.text3.get('1.0', 'end')) - float(self.y_coor)) / self.pixelsize
        x_section = int(round(x_section_temp, 0))

        plt.imshow(gpr2.isel(y=x_section), cmap='Greys', vmin=4, vmax=24,
                   interpolation='bilinear')
        plt.title('TEST')
        plt.show()

    def plot_profile_Y(self):
        file2 = self.NETCDF_dataset.strip('\n')
        dsefolder_ds = xr.open_dataset(file2)
        gpr2 = dsefolder_ds.gpr

        y_section_temp = (float(self.texfolder_ds.get('1.0', 'end')) - float(self.x_coor)) / self.pixelsize
        y_section = int(round(y_section_temp, 0))

        plt.imshow(gpr2.isel(x=y_section), cmap='Greys', vmin=4, vmax=24,
                   interpolation='bilinear')
        plt.title('TEST')
        plt.show()

    def plot_arbitrary(self):
        NetCDF_GPR = self.NETCDF_dataset.strip('\n')
        dset = xr.open_dataset(NetCDF_GPR)
        gpr = dset.gpr

        startY, startX = float(self.text3.get('1.0', 'end')), float(self.texfolder_ds.get('1.0', 'end'))
        endY, endX = float(self.text5.get('1.0', 'end')), float(self.text4.get('1.0', 'end'))
        dist = sqrt(((startY - endY) ** 2) + ((startX - endX) ** 2))
        n = round(dist / 0.05)
        x = xr.DataArray(np.linspace(startX, endX, n), dims='along_course')
        y = xr.DataArray(np.linspace(startY, endY, n), dims='along_course')
        section = gpr.interp(x=x, y=y, method='linear')
        plt.imshow(section, cmap='Greys', vmin=4, vmax=24, interpolation='bilinear')
        plt.show()

    def save_profile_shp(self):
        data = [('Shapefile', '*.shp')]
        file = asksaveasfile(filetypes=data, defaultextension=data, parent=self.toplevel_1_schlizi)
        if file:
            section =[float(self.texfolder_ds.get('1.0', 'end')), float(self.text3.get('1.0', 'end'))], [float(self.text4.get('1.0', 'end')), float(self.text5.get('1.0', 'end'))]
            w = shapefile.Writer(shapefile.POLYLINE)
            w.line(parts=[section])
            w.field('Id', 'C')
            w.record('0')
            w.save(file.name)
        else:
            'do nothing'

    def open_shp(self):
        self.file = filedialog.askopenfilename(initialdir="/", title="Select file",
                                       filetypes=[("shapefile", "*.shp")], parent=self.toplevel_1_schlizi)
        if self.file:
            self.filename.delete('1.0', END)
            self.filename.insert(INSERT, self.file)

    def open_mira(self):
        self.file = filedialog.askopenfilename(initialdir="/", title="Select file",
                                       filetypes=[("mira project file", "*.mira")], parent=self.toplevel_1_schlizi)
        if self.file:
            self.project.delete('1.0', END)
            self.project.insert(INSERT, self.file)
            print(self.file)

    def nearest_features(self):
        self.nearest_Text.delete('1.0', END)
        datasource = str(self.filename.get('1.0', 'end'))[:-1]
        x = float(self.texfolder_ds.get('1.0', 'end'))
        y = float(self.text3.get('1.0', 'end'))
        n = 1

        with collection(datasource, "r") as source:
            features = list(source)

        pts = np.asarray([feat['geometry']['coordinates'] for feat in features])
        pts2D = np.delete(pts, np.s_[::3], axis=1)

        tree = KDTree(pts2D)

        querypoint = np.asarray([[x, y]])
        result = tree.query(querypoint, n)

        if n == 1:
            nearest_features = [features[result[1][0]], ]
            distances = list(result[0])
        else:
            nearest_features = [features[x] for x in result[1][0]]
            distances = list(result[0][0])

        def strip_nearest(p):
            nearest1 = nearest_features[p]
            nearesfolder_ds = nearest1['properties']
            nearest3 = str(nearesfolder_ds)
            nearest4 = nearest3.replace('OrderedDict(', '').replace('[', '').replace(']', '').replace('(', '').replace(
                ')', '')
            nearest5 = tuple(nearest4.split(","))
            self.nearest_Text.insert(INSERT, 'Line:' + nearest5[1] + ', Channel:' + nearest5[3] + ', Trace:' + nearest5[
                5])

        for num, feature in enumerate(nearest_features):
            strip_nearest(p=num)
            dist = str(round(distances[num], 3))
            self.nearest_Text.insert(INSERT, ', Distance: ' + dist +'m\n')

    def nearest_features_5(self):
        self.nearest_Text.delete('1.0', END)
        datasource = str(self.filename.get('1.0', 'end'))[:-1]
        x = float(self.texfolder_ds.get('1.0', 'end'))
        y = float(self.text3.get('1.0', 'end'))
        n = 5

        with collection(datasource, "r") as source:
            features = list(source)

        coords = np.asarray([feat['geometry']['coordinates'] for feat in features])
        pts2D = np.delete(coords, np.s_[2::3], axis=1)

        tree = KDTree(pts2D)

        querypoint = np.asarray([[x, y]])
        result = tree.query(querypoint, n)

        if n == 1:
            nearest_features = [features[result[1][0]], ]
            distances = list(result[0])
        else:
            nearest_features = [features[x] for x in result[1][0]]
            distances = list(result[0][0])

        def strip_nearest(p):
            nearest1 = nearest_features[p]
            nearesfolder_ds = nearest1['properties']
            nearest3 = str(nearesfolder_ds)
            nearest4 = nearest3.replace('OrderedDict(', '').replace('[', '').replace(']', '').replace('(', '').replace(
                ')', '')
            nearest5 = tuple(nearest4.split(","))
            self.nearest_Text.insert(INSERT, 'Line:' + nearest5[1] + ', Channel:' + nearest5[3] + ', Trace:' + nearest5[
                5])

        for num, feature in enumerate(nearest_features):
            strip_nearest(p=num)
            dist = str(round(distances[num], 3))
            self.nearest_Text.insert(INSERT, ', Distance: ' + dist +'m\n')

    def read_mala_single(self):
        def readGPRhdr():
            info = {}
            with open(file_name + '.rad') as f:
                for line in f:
                    strsp = line.split(':')
                    info[strsp[0]] = strsp[1].rstrip()
            return info

        mira = self.project.get('1.0', 'end') #C:/06_forskningsprosjekter/VEMOP/data/sites/Heimdal/GPR/C_14012021/C_14012021.mira'


        #file =  #open('c:/000_VEMOP_convert/nc\GPR\selection.txt')
        file_read = self.nearest_Text.get('1.0', 'end')
        lin = file_read.split()

        line = int(lin[1][:-1])
        channel = int(lin[3][:-1])
        if len(str(channel)) < 2:
            channel = 'A00' + str(channel)
        else:
            channel = 'A0' + str(channel)

        if len(str(line)) < 3:
            line = '0' * (3 - len(str(line))) + str(line)

        trace = int(lin[5][:-1])

        file_name = mira[:-6] + '_' + line + '_' + channel

        info = readGPRhdr()
        filename = file_name + '.rd3'
        data = np.fromfile(filename, dtype=np.int16)
        nrows = int(len(data) / int(info['SAMPLES']))
        data = (np.asmatrix(data.reshape(nrows, int(info['SAMPLES'])))).transpose()

        plt.subplot(1, 2, 1)
        plt.imshow(data, cmap='gray', vmin=-1500, vmax=1500)

        plt.subplot(1, 2, 2)
        x = data[:, trace]
        y = range(512, 0, -1)
        plt.plot(x, y)

        plt.show()

    def read_mala_multiple(self):
        def readGPRhdr():
            info = {}
            with open(file_name + '.rad') as f:
                for line in f:
                    strsp = line.split(':')
                    info[strsp[0]] = strsp[1].rstrip()
            return info

        mira = self.project.get('1.0', 'end')

        file_read = self.nearest_Text.get('1.0', 'end')
        lines = file_read.splitlines()
        output = []

        for num, i in enumerate(lines):
            try:
                lin = lines[num].split()
                line = int(lin[1][:-1])
                channel = int(lin[3][:-1])
                if len(str(channel)) < 2:
                    channel = 'A00' + str(channel)
                else:
                    channel = 'A0' + str(channel)

                if len(str(line)) < 3:
                    line = '0' * (3 - len(str(line))) + str(line)

                trace = int(lin[5][:-1])

                file_name = mira[:-6] + '_' + line + '_' + channel
                output.append(file_name)
                output.append(trace)
            except IndexError:
                print('test')

        info = readGPRhdr()
        filename1 = output[0] + '.rd3'
        data1 = np.fromfile(filename1, dtype=np.int16)
        nrows1 = int(len(data1) / int(info['SAMPLES']))
        data1 = (np.asmatrix(data1.reshape(nrows1, int(info['SAMPLES'])))).transpose()

        filename2 = output[2] + '.rd3'
        data2 = np.fromfile(filename2, dtype=np.int16)
        nrows2 = int(len(data2) / int(info['SAMPLES']))
        data2 = (np.asmatrix(data2.reshape(nrows2, int(info['SAMPLES'])))).transpose()

        filename3 = output[4] + '.rd3'
        data3 = np.fromfile(filename3, dtype=np.int16)
        nrows3 = int(len(data3) / int(info['SAMPLES']))
        data3 = (np.asmatrix(data3.reshape(nrows3, int(info['SAMPLES'])))).transpose()

        filename4 = output[6] + '.rd3'
        data4 = np.fromfile(filename4, dtype=np.int16)
        nrows4 = int(len(data4) / int(info['SAMPLES']))
        data4 = (np.asmatrix(data4.reshape(nrows4, int(info['SAMPLES'])))).transpose()

        filename5 = output[8] + '.rd3'
        data5 = np.fromfile(filename5, dtype=np.int16)
        nrows5 = int(len(data5) / int(info['SAMPLES']))
        data5 = (np.asmatrix(data5.reshape(nrows5, int(info['SAMPLES'])))).transpose()

        plt.subplot(1, 6, 1)
        x1 = data1[:, output[1]]
        y1 = range(512, 0, -1)
        plt.plot(x1, y1)

        plt.subplot(1, 6, 2)
        x2 = data2[:, output[3]]
        y2 = range(512, 0, -1)
        plt.plot(x2, y2)

        plt.subplot(1, 6, 3)
        x3 = data3[:, output[5]]
        y3 = range(512, 0, -1)
        plt.plot(x3, y3)

        plt.subplot(1, 6, 4)
        x4 = data4[:, output[7]]
        y4 = range(512, 0, -1)
        plt.plot(x4, y4)

        plt.subplot(1, 6, 5)
        x5 = data5[:, output[9]]
        y5 = range(512, 0, -1)
        plt.plot(x5, y5)

        plt.subplot(1, 6, 6)
        plt.plot(x1, y2)
        plt.plot(x2, y2)
        plt.plot(x3, y3)
        plt.plot(x4, y4)
        plt.plot(x5, y5)

        plt.show()

    def save_mala_multiple(self):
        data = [('GPR traces numpy', '*.npy')]
        self.file = asksaveasfile(filetypes=data, defaultextension=data, parent=self.toplevel_1_schlizi)

        if self.file:

            def readGPRhdr():
                info = {}
                with open(file_name + '.rad') as f:
                    for line in f:
                        strsp = line.split(':')
                        info[strsp[0]] = strsp[1].rstrip()
                return info

            mira = self.project.get('1.0', 'end')

            file_read = self.nearest_Text.get('1.0', 'end')
            lines = file_read.splitlines()
            output = []

            for num, i in enumerate(lines):
                try:
                    lin = lines[num].split()
                    line = int(lin[1][:-1])
                    channel = int(lin[3][:-1])
                    if len(str(channel)) < 2:
                        channel = 'A00' + str(channel)
                    else:
                        channel = 'A0' + str(channel)

                    if len(str(line)) < 3:
                        line = '0' * (3 - len(str(line))) + str(line)

                    trace = int(lin[5][:-1])

                    file_name = mira[:-6] + '_' + line + '_' + channel
                    output.append(file_name)
                    output.append(trace)
                except IndexError:
                    print('test')

            info = readGPRhdr()
            filename1 = output[0] + '.rd3'
            data1 = np.fromfile(filename1, dtype=np.int16)
            nrows1 = int(len(data1) / int(info['SAMPLES']))
            data1 = (np.asmatrix(data1.reshape(nrows1, int(info['SAMPLES'])))).transpose()

            filename2 = output[2] + '.rd3'
            data2 = np.fromfile(filename2, dtype=np.int16)
            nrows2 = int(len(data2) / int(info['SAMPLES']))
            data2 = (np.asmatrix(data2.reshape(nrows2, int(info['SAMPLES'])))).transpose()

            filename3 = output[4] + '.rd3'
            data3 = np.fromfile(filename3, dtype=np.int16)
            nrows3 = int(len(data3) / int(info['SAMPLES']))
            data3 = (np.asmatrix(data3.reshape(nrows3, int(info['SAMPLES'])))).transpose()

            filename4 = output[6] + '.rd3'
            data4 = np.fromfile(filename4, dtype=np.int16)
            nrows4 = int(len(data4) / int(info['SAMPLES']))
            data4 = (np.asmatrix(data4.reshape(nrows4, int(info['SAMPLES'])))).transpose()

            filename5 = output[8] + '.rd3'
            data5 = np.fromfile(filename5, dtype=np.int16)
            nrows5 = int(len(data5) / int(info['SAMPLES']))
            data5 = (np.asmatrix(data5.reshape(nrows5, int(info['SAMPLES'])))).transpose()

            newdata = np.empty((512, 0), int)
            newdata = np.append(newdata, data1[:, output[1]], axis=1)
            newdata = np.append(newdata, data2[:, output[3]], axis=1)
            newdata = np.append(newdata, data3[:, output[5]], axis=1)
            newdata = np.append(newdata, data4[:, output[7]], axis=1)
            newdata = np.append(newdata, data5[:, output[9]], axis=1)

            np.save(self.file.name, newdata)

        else:
            'do nothing'

    def DC_shift(self):
        DC_shift(self.file.name)

    def timezero_adjustment(self):
        timezero_adjust('trace_collection.npy')

    def netcdf_variables(self, netcdf_dataset):
        self.NETCDF_dataset = netcdf_dataset
        self.xpixels = net_cdf_variables.define_NetCDF_variables(netcdf_dataset)[0]
        self.ypixels = net_cdf_variables.define_NetCDF_variables(netcdf_dataset)[1]
        self.zpixels = net_cdf_variables.define_NetCDF_variables(netcdf_dataset)[2]
        self.pixelsize = net_cdf_variables.define_NetCDF_variables(netcdf_dataset)[3]
        self.x_coor = net_cdf_variables.define_NetCDF_variables(netcdf_dataset)[5]
        self.y_coor = net_cdf_variables.define_NetCDF_variables(netcdf_dataset)[4]

        return self.x_coor, self.y_coor, self.xpixels, self.ypixels, self.pixelsize

    def exit_schlitzi(self):
        self.toplevel_1_schlizi.destroy()

    def open_vemop_project(self):
        self.vemop_project = filedialog.askopenfilename(title="Select vemop file", filetypes=[("vemop project file", "*.vemop")], parent=self.toplevel_1_schlizi)

        if self.vemop_project:
            self.destroy_single_interface()
            self.fill_vemop_list()
            self.create_vemop_interface()
            self.offsets_to_first()

            self.checkbutton_list =[]

            row_MIRA = 0
            row_GX = 0

            for i in range(len(self.vemop_proj)):
                self.cvar = tk.StringVar()
                self.cvar.set('off')

                if self.vemop_proj[i][5] == str(0):
                    Checkbutton(self.data_avail_frame, text=self.vemop_proj[i][1], variable=self.cvar,
                                onvalue=self.vemop_proj[i][0], offvalue='off',
                                command=lambda m=self.cvar: self.switch(m)).grid(row=row_MIRA, column=0, sticky='w')
                    self.checkbutton_list.append(self.cvar)
                    row_MIRA += 1

                else:
                    Checkbutton(self.data_avail_frame, text=self.vemop_proj[i][1], variable=self.cvar,
                                onvalue=self.vemop_proj[i][0], offvalue='off',
                                command=lambda m=self.cvar: self.switch(m)).grid(row=row_GX, column=1, sticky='w')
                    self.checkbutton_list.append(self.cvar)
                    row_GX += 1

    def create_vemop_interface(self):
        height_frame = (GetSystemMetrics(1) / 100) * 90
        width_frame = GetSystemMetrics(0) / 2

        self.vemop_frame = Frame(self.toplevel_1_schlizi, highlightbackground='black', highlightthickness=1)
        self.vemop_frame.place(x=width_frame + 234, y=5)

        self.data_avail_frame = Frame(self.vemop_frame, width=400, height=200, highlightbackground='black', highlightthickness=1)
        self.data_avail_frame.grid(row=0, column=0)

        self.which_surveys = Button(self.vemop_frame, text='Open traces', command=self.open_traces)
        self.which_surveys.grid(row=1, column=0)

        self.get_trace_button = Button(self.vemop_frame, text='Get traces', command=self.ask_number)
        self.get_trace_button.grid(row=1, column=1)

        self.get_section_button = Button(self.vemop_frame, text='Interpolate profile', command=self.create_virtual_section)
        self.get_section_button.grid(row=2, column=1)

        self.ivar_viewer = tk.IntVar()
        self.view_mode = Checkbutton(self.vemop_frame, text='Viewer mode', variable=self.ivar_viewer, onvalue=1, offvalue=0, command=self.viewer_mode)
        self.view_mode.grid(row=0, column=1)

        self.ivar_analysis = tk.IntVar()
        self.analyse_mode = Checkbutton(self.vemop_frame, text='Analysis mode', variable=self.ivar_analysis, onvalue=1, offvalue=0, command=self.analysis_mode)
        self.analyse_mode.grid(row=0, column=2)

    def fill_vemop_list(self):
        with open(self.vemop_project) as vemop:

            self.vemop_proj = []

            for line in vemop.readlines():
                single_line = line.rsplit(',')
                line_nr = int(single_line[0])

                line_list = [single_line[0], single_line[1], single_line[2], single_line[3], single_line[4],
                             single_line[5], single_line[6], single_line[7], single_line[8], single_line[9]]

                try:
                    comm = line[find_nth(line, ',', 10) + 1:]
                    formatted_comm = comm.rstrip().replace(r'\\n', '\n')
                    line_list.append(formatted_comm)
                except ValueError:
                    'nix'

                self.vemop_proj.append(line_list)

    def offsets_to_first(self):
        self.offsets = []
        center_0_x = self.netcdf_variables(self.vemop_proj[0][7])[0] + ((self.netcdf_variables(self.vemop_proj[0][7])[2]/2) * self.netcdf_variables(self.vemop_proj[0][7])[4])
        center_0_y = float(self.netcdf_variables(self.vemop_proj[0][7])[1]) + ((float(self.netcdf_variables(self.vemop_proj[0][7])[3])/2) * float(self.netcdf_variables(self.vemop_proj[0][7])[4]))

        for i in range(0, len(self.vemop_proj)):
            offset_i_x = self.netcdf_variables(self.vemop_proj[i][7])[0] + ((self.netcdf_variables(self.vemop_proj[i][7])[2]/2) * self.netcdf_variables(self.vemop_proj[i][7])[4])
            offset_i_y = float(self.netcdf_variables(self.vemop_proj[i][7])[1]) + ((float(self.netcdf_variables(self.vemop_proj[i][7])[3]/2)) * float(self.netcdf_variables(self.vemop_proj[i][7])[4]))
            offset_x = (center_0_x - offset_i_x) * -1
            offset_y = (center_0_y - offset_i_y) * 1

            self.offsets.append([round(offset_x, 2), round(offset_y, 2)])

    def selection(self):
        self.selection_list = []
        for item in self.checkbutton_list:
            if not item.get() == 'off':
                self.selection_list.append(int(item.get()) - 1)

        print(self.selection_list)

    def get_survey_dates(self):
        self.selection()

        for item in self.selection_list:
            print(self.vemop_proj[item][2])

    def viewer_mode(self):
        for item in self.checkbutton_list:
            item.set('off')

        self.checkbutton_list[0].set(self.vemop_proj[0][0])

        self.ivar_analysis.set(0)

    def analysis_mode(self):
        self.ivar_viewer.set(0)

    def switch(self, checkbutton):
        if self.ivar_viewer.get() == 1:

            self.number = int(str(checkbutton).replace('PY_VAR', ''))
            print(self.number)

            for item in self.checkbutton_list:
                item.set('off')

            self.checkbutton_list[self.number-3].set(self.vemop_proj[self.number-3][0])

            current_depth = int(int(self.text1.get('1.0', 'end-1c').rsplit('.', 1)[0][-3:])/5)

            file = self.vemop_proj[self.current_onbutton()][7]
            path =  file.rsplit('/', 1)[0]
            filename = file.rsplit('/', 1)[1].rsplit('.', 1)[0]
            new_path = path + '/NetCDF_img_' + filename

            self.list_depthslices(new_path)
            self.text1.delete('1.0', END)
            self.text1.insert(INSERT, self.list_depthslices(new_path.strip("\n"))[current_depth - 1])
            self.netcdf_variables(netcdf_dataset=file)
            os.chdir(new_path)

            self.show_image()
            self.redraw_switch()

        else:
            'do nothing'

    def current_onbutton(self):
        self.on_list = []
        self.on_list.clear()

        for item in self.checkbutton_list:
            self.on_list.append(item.get())

        self.on_list = remove_values_from_list(self.on_list, 'off')
        active_nr = int(self.on_list[0]) - 1

        try:
            self.last = int(self.text12.get('1.0', END).strip('\n'))
        except ValueError:
            self.last = 0

        self.text12.delete('1.0', END)
        self.text12.insert(INSERT, active_nr)

        return active_nr

    def get_closest_trace(self):
        self.trace_list = []

        self.n = self.number_of_traces

        self.current_onbutton()
        if self.ivar_analysis.get() == 1:
            try:
                x = float(self.texfolder_ds.get('1.0', 'end'))
                y = float(self.text3.get('1.0', 'end'))

                width_frame = GetSystemMetrics(0) / 2

                self.trace_frame = Frame(self.toplevel_1_schlizi, width=200, height=50, highlightbackground='black', highlightthickness=1)
                self.trace_frame.place(x=width_frame + 190, y=350)
                self.trace_info = tk.Listbox(self.trace_frame, width=75, height=15)
                self.trace_info.pack()
                self.trace_info.bind("<<ListboxSelect>>", self.show_single_trace)

                self.single_var = tk.IntVar()
                self.single_cb = Checkbutton(self.trace_frame, text='Single trace', variable=self.single_var, onvalue=1, offvalue=0, command=self.trace_mode_single)
                self.single_cb.pack()
                self.single_var.set(1)

                self.multi_var = tk.IntVar()
                self.multi_cb = Checkbutton(self.trace_frame, text='Muliple traces', variable=self.multi_var, onvalue=1, offvalue=0, command=self.trace_mode_multi)
                self.multi_cb.pack()

                self.spec_var = tk.IntVar()
                self.spec = Checkbutton(self.trace_frame, text='Spectral analysis', variable=self.spec_var, onvalue=1, offvalue=0, command=self.spectral_analysis)
                self.spec.pack()

                self.section_view = Button(self.trace_frame, text='Show profile', command=self.show_section, state='disabled')
                self.section_view.pack()


            except:
                no_point = tk.Toplevel()
                no_point.title("Schlitzi+")
                no_point.geometry("350x150")
                no_point.propagate(0)
                no_point.iconbitmap('c:/01_privat/01_Prog/VEMOP/02_development/Schlizi/Gjellestad.ico')
                no_point.attributes('-topmost', True)

                lab = Label(no_point, text='No point selected. Use right-click on image to select a point.')
                lab.pack()

                ok_butt = Button(no_point, text='OK', command=no_point.destroy)
                ok_butt.pack()

            for item in self.on_list:
                try:
                    shpfile = self.vemop_proj[int(item)-1][8]
                    pkl = str(shpfile.rsplit('.')[0]) + '.pickle'
                    npy = str(shpfile.rsplit('.')[0]) + '.npy'

                    print(pkl)

                    dist, indices = nn_from_file(pkl, x=x, y=y, n=self.n)[0], nn_from_file(pkl, x=x, y=y, n=self.n)[1]
                    trace_info = kd_int_to_point_info(npy, indices)

                    for i in range(len(trace_info)):
                        info_text = str(self.vemop_proj[int(item)-1][1]) + ' -- Line: ' + str(trace_info[i][0]) + ', Channel: ' + str(trace_info[i][1]) + ', Trace: ' + str(trace_info[i][2]) + ', Distance: ' + str(dist[i]) + 'm' + '\n'

                        self.trace_info.insert(tk.END, info_text)
                        single_trace = [item, trace_info[i][0], trace_info[i][1], trace_info[i][2]]
                        self.trace_list.append(single_trace)

                except IndexError:
                    no_data = tk.Toplevel()
                    no_data.title("Schlitzi+")
                    no_data.geometry("350x150")
                    no_data.propagate(0)
                    no_data.iconbitmap('c:/01_privat/01_Prog/VEMOP/02_development/Schlizi/Gjellestad.ico')
                    no_data.attributes('-topmost', True)

                    lab = Label(no_data, text='No dataset selected. Select a dataset first!')
                    lab.pack()

                    ok_butt = Button(no_data, text='OK', command=no_data.destroy)
                    ok_butt.pack()

            print(self.trace_list)

        else:
            print('ERRor')

    def trace_mode_single(self):
        self.multi_var.set(0)
        self.single_var.set(1)
        self.spec_var.set(0)

    def trace_mode_multi(self):
        self.multi_var.set(1)
        self.single_var.set(0)
        self.spec_var.set(0)

    def spectral_analysis(self):
        self.multi_var.set(0)
        self.single_var.set(0)
        self.spec_var.set(1)

    def ask_number(self):
        def get_nr():
            self.number_of_traces = int(self.enter_tr.get())
        self.number_tr = tk.Toplevel()
        self.number_tr.title("Schlitzi+")
        self.number_tr.geometry("300x100")
        #self.number_tr.eval('tk::PlaceWindow . center')
        self.number_tr.propagate(0)
        self.number_tr.iconbitmap('c:/01_privat/01_Prog/VEMOP/02_development/Schlizi/Gjellestad.ico')


        self.info_lab = Label(self.number_tr, text='Enter number of closest traces. Default = 1')
        self.info_lab.pack()
        self.enter_tr = Entry(self.number_tr)
        self.enter_tr.pack()
        self.enter_tr.insert(INSERT, 1)

        self.ok_butt = Button(self.number_tr, text='OK', command=lambda:[get_nr(), self.number_tr.destroy(), self.get_closest_trace()])
        self.ok_butt.pack()

    def open_traces(self):
        if self.n == 1:
            self.traces = np.array()
            for item in self.trace_list:
                trace = self.load_trace()
                self.traces.append(trace)

                'save traces to single files, with traceinformation as filename???'

        elif self.n >= 1:
            self.traces = np.array()
            for i in range(len(self.trace_list)):
                for item in self.on_list:
                    if int(self.trace_list[i][0]) == item:
                        trace = self.load_trace()
                        self.traces.append(trace)

        '''ttt'''#start_trace_viewer()

    def show_single_trace(self, event):
        #if self.multi_var.get() == 0:
        #    try:
        #        plt.close()
        #    except:
        #        'do nothing'

        if self.trace_info.curselection() != ():
            self.section_view['state'] = 'normal'
            trace = self.trace_info.get(self.trace_info.curselection())
            proj_name = str(trace).split(' -- ')[0].strip()
            proj_ar = np.array(self.vemop_proj)
            proj_ind = np.where(proj_ar == proj_name)[0][0]

            sys = int(self.vemop_proj[proj_ind][5])

            inf = str(trace).split(',')

            line = inf[0].split('-- ')[1].split(': ')[1]
            channel = inf[1].split(': ')[1]
            trace = int(inf[2].split(': ')[1])

            data_link = self.vemop_proj[proj_ind][9]

            print(data_link, line, channel, trace, sys)

            data_all = open_trace(data_link, line, channel, trace, sys)
            data = data_all[0]
            sig = data[:, trace]

            np.save('trace_for_spectral_analysis.npy', sig)
            signal = np.load('trace_for_spectral_analysis.npy')

            filename = data_all[1]
            sampling_frequency = float(data_all[2])
            timewindow = round(float(data_all[3])/1000, 7)
            number_of_samples = int(data_all[4])




            if sys == 0:
                y = range(512, 0, -1)
            elif sys == 1:
                y = range(343, 0, -1)

            if self.single_var.get() == 1:
                x = data[:, trace]
                y = y
                plt.figure(100)
                plt.plot(x, y)

                plt.show()

            elif self.spec_var.get() == 1:

                samples_time = np.arange(0, timewindow, timewindow/number_of_samples)

                signal_flat = signal.flatten()

                freq_axis = np.size(samples_time)  # frecqyency axis

                freq = (sampling_frequency//7) * np.linspace(0, 1, freq_axis//7)  # frequency axis

                signal_fft = fft(signal_flat)
                signal_magnitude = (2 / freq_axis) * abs(signal_fft[0:np.size(freq)])

                signal_magnitude[0] = 0

                plt.subplot(4, 1, 3)
                plt.plot(samples_time, signal)
                plt.title('GPR Signal')
                plt.xlabel('Time(ns)')
                plt.ylabel('Amplitude')

                plt.subplot(4, 1, 4)
                plt.plot(freq, signal_magnitude)
                plt.title('Frequency Spectrum')
                plt.xlabel('Frequency(MHz)')
                plt.ylabel('Magnitude')

                plt.show()

    def show_section(self):
        trace = self.trace_info.get(self.trace_info.curselection())
        proj_name = str(trace).split(' -- ')[0].strip()
        proj_ar = np.array(self.vemop_proj)
        proj_ind = np.where(proj_ar == proj_name)[0][0]

        sys = int(self.vemop_proj[proj_ind][5])

        inf = str(trace).split(',')

        line = inf[0].split('-- ')[1].split(': ')[1]
        channel = inf[1].split(': ')[1]
        trace = int(inf[2].split(': ')[1])

        data_link = self.vemop_proj[proj_ind][9]

        data, filename = open_trace(data_link, line, channel, trace, sys)[0], open_trace(data_link, line, channel, trace, sys)[1]
        shape = (data.shape[0], 500)

        newdata = np.asmatrix(np.zeros(shape))
        newdata = data[:, trace-250:trace + 250]

        newdata2 = data[:, trace - 1250:trace - 750]

        print(newdata2.shape)

        plt.figure(200)
        plt.subplot(1, 2, 1)
        plt.imshow(newdata, cmap='gray', vmin=-1500, vmax=1500)

        plt.subplot(1, 2, 2)
        plt.imshow(newdata2, cmap='gray', vmin=-1500, vmax=1500)

        plt.show()

    def interpolate_along_line(self):
        interval = 0.05
        startY, startX = float(self.text3.get('1.0', 'end')), float(self.texfolder_ds.get('1.0', 'end'))
        endY, endX = float(self.text5.get('1.0', 'end')), float(self.text4.get('1.0', 'end'))
        dist = sqrt(((startY - endY) ** 2) + ((startX - endX) ** 2))
        self.num_samples = round(dist / interval)
        self.int_points = []

        for i in range(self.num_samples + 1):
            x_neu = round(startX + ((interval / dist * i) * (endX - startX)), 3)
            y_neu = round(startY + ((interval / dist * i) * (endY - startY)), 3)
            pnt = [x_neu, y_neu]
            self.int_points.append(pnt)

    def draw_points_on_canvas(self):
        self.interpolate_along_line()

        try:
            if self.ivar_viewer.get() == 1 or self.ivar_analysis.get() == 1:
                print('here')
                list_on = []

                for item in self.checkbutton_list:
                    list_on.append(item.get())

                list_on = remove_values_from_list(list_on, 'off')

                if self.last != int(list_on[0]) - 1:
                    x_off, y_off = self.x_off_switch, self.y_off_switch
                else:
                    x_off, y_off = self.x_off_switch, self.y_off_switch

            else:
                x_off, y_off = 0, 0
                print('fal')
        except:
            x_off, y_off = 0, 0
            print('ssse')

        for item in self.int_points:
            canXpoint = (((item[0] - self.centerx) * self.imscale) / self.pixelsize)
            canXXpoint = round(canXpoint, 0) + (x_off * self.imscale)

            canYpoint = (((item[1] - self.centery) * self.imscale) / self.pixelsize)
            canYYpoint = round(-canYpoint, 0) + (y_off * self.imscale)
            self.int_point = self.canvas.create_oval(canXXpoint + 2.5, canYYpoint + 2.5, canXXpoint - 2.5, canYYpoint - 2.5, fill='red')

    def create_virtual_section(self):
        self.draw_points_on_canvas()

        width_frame = GetSystemMetrics(0) / 2

        self.trace_frame = Frame(self.toplevel_1_schlizi, width=200, height=50, highlightbackground='black',
                                 highlightthickness=1)
        self.trace_frame.place(x=width_frame + 190, y=350)
        self.trace_info = tk.Listbox(self.trace_frame, width=75, height=15)
        self.trace_info.pack()
        self.trace_info.bind("<<ListboxSelect>>", self.show_single_trace)

        self.single_var = tk.IntVar()
        self.single_cb = Checkbutton(self.trace_frame, text='Single trace', variable=self.single_var,
                                     onvalue=1, offvalue=0, command=self.trace_mode_single)
        self.single_cb.pack()
        self.single_var.set(1)

        self.multi_var = tk.IntVar()
        self.multi_cb = Checkbutton(self.trace_frame, text='Muliple traces', variable=self.multi_var,
                                    onvalue=1, offvalue=0, command=self.trace_mode_multi)
        self.multi_cb.pack()

        self.section_view = Button(self.trace_frame, text='Show profile', command=self.show_section,
                                   state='disabled')
        self.section_view.pack()

        self.virtual_section = Button(self.trace_frame, text='Show virtual section', command=self.show_virtual_profile)
        self.virtual_section.pack()

        self.virtual_section_DC = Button(self.trace_frame, text='Show virtual section / DC-shift', command=self.apply_DC)
        self.virtual_section_DC.pack()

        self.virtual_section_timezero = Button(self.trace_frame, text='Show virtual section / timezero', command=self.apply_timezero)
        self.virtual_section_timezero.pack()

        for item in self.int_points:
            self.trace_list = []

            self.n = 1

            self.current_onbutton()
            if self.ivar_analysis.get() == 1:

                x = item[0]
                y = item[1]

                for item in self.on_list:
                    try:
                        shpfile = self.vemop_proj[int(item) - 1][8]
                        pkl = str(shpfile.rsplit('.')[0]) + '.pickle'
                        npy = str(shpfile.rsplit('.')[0]) + '.npy'

                        dist, indices = nn_from_file(pkl, x=x, y=y, n=self.n)[0], nn_from_file(pkl, x=x, y=y, n=self.n)[
                            1]
                        trace_info = kd_int_to_point_info(npy, indices)

                        for i in range(len(trace_info)):
                            info_text = str(self.vemop_proj[int(item) - 1][1]) + ' -- Line: ' + str(
                                trace_info[i][0]) + ', Channel: ' + str(trace_info[i][1]) + ', Trace: ' + str(
                                trace_info[i][2]) + ', Distance: ' + str(dist[i]) + 'm' + '\n'

                            self.trace_info.insert(tk.END, info_text)
                            single_trace = [item, trace_info[i][0], trace_info[i][1], trace_info[i][2]]
                            self.trace_list.append(single_trace)

                    except IndexError:
                        no_data = tk.Toplevel()
                        no_data.title("Schlitzi+")
                        no_data.geometry("350x150")
                        no_data.propagate(0)
                        no_data.iconbitmap('c:/01_privat/01_Prog/VEMOP/02_development/Schlizi/Gjellestad.ico')
                        no_data.attributes('-topmost', True)

                        lab = Label(no_data, text='No dataset selected. Select a dataset first!')
                        lab.pack()

                        ok_butt = Button(no_data, text='OK', command=no_data.destroy)
                        ok_butt.pack()

                print(self.trace_list)

            else:
                print('ERRor')

    def show_virtual_profile(self):
        all_traces = self.trace_info.get(0, END)

        alldata = []
        newdata = np.empty((512, 0), int)

        for item in all_traces:
            trace = item.strip('\n')

            proj_name = str(trace).split(' -- ')[0].strip()
            proj_ar = np.array(self.vemop_proj)
            proj_ind = np.where(proj_ar == proj_name)[0][0]

            sys = int(self.vemop_proj[proj_ind][5])

            inf = str(trace).split(',')

            line = inf[0].split('-- ')[1].split(': ')[1]
            channel = inf[1].split(': ')[1]
            trace = int(inf[2].split(': ')[1])

            data_link = self.vemop_proj[proj_ind][9]

            data, filename = open_trace(data_link, line, channel, trace, sys)[0], \
                             open_trace(data_link, line, channel, trace, sys)[1]

            newdata = np.append(newdata, data[:, trace], axis=1)

        np.save('virtual_section.npy', newdata)
        plt.figure(300)
        plt.imshow(newdata, cmap='gray', vmin=-1500, vmax=1500)

        plt.show()

    def apply_DC(self):
        data = np.load('virtual_section.npy')

        newdata_DC_shift = np.asmatrix(np.zeros(data.shape))

        for tr in range(0, data.shape[1]):
            mean10 = int(np.round(np.mean(data[:10, tr])))
            newdata_DC_shift[:, tr] = np.reshape(data[:, tr] - mean10, (512, 1))

        plt.figure(400)
        plt.subplot(1, 2, 1)
        plt.imshow(data, cmap='gray', vmin=-1500, vmax=1500)

        plt.subplot(1, 2, 2)
        plt.imshow(newdata_DC_shift, cmap='gray', vmin=-1500, vmax=1500)

        plt.show()

        np.save('virtual_section_DC.npy', newdata_DC_shift)

    def apply_timezero(self):
        data = np.load('virtual_section_DC.npy')

        maxlen = data.shape[0]
        newdata_timezero = np.asmatrix(np.zeros(data.shape))

        # Go through all traces to find maximum spike
        maxind = np.zeros(data.shape[1], dtype=int)

        for tr in range(0, data.shape[1]):
            maxind[tr] = int(np.argmax(data[:, tr]))

        # Find the mean spike point
        meanind = int(np.round(np.mean(maxind)))

        # Shift all traces. If max index is smaller than
        # mean index, then prepend zeros, otherwise append
        for tr in range(0, data.shape[1]):
            if meanind > maxind[tr]:
                differ = int(meanind - maxind[tr])
                newdata_timezero[:, tr] = np.reshape(
                    np.concatenate([np.zeros((differ)), data[0:(maxlen - differ), tr]]),
                    (512, 1))
            elif meanind <= maxind[tr]:
                differ = maxind[tr] - meanind
                # newdata_aligned = np.append(newdata_aligned, np.concatenate([data[differ:maxlen, tr], np.zeros((differ))]), axis=1)
                newdata_timezero[:, tr] = np.reshape(np.concatenate([data[differ:maxlen, tr], np.zeros((differ))]),
                                                     (512, 1))

        plt.figure(400)
        plt.subplot(1,2,1)
        plt.imshow(data, cmap='gray', vmin=-1500, vmax=1500)

        plt.subplot(1,2,2)
        plt.imshow(newdata_timezero, cmap='gray', vmin=-1500, vmax=1500)

        plt.show()

        np.save('virtual_section_timezero.npy', newdata_timezero)


class Vemop:
    def __init__(self, number, name, date, time_start, time_stop, system, NetCDF, shp, proj, comment):
        self.number = number
        self.name = name
        self.date = date
        self.time_start = time_start
        self.time_stop = time_stop
        self.system = system
        self.NetCDF = NetCDF
        self.shp = shp
        self.proj = proj
        self.comment = comment

def toggle():
    if c_var.get() == 1:
        b1.configure(state='active')
    else:
        b1.configure(state='disabled')

def start_schlitzi():
    global root
    no_human.destroy()
    root = Tk()
    root.title("Shlitzi+")
    root.geometry("600x300")
    root.propagate(0)
    root.iconbitmap('Gjellestad.ico')
    # root.attributes('-topmost', True)
    app = MainWindow(root)
    app.mainloop()

if datetime.strptime(str(date.today()), '%Y-%M-%d') < datetime.strptime('2021-12-31', '%Y-%M-%d'):
    no_human = Tk()
    no_human.title('Schlitzi+')
    no_human.geometry('250x75')
    no_human.eval('tk::PlaceWindow . center')
    no_human.iconbitmap('Gjellestad.ico')
    no_human.propagate(0)

    f1 = Frame(no_human, width=75, height=25)
    f1.pack(fill=BOTH, expand=1)
    f1.pack_propagate()

    c_var = tk.IntVar()
    c1 = Checkbutton(no_human, variable=c_var, onvalue=1, offvalue=0, command=start_schlitzi)
    c1.grid(row=2, column=0)

    t1 = Label(f1, text='        I`m not a human')
    t1.grid(row=2, column=1)

    no_human.mainloop()

else:
    no_license = Tk()
    no_license.title('Schlitzi+')
    no_license.geometry('300x165')
    no_license.iconbitmap('Gjellestad.ico')
    no_license.propagate(0)

    f1 = Frame(no_license)
    f1.pack(fill=BOTH, expand=1)

    t1 = Label(f1, text = '\n\nLisence expired 2021-09-30 \n Contact Kong Erich Nau (erich.nau@niku.no) \n\n\n\n')
    t1.pack()

    b1 = Button(f1, text='OK', command=no_license.destroy)
    b1.pack()

    no_license.mainloop()


