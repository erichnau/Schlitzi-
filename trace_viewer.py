from tkinter import *
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt
import numpy as np
import os

class TraceViewer(Frame, object):
    def __init__(self, master):
        super(TraceViewer, self). \
            __init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.mainframe = Frame(root_4)
        self.mainframe.pack(ipady=20, fill='both')

        self.tool_frame = Frame(self.mainframe, borderwidth=3, relief='sunken', height=25)
        self.tool_frame.pack(ipady=20, fill='x')

        '''TOOLS'''
        self.DC_shift_Button = Button(self.tool_frame, text='DC-shift')#, command=self.calculate_DC_shift)
        self.DC_shift_Button.grid(row=0, column=1)

        self.timezero_adjustment = Button(self.tool_frame, text='Timezero')#, command=self.calculacte_timezero)
        self.timezero_adjustment.grid(row=0, column=2)

        self.trace_frame = Frame(self.mainframe, borderwidth=3, relief='sunken')
        self.trace_frame.pack(ipady=20, fill=BOTH)


#def start_trace_viewer():
#        global root_4

os.chdir(str(__file__).rsplit('\\', 1)[0])
root_4 = tk.Tk()
root_4.title('Trace details')
root_4.state('zoomed')
root_4.iconbitmap('Gjellestad.ico')
root_4.attributes('-topmost', True)

app = TraceViewer(root_4)
app.mainloop()