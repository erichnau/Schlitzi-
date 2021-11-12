from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from os import path
import netCDF4 as nc
import xarray as xr
from matplotlib import pyplot as plt
from tkinter.ttk import Progressbar
from tkcalendar import Calendar
import datetime
from win32api import GetSystemMetrics
from net_cdf_variables import find_nth
import shp_tools

class DefineVEMOP(Frame, object):
    def __init__(self, master):
        super(DefineVEMOP, self). \
            __init__(master)
        self.pack()
        self.survey_label_Dict = {1: 'self.survey_nr_1', 2: 'self.survey_nr_2', 3: 'self.survey_nr_3',
                                  4: 'self.survey_nr_4', 5: 'self.survey_nr_5',
                                  6: 'self.survey_nr_6', 7: 'self.survey_nr_7', 8: 'self.survey_nr_8',
                                  9: 'self.survey_nr_9', 10: 'self.survey_nr_10',
                                  11: 'self.survey_nr_11', 12: 'self.survey_nr_12', 13: 'self.survey_nr_13',
                                  14: 'self.survey_nr_14', 15: 'self.survey_nr_15',
                                  16: 'self.survey_nr_16', 17: 'self.survey_nr_17', 18: 'self.survey_nr_18',
                                  19: 'self.survey_nr_19', 20: 'self.survey_nr_20',
                                  21: 'self.survey_nr_21', 22: 'self.survey_nr_22', 23: 'self.survey_nr_23',
                                  24: 'self.survey_nr_24', 25: 'self.survey_nr_25'}
        self.def_netCDF_Dict = {1: 'self.def_netCDF_1', 2: 'self.def_netCDF_2', 3: 'self.def_netCDF_3',
                                4: 'self.def_netCDF_4', 5: 'self.def_netCDF_5',
                                6: 'self.def_netCDF_6', 7: 'self.def_netCDF_7', 8: 'self.def_netCDF_8',
                                9: 'self.def_netCDF_9', 10: 'self.def_netCDF_10',
                                11: 'self.def_netCDF_11', 12: 'self.def_netCDF_12', 13: 'self.def_netCDF_13',
                                14: 'self.def_netCDF_14', 15: 'self.def_netCDF_15',
                                16: 'self.def_netCDF_16', 17: 'self.def_netCDF_17', 18: 'self.def_netCDF_18',
                                19: 'self.def_netCDF_19', 20: 'self.def_netCDF_20',
                                21: 'self.def_netCDF_21', 22: 'self.def_netCDF_22', 23: 'self.def_netCDF_23',
                                24: 'self.def_netCDF_24', 25: 'self.def_netCDF_25'}
        self.netCDF_Dict = {1: 'self.netCDF_1', 2: 'self.netCDF_2', 3: 'self.netCDF_3', 4: 'self.netCDF_4',
                            5: 'self.netCDF_5',
                            6: 'self.netCDF_6', 7: 'self.netCDF_7', 8: 'self.netCDF_8', 9: 'self.netCDF_9',
                            10: 'self.netCDF_10',
                            11: 'self.netCDF_11', 12: 'self.netCDF_12', 13: 'self.netCDF_13', 14: 'self.netCDF_14',
                            15: 'self.netCDF_15',
                            16: 'self.netCDF_16', 17: 'self.netCDF_17', 18: 'self.netCDF_18', 19: 'self.netCDF_19',
                            20: 'self.netCDF_20',
                            21: 'self.netCDF_21', 22: 'self.netCDF_22', 23: 'self.netCDF_23', 24: 'self.netCDF_24',
                            25: 'self.netCDF_25'}
        self.def_antenna_points_Dict = {1: 'self.def_antenna_points_1', 2: 'self.def_antenna_points_2',
                                        3: 'self.def_antenna_points_3', 4: 'self.def_antenna_points_4',
                                        5: 'self.def_antenna_points_5',
                                        6: 'self.def_antenna_points_6', 7: 'self.def_antenna_points_7',
                                        8: 'self.def_antenna_points_8', 9: 'self.def_antenna_points_9',
                                        10: 'self.def_antenna_points_10',
                                        11: 'self.def_antenna_points_11', 12: 'self.def_antenna_points_12',
                                        13: 'self.def_antenna_points_13', 14: 'self.def_antenna_points_14',
                                        15: 'self.def_antenna_points_15',
                                        16: 'self.def_antenna_points_16', 17: 'self.def_antenna_points_17',
                                        18: 'self.def_antenna_points_18', 19: 'self.def_antenna_points_19',
                                        20: 'self.def_antenna_points_20',
                                        21: 'self.def_antenna_points_21', 22: 'self.def_antenna_points_22',
                                        23: 'self.def_antenna_points_23', 24: 'self.def_antenna_points_24',
                                        25: 'self.def_antenna_points_25'}
        self.antenna_points_Dict = {1: 'self.antenna_points_1', 2: 'self.antenna_points_2', 3: 'self.antenna_points_3',
                                    4: 'self.antenna_points_4', 5: 'self.antenna_points_5',
                                    6: 'self.antenna_points_6', 7: 'self.antenna_points_7', 8: 'self.antenna_points_8',
                                    9: 'self.antenna_points_9', 10: 'self.antenna_points_10',
                                    11: 'self.antenna_points_11', 12: 'self.antenna_points_12',
                                    13: 'self.antenna_points_13', 14: 'self.antenna_points_14',
                                    15: 'self.antenna_points_15',
                                    16: 'self.antenna_points_16', 17: 'self.antenna_points_17',
                                    18: 'self.antenna_points_18', 19: 'self.antenna_points_19',
                                    20: 'self.antenna_points_20',
                                    21: 'self.antenna_points_21', 22: 'self.antenna_points_22',
                                    23: 'self.antenna_points_23', 24: 'self.antenna_points_24',
                                    25: 'self.antenna_points_25'}
        self.def_mira_proj_Dict = {1: 'self.def_mira_proj_1', 2: 'self.def_mira_proj_2', 3: 'self.def_mira_proj_3',
                                   4: 'self.def_mira_proj_4', 5: 'self.def_mira_proj_5',
                                   6: 'self.def_mira_proj_6', 7: 'self.def_mira_proj_7', 8: 'self.def_mira_proj_8',
                                   9: 'self.def_mira_proj_9', 10: 'self.def_mira_proj_10',
                                   11: 'self.def_mira_proj_11', 12: 'self.def_mira_proj_12',
                                   13: 'self.def_mira_proj_13', 14: 'self.def_mira_proj_14',
                                   15: 'self.def_mira_proj_15',
                                   16: 'self.def_mira_proj_16', 17: 'self.def_mira_proj_17',
                                   18: 'self.def_mira_proj_18', 19: 'self.def_mira_proj_19',
                                   20: 'self.def_mira_proj_20',
                                   21: 'self.def_mira_proj_21', 22: 'self.def_mira_proj_22',
                                   23: 'self.def_mira_proj_23', 24: 'self.def_mira_proj_24',
                                   25: 'self.def_mira_proj_25'}
        self.mira_proj_Dict = {1: 'self.mira_proj_1', 2: 'self.mira_proj_2', 3: 'self.mira_proj_3',
                               4: 'self.mira_proj_4', 5: 'self.mira_proj_5',
                               6: 'self.mira_proj_6', 7: 'self.mira_proj_7', 8: 'self.mira_proj_8',
                               9: 'self.mira_proj_9', 10: 'self.mira_proj_10',
                               11: 'self.mira_proj_11', 12: 'self.mira_proj_12', 13: 'self.mira_proj_13',
                               14: 'self.mira_proj_14', 15: 'self.mira_proj_15',
                               16: 'self.mira_proj_16', 17: 'self.mira_proj_17', 18: 'self.mira_proj_18',
                               19: 'self.mira_proj_19', 20: 'self.mira_proj_20',
                               21: 'self.mira_proj_21', 22: 'self.mira_proj_22', 23: 'self.mira_proj_23',
                               24: 'self.mira_proj_24', 25: 'self.mira_proj_25'}
        self.remove_line_Dict = {1: 'self.remove_line_1', 2: 'self.remove_line_2', 3: 'self.remove_line_3',
                               4: 'self.remove_line_4', 5: 'self.remove_line_5',
                               6: 'self.remove_line_6', 7: 'self.remove_line_7', 8: 'self.remove_line_8',
                               9: 'self.remove_line_9', 10: 'self.remove_line_10',
                               11: 'self.remove_line_11', 12: 'self.remove_line_12', 13: 'self.remove_line_13',
                               14: 'self.remove_line_14', 15: 'self.remove_line_15',
                               16: 'self.remove_line_16', 17: 'self.remove_line_17', 18: 'self.remove_line_18',
                               19: 'self.remove_line_19', 20: 'self.remove_line_20',
                               21: 'self.remove_line_21', 22: 'self.remove_line_22', 23: 'self.remove_line_23',
                               24: 'self.remove_line_24', 25: 'self.remove_line_25'}
        self.project_name_Dict = {1: 'self.project_name_1', 2: 'self.project_name_2', 3: 'self.project_name_3',
                               4: 'self.project_name_4', 5: 'self.project_name_5',
                               6: 'self.project_name_6', 7: 'self.project_name_7', 8: 'self.project_name_8',
                               9: 'self.project_name_9', 10: 'self.project_name_10',
                               11: 'self.project_name_11', 12: 'self.project_name_12', 13: 'self.project_name_13',
                               14: 'self.project_name_14', 15: 'self.project_name_15',
                               16: 'self.project_name_16', 17: 'self.project_name_17', 18: 'self.project_name_18',
                               19: 'self.project_name_19', 20: 'self.project_name_20',
                               21: 'self.project_name_21', 22: 'self.project_name_22', 23: 'self.project_name_23',
                               24: 'self.project_name_24', 25: 'self.project_name_25'}
        self.project_date_Dict = {1: 'self.project_date_1', 2: 'self.project_date_2', 3: 'self.project_date_3',
                               4: 'self.project_date_4', 5: 'self.project_date_5',
                               6: 'self.project_date_6', 7: 'self.project_date_7', 8: 'self.project_date_8',
                               9: 'self.project_date_9', 10: 'self.project_date_10',
                               11: 'self.project_date_11', 12: 'self.project_date_12', 13: 'self.project_date_13',
                               14: 'self.project_date_14', 15: 'self.project_date_15',
                               16: 'self.project_date_16', 17: 'self.project_date_17', 18: 'self.project_date_18',
                               19: 'self.project_date_19', 20: 'self.project_date_20',
                               21: 'self.project_date_21', 22: 'self.project_date_22', 23: 'self.project_date_23',
                               24: 'self.project_date_24', 25: 'self.project_date_25'}
        self.check_mira_Dict = {1: 'self.check_mira_1', 2: 'self.check_mira_2', 3: 'self.check_mira_3',
                               4: 'self.check_mira_4', 5: 'self.check_mira_5',
                               6: 'self.check_mira_6', 7: 'self.check_mira_7', 8: 'self.check_mira_8',
                               9: 'self.check_mira_9', 10: 'self.check_mira_10',
                               11: 'self.check_mira_11', 12: 'self.check_mira_12', 13: 'self.check_mira_13',
                               14: 'self.check_mira_14', 15: 'self.check_mira_15',
                               16: 'self.check_mira_16', 17: 'self.check_mira_17', 18: 'self.check_mira_18',
                               19: 'self.check_mira_19', 20: 'self.check_mira_20',
                               21: 'self.check_mira_21', 22: 'self.check_mira_22', 23: 'self.check_mira_23',
                               24: 'self.check_mira_24', 25: 'self.check_mira_25'}
        self.check_GX = {1: 'self.check_GX_1', 2: 'self.check_GX_2', 3: 'self.check_GX_3',
                               4: 'self.check_GX_4', 5: 'self.check_GX_5',
                               6: 'self.check_GX_6', 7: 'self.check_GX_7', 8: 'self.check_GX_8',
                               9: 'self.check_GX_9', 10: 'self.check_GX_10',
                               11: 'self.check_GX_11', 12: 'self.check_GX_12', 13: 'self.check_GX_13',
                               14: 'self.check_GX_14', 15: 'self.check_GX_15',
                               16: 'self.check_GX_16', 17: 'self.check_GX_17', 18: 'self.check_GX_18',
                               19: 'self.check_GX_19', 20: 'self.check_GX_20',
                               21: 'self.check_GX_21', 22: 'self.check_GX_22', 23: 'self.check_GX_23',
                               24: 'self.check_GX_24', 25: 'self.check_GX_25'}
        self.calendar_Dict = {1: 'self.calendar_Dict_1', 2: 'self.calendar_Dict_2', 3: 'self.calendar_Dict_3',
                              4: 'self.calendar_Dict_4', 5: 'self.calendar_Dict_5',
                              6: 'self.calendar_Dict_6', 7: 'self.calendar_Dict_7', 8: 'self.calendar_Dict_8',
                              9: 'self.calendar_Dict_9', 10: 'self.calendar_Dict_10',
                              11: 'self.calendar_Dict_11', 12: 'self.calendar_Dict_12', 13: 'self.calendar_Dict_13',
                              14: 'self.calendar_Dict_14', 15: 'self.calendar_Dict_15',
                              16: 'self.calendar_Dict_16', 17: 'self.calendar_Dict_17', 18: 'self.calendar_Dict_18',
                              19: 'self.calendar_Dict_19', 20: 'self.calendar_Dict_20',
                              21: 'self.calendar_Dict_21', 22: 'self.calendar_Dict_22', 23: 'self.calendar_Dict_23',
                              24: 'self.calendar_Dict_24', 25: 'self.calendar_Dict_25'}
        self.checkvar1 = {1: 'self.checkvar_1', 2: 'self.checkvar_2', 3: 'self.checkvar_3',
                              4: 'self.checkvar_4', 5: 'self.checkvar_5',
                              6: 'self.checkvar_6', 7: 'self.checkvar_7', 8: 'self.checkvar_8',
                              9: 'self.checkvar_9', 10: 'self.checkvar_10',
                              11: 'self.checkvar_11', 12: 'self.checkvar_12', 13: 'self.checkvar_13',
                              14: 'self.checkvar_14', 15: 'self.checkvar_15',
                              16: 'self.checkvar_16', 17: 'self.checkvar_17', 18: 'self.checkvar_18',
                              19: 'self.checkvar_19', 20: 'self.checkvar_20',
                              21: 'self.checkvar_21', 22: 'self.checkvar_22', 23: 'self.checkvar_23',
                              24: 'self.checkvar_24', 25: 'self.checkvar_25'}
        self.checkvar2 = {1: 'self.checkvar2_1', 2: 'self.checkvar2_2', 3: 'self.checkvar2_3',
                              4: 'self.checkvar2_4', 5: 'self.checkvar2_5',
                              6: 'self.checkvar2_6', 7: 'self.checkvar2_7', 8: 'self.checkvar2_8',
                              9: 'self.checkvar2_9', 10: 'self.checkvar2_10',
                              11: 'self.checkvar2_11', 12: 'self.checkvar2_12', 13: 'self.checkvar2_13',
                              14: 'self.checkvar2_14', 15: 'self.checkvar2_15',
                              16: 'self.checkvar2_16', 17: 'self.checkvar2_17', 18: 'self.checkvar2_18',
                              19: 'self.checkvar2_19', 20: 'self.checkvar2_20',
                              21: 'self.checkvar2_21', 22: 'self.checkvar2_22', 23: 'self.checkvar2_23',
                              24: 'self.checkvar2_24', 25: 'self.checkvar2_25'}
        self.survey_time_start = {1: 'self.survey_time_start_1', 2: 'self.survey_time_start_2', 3: 'self.survey_time_start_3',
                              4: 'self.survey_time_start_4', 5: 'self.survey_time_start_5',
                              6: 'self.survey_time_start_6', 7: 'self.survey_time_start_7', 8: 'self.survey_time_start_8',
                              9: 'self.survey_time_start_9', 10: 'self.survey_time_start_10',
                              11: 'self.survey_time_start_11', 12: 'self.survey_time_start_12', 13: 'self.survey_time_start_13',
                              14: 'self.survey_time_start_14', 15: 'self.survey_time_start_15',
                              16: 'self.survey_time_start_16', 17: 'self.survey_time_start_17', 18: 'self.survey_time_start_18',
                              19: 'self.survey_time_start_19', 20: 'self.survey_time_start_20',
                              21: 'self.survey_time_start_21', 22: 'self.survey_time_start_22', 23: 'self.survey_time_start_23',
                              24: 'self.survey_time_start_24', 25: 'self.survey_time_start_25'}
        self.survey_time_stop = {1: 'self.survey_time_stop_1', 2: 'self.survey_time_stop_2', 3: 'self.survey_time_stop_3',
                              4: 'self.survey_time_stop_4', 5: 'self.survey_time_stop_5',
                              6: 'self.survey_time_stop_6', 7: 'self.survey_time_stop_7', 8: 'self.survey_time_stop_8',
                              9: 'self.survey_time_stop_9', 10: 'self.survey_time_stop_10',
                              11: 'self.survey_time_stop_11', 12: 'self.survey_time_stop_12', 13: 'self.survey_time_stop_13',
                              14: 'self.survey_time_stop_14', 15: 'self.survey_time_stop_15',
                              16: 'self.survey_time_stop_16', 17: 'self.survey_time_stop_17', 18: 'self.survey_time_stop_18',
                              19: 'self.survey_time_stop_19', 20: 'self.survey_time_stop_20',
                              21: 'self.survey_time_stop_21', 22: 'self.survey_time_stop_22', 23: 'self.survey_time_stop_23',
                              24: 'self.survey_time_stop_24', 25: 'self.survey_time_stop_25'}
        self.comment = {1: 'self.comment_1', 2: 'self.comment_2', 3: 'self.comment_3',
                              4: 'self.comment_4', 5: 'self.comment_5',
                              6: 'self.comment_6', 7: 'self.comment_7', 8: 'self.comment_8',
                              9: 'self.comment_9', 10: 'self.comment_10',
                              11: 'self.comment_11', 12: 'self.comment_12', 13: 'self.comment_13',
                              14: 'self.comment_14', 15: 'self.comment_15',
                              16: 'self.comment_16', 17: 'self.comment_17', 18: 'self.comment_18',
                              19: 'self.comment_19', 20: 'self.comment_20',
                              21: 'self.comment_21', 22: 'self.comment_22', 23: 'self.comment_23',
                              24: 'self.comment_24', 25: 'self.comment_25'}

        self.number_of_lines = 1
        self.create_frame()
        self.total_lines = 0
        self.top_line()
        self.add_input_line()
        self.comment_lst = []
        self.comment_text_lst = []

    def create_frame(self):
        #try:
        #    self.main_frame.destroy()
        #except AttributeError:
        #    'nix'

        self.top_frame = Frame(self.master, highlightbackground='black', highlightthickness='1', width=1500)
        self.top_frame.pack(side=TOP)
        self.title_frame = Frame(self.master, width=1650, height=25, highlightbackground='black', highlightthickness='1')
        self.title_frame.pack(side=TOP)

        self.main_frame = Frame(self.master, height=1500)
        self.main_frame.pack_propagate(0)
        self.main_frame.pack(side=BOTTOM, fill=BOTH)

        self.input_Canvas = Canvas(self.main_frame)

        self.scrollbar_vert = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.input_Canvas.yview)
        self.scrollbar_vert.pack(side=RIGHT, fill=Y)

        self.scrollbar_hori = ttk.Scrollbar(self.main_frame, orient=HORIZONTAL, command=self.input_Canvas.xview)
        self.scrollbar_hori.pack(side=BOTTOM, fill=X)

        self.input_Canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.input_Canvas.configure(yscrollcommand=self.scrollbar_vert.set, xscrollcommand=self.scrollbar_hori.set)
        self.input_Canvas.bind('<Configure>', lambda e: self.input_Canvas.configure(scrollregion=(0,0,5500,1500)))
        self.input_Canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.input_frame = Frame(self.input_Canvas)
        self.input_Canvas.create_window((0,0), window=self.input_frame, anchor='nw')

        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='New', command=self.new)
        self.filemenu.add_command(label='Open', command=self.open_project)
        self.filemenu.add_command(label='Save', command=self.save_project)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.exit)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        root_2_vemop.config(menu=self.menubar)

    def add_input_line(self):
        globals()[self.checkvar1[self.number_of_lines]] = IntVar()
        globals()[self.checkvar2[self.number_of_lines]] = IntVar()

        globals()[self.survey_label_Dict[self.number_of_lines]] = Label(self.input_frame, text=self.number_of_lines, width=2)
        globals()[self.survey_label_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=0)

        globals()[self.project_name_Dict[self.number_of_lines]] = Entry(self.input_frame, width=15)
        globals()[self.project_name_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=1)

        globals()[self.project_date_Dict[self.number_of_lines]] = Entry(self.input_frame, width=10)
        globals()[self.project_date_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=2, sticky=E)

        globals()[self.calendar_Dict[self.number_of_lines]] = Button(self.input_frame, text='calendar', command=lambda m = str(self.calendar_Dict[self.number_of_lines]): self.which_button(m))
        globals()[self.calendar_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=3, sticky=W)

        globals()[self.survey_time_start[self.number_of_lines]] = Entry(self.input_frame, width=5)
        globals()[self.survey_time_start[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=4)

        globals()[self.survey_time_stop[self.number_of_lines]] = Entry(self.input_frame, width=5)
        globals()[self.survey_time_stop[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=5)

        globals()[self.check_GX[self.number_of_lines]] = Checkbutton(self.input_frame, variable=globals()[self.checkvar1[self.number_of_lines]], onvalue=1, offvalue=0, command=lambda m = str(self.check_GX[self.number_of_lines]): self.which_checkbutton(m))
        globals()[self.check_GX[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=6)

        globals()[self.check_mira_Dict[self.number_of_lines]] = Checkbutton(self.input_frame, variable=globals()[self.checkvar2[self.number_of_lines]], onvalue=1, offvalue=0, command=lambda m = str(self.check_mira_Dict[self.number_of_lines]): self.which_checkbutton(m))
        globals()[self.check_mira_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=7)

        globals()[self.def_netCDF_Dict[self.number_of_lines]] = Button(self.input_frame, text='NetCDF', command=lambda m = str(self.def_netCDF_Dict[self.number_of_lines]): self.which_button(m))
        globals()[self.def_netCDF_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=8)

        globals()[self.netCDF_Dict[self.number_of_lines]] = self.netCDF_Dict[self.number_of_lines]
        globals()[self.netCDF_Dict[self.number_of_lines]] = Text(self.input_frame, width=33, height=3)
        globals()[self.netCDF_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=9)

        globals()[self.def_antenna_points_Dict[self.number_of_lines]] = Button(self.input_frame, text='Antenna points shp', command=lambda m = str(self.def_antenna_points_Dict[self.number_of_lines]): self.which_button(m))
        globals()[self.def_antenna_points_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=10)

        globals()[self.antenna_points_Dict[self.number_of_lines]] = self.antenna_points_Dict[self.number_of_lines]
        globals()[self.antenna_points_Dict[self.number_of_lines]] = Text(self.input_frame, width=33, height=3)
        globals()[self.antenna_points_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=11)

        buttontext ="MIRA project\nGX GPR-profile"
        globals()[self.def_mira_proj_Dict[self.number_of_lines]] = Button(self.input_frame, text=buttontext, justify='left', command=lambda m = str(self.def_mira_proj_Dict[self.number_of_lines]): self.which_button(m))
        globals()[self.def_mira_proj_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=12)

        globals()[self.mira_proj_Dict[self.number_of_lines]] = self.mira_proj_Dict[self.number_of_lines]
        globals()[self.mira_proj_Dict[self.number_of_lines]] = Text(self.input_frame, width=33, height=3)
        globals()[self.mira_proj_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=13)

        globals()[self.comment[self.number_of_lines]] = Button(self.input_frame, text='Comment', command=lambda m = str(self.comment[self.number_of_lines]): self.add_comment(m))
        globals()[self.comment[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=14)

        globals()[self.remove_line_Dict[self.number_of_lines]] = Button(self.input_frame, text='-', font=('Arial', 14, 'bold'), command=lambda m = str(self.remove_line_Dict[self.number_of_lines]): self.which_remove_button(m))
        globals()[self.remove_line_Dict[self.number_of_lines]].grid(row=self.number_of_lines + 2, column=15)

        self.number_of_lines = self.number_of_lines + 1
        self.total_lines = self.total_lines + 1

        try:
            self.exit_butt.destroy()
            self.button_add.destroy()
            self.button_validate.destroy()
            self.button_check_depthslices.destroy()
            self.placeholder1.destroy()
            self.placeholder.destroy()
            self.placeholder2.destroy()
            self.button_check_shp.destroy()


        except AttributeError:
            'nix'

        self.add_button()

    def which_remove_button(self, button_press):
        self.button_remove_pressed = button_press
        self.button_remove_nr = int(button_press[- (len(button_press) - int(button_press.rfind('_')) - 1):])
        self.button_remove_name = button_press[:- (len(button_press) - int(button_press.rfind('_')))]

        self.remove_input_line(self.button_remove_nr)

    def remove_input_line(self, number):
        globals()[self.survey_label_Dict[number]].destroy()
        globals()[self.def_netCDF_Dict[number]].destroy()
        globals()[self.netCDF_Dict[number]].destroy()
        globals()[self.def_antenna_points_Dict[number]].destroy()
        globals()[self.antenna_points_Dict[number]].destroy()
        globals()[self.def_mira_proj_Dict[number]].destroy()
        globals()[self.mira_proj_Dict[number]].destroy()
        globals()[self.remove_line_Dict[number]].destroy()
        globals()[self.project_name_Dict[number]].destroy()
        globals()[self.project_date_Dict[number]].destroy()
        globals()[self.check_mira_Dict[number]].destroy()
        globals()[self.check_GX[number]].destroy()
        globals()[self.calendar_Dict[number]].destroy()
        globals()[self.survey_time_start[number]].destroy()
        globals()[self.survey_time_stop[number]].destroy()
        globals()[self.comment[number]].destroy()

        del globals()[self.mira_proj_Dict[number]]
        del globals()[self.antenna_points_Dict[number]]
        del globals()[self.netCDF_Dict[number]]
        del globals()[self.survey_label_Dict[number]]
        del globals()[self.def_netCDF_Dict[number]]
        del globals()[self.def_antenna_points_Dict[number]]
        del globals()[self.remove_line_Dict[number]]
        del globals()[self.project_name_Dict[number]]
        del globals()[self.project_date_Dict[number]]
        del globals()[self.check_GX[number]]
        del globals()[self.check_mira_Dict[number]]
        del globals()[self.calendar_Dict[number]]
        del globals()[self.survey_time_stop[number]]
        del globals()[self.survey_time_start[number]]
        del globals()[self.comment[number]]

        self.total_lines = self.total_lines - 1

    def add_button(self):
        self.button_add = Button(self.input_frame, text='+', font=('Arial', 14, 'bold'), command=self.add_input_line)
        self.button_add.grid(row=self.number_of_lines + 3, column=0)
        self.button_validate = Button(self.input_frame, text='Validate entries', width=15, command=self.validate_entries)
        self.button_validate.grid(row=self.number_of_lines + 3, column=1)
        self.placeholder = Frame(self.input_frame, width=75)
        self.placeholder.grid(row=self.number_of_lines + 3, column=2)
        self.placeholder.grid_propagate()
        self.button_check_depthslices = Button(self.input_frame, text='Check depthsslices', command=self.check_depthslices)
        self.button_check_depthslices.grid(row=self.number_of_lines + 4, column=1)
        self.button_check_shp = Button(self.input_frame, text='Check shp files', command=self.check_shpfiles)
        self.button_check_shp.grid(row=self.number_of_lines + 5, column=1)
        self.placeholder1 = Frame(self.input_frame, width=50)
        self.placeholder1.grid(row=self.number_of_lines + 3, column=4)
        self.placeholder1.grid_propagate()
        self.placeholder2 = Frame(self.input_frame, width=75)
        self.placeholder2.grid(row=self.number_of_lines + 3, column=14)
        self.placeholder2.grid_propagate()
        self.exit_butt = Button(self.input_frame, text='Exit', command=self.exit)
        self.exit_butt.grid(row=self.number_of_lines + 4, column=2)

    def top_line(self):
        self.title = StringVar()
        self.title.set('Project name: ')
        self.project_name = Label(self.top_frame, width=50, textvariable=self.title, font=('Arial', 12, 'bold')).grid(row=1, column=0, columnspan=3, sticky=W)
        self.top_pr_nr = Label(self.title_frame, text='Nr', width=2).place(anchor=NW, x=5, y=0)
        self.top_pr_name = Label(self.title_frame, text='Name', width=4).place(anchor=NW, x=50, y=0)
        self.top_pr_date = Label(self.title_frame, text='Surveydate           time start and stop', width=30).place(anchor=NW, x=150, y=0)
        self.top_netcdf = Label(self.title_frame, text='NetCDF File', width=11).place(anchor=NW, x=520, y=0)
        self.top_shapefile = Label(self.title_frame, text='Antenna points', width=14).place(anchor=NW, x=920, y=0)
        self.top_mira_proj = Label(self.title_frame, text='GPR raw data', width=12).place(anchor=NW, x=1300, y=0)
        self.top_GX_or_mira = Label(self.title_frame, text='GX / MIRA', width=9).place(anchor=NW, x=355, y=0)

    def which_button(self, button_press):
        self.button_pressed = button_press
        self.button_nr = int(button_press[- (len(button_press)-int(button_press.rfind('_')) - 1):])
        self.button_name = button_press[:- (len(button_press)-int(button_press.rfind('_')))]

        if self.button_name == 'self.def_netCDF':
           self.ask_NetCDF()
        elif self.button_name == 'self.def_antenna_points':
            self.ask_shp()
        elif self.button_name == 'self.def_mira_proj':
            self.ask_GPR_proj()
        elif self.button_name =='self.calendar_Dict':
            self.date_from_cal()
        elif self.button_name =='comment':
            return self.button_name, self.button_nr

    def which_checkbutton(self, checkbutton):
        self.checkbutton_nr = int(checkbutton[- (len(checkbutton)-int(checkbutton.rfind('_')) - 1):])
        self.checkbutton_name = checkbutton[:- (len(checkbutton)-int(checkbutton.rfind('_')))]

        if self.checkbutton_name == 'self.check_GX':
            globals()[self.checkvar1[self.checkbutton_nr]].set(1)
            globals()[self.checkvar2[self.checkbutton_nr]].set(0)
        elif self.checkbutton_name == 'self.check_mira':
            globals()[self.checkvar2[self.checkbutton_nr]].set(1)
            globals()[self.checkvar1[self.checkbutton_nr]].set(0)

    def ask_NetCDF(self):
        NetCDF = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=[("NetCDF file", "*.nc")], parent=root_2_vemop)
        if NetCDF:
            globals()[self.netCDF_Dict[self.button_nr]].delete('1.0', END)
            globals()[self.netCDF_Dict[self.button_nr]].insert(INSERT, NetCDF)

    def ask_shp(self):
        shp = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=[("shapefile", "*.shp")], parent=root_2_vemop)
        if shp:
            globals()[self.antenna_points_Dict[self.button_nr]].delete('1.0', END)
            globals()[self.antenna_points_Dict[self.button_nr]].insert(INSERT, shp)

    def ask_GPR_proj(self):
         mira_proj = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=[("mira project file", "*.mira"), ('mala rd3', '*.rd3'), ('mala rd7', '*.rd7')], parent=root_2_vemop)
         if mira_proj:
             globals()[self.mira_proj_Dict[self.button_nr]].delete('1.0', END)
             globals()[self.mira_proj_Dict[self.button_nr]].insert(INSERT, mira_proj)

    def date_from_cal(self):
        self.popup_cal = tk.Toplevel()
        self.popup_cal.attributes('-topmost', True)
        self.popup_cal.title('Choose date')
        self.popup_cal.iconbitmap('Gjellestad.ico')
        self.cal = Calendar(self.popup_cal,font="Arial 14", selectmode='day',cursor="hand2", year=2021, month=1, day=2)
        self.cal.grid()
        self.submit = Button(self.popup_cal, text="ok", command=lambda: [self.submit_date(), self.popup_cal.destroy()]).grid()

    def submit_date(self):
        globals()[self.project_date_Dict[self.button_nr]].delete(0, 'end')
        globals()[self.project_date_Dict[self.button_nr]].insert(INSERT, self.cal.selection_get())

    def save_project(self):
        project_name = filedialog.asksaveasfilename(initialdir='/', title='Save VEMOP project', defaultextension='.vemop', filetypes=[('VEMOP project file', '*.vemop')], parent=root_2_vemop)
        name = project_name[project_name.rfind('/') + 1:][:-6]
        self.title.set('Project name: %s' % name)

        if project_name:
            f = open(project_name, 'w')
            count = 1

            for i in range(1, self.number_of_lines):
                try:
                    name = globals()[self.project_name_Dict[i]].get().strip()
                    date = globals()[self.project_date_Dict[i]].get().strip()
                    check_Gx = globals()[self.checkvar1[i]].get()
                    check_mira = globals()[self.checkvar2[i]].get()
                    netcdf = globals()[self.netCDF_Dict[i]].get('1.0', END).strip()
                    antenna_points = globals()[self.antenna_points_Dict[i]].get('1.0', END).strip()
                    mira_proj = globals()[self.mira_proj_Dict[i]].get('1.0', END).strip()
                    if i in self.comment_lst:
                        comment= str(self.comment_text_lst[self.comment_lst.index(i)])
                        formatted_comm = comment.replace('\n', r'\\n')
                    else:
                        formatted_comm =''

                    start_time = globals()[self.survey_time_start[i]].get().strip()
                    stop_time = globals()[self.survey_time_stop[i]].get().strip()
                    f.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (count, name, date, start_time, stop_time, check_Gx, check_mira, netcdf, antenna_points, mira_proj, formatted_comm))
                    count = count+1
                except KeyError:
                    'nix'

            f.close()

    def open_project(self):

        def file_len(project_name):
            with open(project_name) as f:
                for i, l in enumerate(f):
                    pass
            return i + 1

        project_name = filedialog.askopenfilename(initialdir='/', title='Open VEMOP project', filetypes=[('VEMOP project file', '*.vemop')], parent=root_2_vemop)
        file = open(project_name)

        if project_name:
            self.new()
            num_entries = file_len(project_name)
            for i in range(25):
                try:
                    self.remove_input_line(i)
                except:
                    'nix'
            self.number_of_lines = 1

            for i in range(num_entries):
                self.add_input_line()

            for line in file.readlines():
                single_line = line.rsplit(',')
                line_nr = int(single_line[0])

                globals()[self.project_name_Dict[line_nr]].insert(INSERT, single_line[1])
                globals()[self.project_date_Dict[line_nr]].insert(INSERT, single_line[2])
                globals()[self.survey_time_start[line_nr]].insert(INSERT, single_line[3])
                globals()[self.survey_time_stop[line_nr]].insert(INSERT, single_line[4])
                globals()[self.checkvar1[line_nr]].set(int(single_line[5]))
                globals()[self.checkvar2[line_nr]].set(int(single_line[6]))
                globals()[self.netCDF_Dict[line_nr]].insert(INSERT, single_line[7])
                globals()[self.antenna_points_Dict[line_nr]].insert(INSERT, single_line[8])
                globals()[self.mira_proj_Dict[line_nr]].insert(INSERT, single_line[9])
                self.comment_lst.append(line_nr)
                try:
                    comm = line[find_nth(line, ',', 10) + 1:]
                    formatted_comm = comm.rstrip().replace(r'\\n', '\n')
                    self.comment_text_lst.append(formatted_comm)
                except ValueError:
                    'nix'

        name = project_name[project_name.rfind('/') + 1:][:-6]
        self.title.set('Project name: %s' % name)

    def new(self):
        self.main_frame.destroy()
        self.top_frame.destroy()
        self.title_frame.destroy()
        self.number_of_lines = 1
        self.create_frame()
        self.top_line()
        self.add_input_line()
        self.comment_lst.clear()
        self.comment_text_lst.clear()

    def exit(self):
        root_2_vemop.quit()
        root_2_vemop.destroy()

    def number_of_entries(self):
        list_labels = []
        for i in range (1, 25):
            try:
                if globals()[self.netCDF_Dict[i]]:
                    list_labels.append(i)
            except KeyError:
                'nix'
        print(list_labels)
        return list_labels

    def validate_entries(self):
        self.valid_netcdf = []
        self.valid_shp = []
        for i in self.number_of_entries():
            netCDF = globals()[self.netCDF_Dict[i]].get('1.0', END).strip()
            antenna_points = globals()[self.antenna_points_Dict[i]].get('1.0', END).strip()
            mira_proj = globals()[self.mira_proj_Dict[i]].get('1.0', END).strip()
            name = globals()[self.project_name_Dict[i]].get().strip()
            date = globals()[self.project_date_Dict[i]].get().strip()
            start_time = globals()[self.survey_time_start[i]].get().strip()
            stop_time = globals()[self.survey_time_stop[i]].get().strip()
            format_time = '%H:%M'

            if not os.path.isfile(netCDF):
                globals()[self.netCDF_Dict[i]].config(bg="light salmon")
                globals()[self.netCDF_Dict[i]].delete('1.0', END)
                globals()[self.netCDF_Dict[i]].insert(INSERT, 'Not a valid file')
            else:
                globals()[self.netCDF_Dict[i]].config(bg="light green")
                self.valid_netcdf.append(netCDF)
                self.valid_netcdf.append(i)

            if not os.path.isfile(antenna_points):
                globals()[self.antenna_points_Dict[i]].config(bg="light salmon")
                globals()[self.antenna_points_Dict[i]].delete('1.0', END)
                globals()[self.antenna_points_Dict[i]].insert(INSERT, 'Not a valid file')
            else:
                globals()[self.antenna_points_Dict[i]].config(bg="light green")
                self.valid_shp.append(antenna_points)
                self.valid_shp.append(i)

            if not os.path.isfile(mira_proj):
                globals()[self.mira_proj_Dict[i]].config(bg="light salmon")
                globals()[self.mira_proj_Dict[i]].delete('1.0', END)
                globals()[self.mira_proj_Dict[i]].insert(INSERT, 'Not a valid file')
            else:
                globals()[self.mira_proj_Dict[i]].config(bg="light green")

            if not name:
                globals()[self.project_name_Dict[i]].config(bg='light salmon')
                globals()[self.project_name_Dict[i]].insert(INSERT, 'Enter name')
            elif name == 'Enter name':
                globals()[self.project_name_Dict[i]].config(bg='light salmon')
            else:
                globals()[self.project_name_Dict[i]].config(bg='light green')

            if not date:
                globals()[self.project_date_Dict[i]].config(bg='light salmon')
            elif date:
                format = '%Y-%m-%d'
                try:
                    datetime.datetime.strptime(date, format)
                    globals()[self.project_date_Dict[i]].config(bg='light green')
                except ValueError:
                    globals()[self.project_date_Dict[i]].config(bg='light salmon')

            if not start_time:
                globals()[self.survey_time_start[i]].config(bg='light salmon')
            elif start_time:
                try:
                    datetime.datetime.strptime(start_time, format_time)
                    globals()[self.survey_time_start[i]].config(bg='light green')
                except ValueError:
                    globals()[self.survey_time_start[i]].config(bg='light salmon')

            if not stop_time:
                globals()[self.survey_time_stop[i]].config(bg='light salmon')
            elif start_time:
                try:
                    datetime.datetime.strptime(stop_time, format_time)
                    globals()[self.survey_time_stop[i]].config(bg='light green')
                except ValueError:
                    globals()[self.survey_time_stop[i]].config(bg='light salmon')
            try:
                if datetime.datetime.strptime(start_time, format_time) < datetime.datetime.strptime(stop_time, format_time):
                    globals()[self.survey_time_stop[i]].config(bg='light green')
                    globals()[self.survey_time_start[i]].config(bg='light green')
                elif datetime.datetime.strptime(start_time, format_time) > datetime.datetime.strptime(stop_time, format_time):
                    globals()[self.survey_time_stop[i]].config(bg='light salmon')
                    globals()[self.survey_time_start[i]].config(bg='light salmon')
            except ValueError:
                globals()[self.survey_time_stop[i]].config(bg='light salmon')
                globals()[self.survey_time_start[i]].config(bg='light salmon')

        return self.valid_netcdf, self.valid_shp

    def check_depthslices(self):
        self.existing_depthslices = []
        self.missing_depthslices = []
        for i in self.validate_entries()[0][::2]:
            print(i)
            line_nr = self.validate_entries()[0].index(i) + 1

            folder = i.rsplit('/', 1)[0]
            filename = i.rsplit('/', 1)[1].rsplit('.', 1)[0]
            #folder_new = folder + '/05cm'
            #file = folder_new + filename + '_000-005.tif'
            #folder_new2 = folder + '/depth_slices_' + filename
            #file2 = folder_new2 + '/' + filename + '_000_005.jpg'
            #file4 = folder_new2 + '/' + filename + '_0000_0005.jpg'
            folder_new3 = folder + '/NetCDF_img_' + filename
            print(folder_new3)
            file3 = folder_new3 + '/' + filename + '_000_005.jpg'
            file5 = folder_new3 + '/' + filename + '_0000_0005.jpg'

            #if path.exists(folder_new):
            #    if path.exists(file):
            #        self.existing_depthslices.append(folder_new)
            #    else:
            #        self.missing_depthslices.append(folder + '/' + filename)
            #        self.missing_depthslices.append(self.validate_entries()[0][line_nr])

            #elif path.exists(folder_new2):
            #    if path.exists(file2) or path.exists(file4):
            #        self.existing_depthslices.append(folder_new2)

            #    else:
            #        self.missing_depthslices.append(folder + '/' + filename)
            #        self.missing_depthslices.append(self.validate_entries()[0][line_nr])

            if path.exists(folder_new3):
                print('teeet')
                if path.exists(file3) or path.exists(file5):
                    self.existing_depthslices.append(folder_new3)

                else:
                    print('nooooo')
                    self.missing_depthslices.append(folder + '/' + filename)
                    self.missing_depthslices.append(self.validate_entries()[0][line_nr])

            else:
                self.missing_depthslices.append(folder + '/' + filename)
                self.missing_depthslices.append(self.validate_entries()[0][line_nr])
        self.depthslice_info()

    def check_shpfiles(self):
        self.existing_npy_kd = []
        self.missing_npy_kd = []
        self.missing_npy_kd_number = []
        for i in self.validate_entries()[1][::2]:
            line_nr = self.validate_entries()[1].index(i) + 1
            name = i.rsplit('.', 1)[0]
            npy = name + '.npy'
            kd = name + '.pickle'

            print(kd)
            if path.exists(npy):
                self.existing_npy_kd.append(npy)
            else:
                self.missing_npy_kd.append(i)
                self.missing_npy_kd_number.append(line_nr)

            print(self.missing_npy_kd)

            #if path.exists(kd):
            #    self.existing_npy_kd.append(kd)
            #else:
            #    self.missing_npy_kd.append(i)

        self.shp_info()

    def depthslice_info(self):
        self.popup_info = tk.Toplevel()
        self.popup_info.title('Missing depthslices found')
        self.popup_info.iconbitmap('Gjellestad.ico')
        self.popup_info.geometry('400x300')
        self.popup_info.attributes('-topmost', True)

        self.missing_ds = Text(self.popup_info, width=600, height=10, bg='light grey')
        self.missing_ds.pack()
        for i in self.missing_depthslices[1::2]:
            self.missing_ds.insert(INSERT, 'No depthslices found for entry in Line %s' % (i))
            self.missing_ds.insert(INSERT, '\n' )
            self.missing_ds.insert(INSERT, self.missing_depthslices[self.missing_depthslices.index(i) - 1])
            self.missing_ds.insert(INSERT, '\n \n')

        if self.missing_depthslices:
            self.button_create_depthslices = Button(self.popup_info, text='Create missing depthslices',
                                                    command=self.create_depthslices)
            self.button_create_depthslices.pack()
            self.ok_button = Button(self.popup_info, text='OK', command=self.close_popup)
            self.ok_button.pack()

        elif not self.missing_depthslices:
            self.missing_ds.insert(INSERT, 'All depthslices found')
            self.ok_button = Button(self.popup_info, text='OK', command=self.close_popup)
            self.ok_button.pack()

    def shp_info(self):
        self.popup_shp = tk.Toplevel()
        self.popup_shp.title('Shapefile preprocessing')
        self.popup_shp.iconbitmap('Gjellestad.ico')
        self.popup_shp.geometry('400x300')
        self.popup_shp.attributes('-topmost', True)

        self.missing_npy_kd_text = Text(self.popup_shp, width=600, height=10, bg='light grey')
        self.missing_npy_kd_text.pack()

        for i in range(0, len(self.missing_npy_kd_number)):
            self.missing_npy_kd_text.insert(INSERT, 'Shapefile not preprocessed for entry in Line %s' % self.missing_npy_kd_number[i])
            self.missing_npy_kd_text.insert(INSERT, '\n' )
            self.missing_npy_kd_text.insert(INSERT, self.missing_npy_kd[i])
            self.missing_npy_kd_text.insert(INSERT, '\n \n')

        if self.missing_npy_kd:
            self.button_preprocess_shp = Button(self.popup_shp, text='Preprocess shapefiles',
                                                    command=self.preprocess_shp)
            self.button_preprocess_shp.pack()
            self.ok_button = Button(self.popup_shp, text='OK', command=self.close_popup)
            self.ok_button.pack()

        elif not self.missing_npy_kd:
            self.missing_npy_kd_text.insert(INSERT, 'All shapefiles preprocessed')
            self.ok_button = Button(self.popup_shp, text='OK', command=self.close_popup)
            self.ok_button.pack()

    def preprocess_shp(self):
        print(len(self.missing_npy_kd))
        self.progress = Progressbar(self.popup_shp, orient='horizontal', length=len(self.missing_npy_kd), mode='determinate')
        self.progress.pack()
        self.progress['value'] += 0

        for i in self.missing_npy_kd:
            print(i)
            shp_tools.shp_to_np_kdtree(datasource=i)
            self.progress['value'] += 1

            self.missing_npy_kd_text.insert(INSERT, 'Shapefiles preprocessed for %s created \n' % i)

        self.missing_npy_kd_text.insert(INSERT, 'Finished')

    def add_comment(self, button_pressed):
        try:
            self.comment_win.destroy()
        except:
            'nex'

        self.button_pressed_comm = button_pressed
        self.button_comm_nr = int(button_pressed[- (len(button_pressed) - int(button_pressed.rfind('_')) - 1):])

        self.comment_win = tk.Toplevel()
        self.comment_win.title('Add comment')
        self.comment_win.iconbitmap('Gjellestad.ico')
        self.comment_win.geometry('400x430')
        self.comment_win.attributes('-topmost', True)

        self.comment_frame = Frame(self.comment_win)
        self.comment_frame.pack(fill=BOTH, expand=1)

        self.comment_label = Label(self.comment_frame, height=1, text='Enter comment below:', font=('Arial', 10))
        self.comment_label.pack()
        self.comment_label.pack_propagate(0)

        self.comment_text = Text(self.comment_frame, height=22)
        self.comment_text.pack()

        self.save_comment_but = Button(self.comment_frame, text='Save comment', command=self.save_comment)
        self.save_comment_but.pack()

        self.exit_comm = Button(self.comment_frame, text='Exit', command=self.comment_win.destroy)
        self.exit_comm.pack()

        try:
            if self.button_comm_nr in self.comment_lst:
                comm_ind = self.comment_lst.index(self.button_comm_nr)
                self.comment_text.delete('1.0', END)
                formatted_comm = self.comment_text_lst[comm_ind].rstrip().replace(r'\\n', '\n')
                self.comment_text.insert(INSERT, formatted_comm)
        except:
            'nis'

    def save_comment(self):
        if self.button_comm_nr in self.comment_lst:
            nr_remove = self.comment_lst.index(self.button_comm_nr)
            self.comment_lst.pop(nr_remove)
            self.comment_text_lst.pop(nr_remove)

        if not self.comment_text.get('1.0', END) == 1:
            self.comment_lst.append(self.button_comm_nr)
            comm = str(self.comment_text.get('1.0', END))
            formatted = comm.replace('\n', r'\\n')
            self.comment_text_lst.append(formatted.rstrip(r'\\n'))

    def close_popup(self):
        try:
            self.popup_info.destroy()
        except AttributeError:
            'nix'

        try:
            self.popup_shp.destroy()
        except AttributeError:
            'nix'

    def create_depthslices(self):
        self.progress = Progressbar(self.popup_info, orient='horizontal', length=100, mode='determinate')
        self.progress.pack()
        self.progress['value'] += 0
        vmin = 2
        vmax = 24
        depth_range_top = 0

        for i in self.missing_depthslices[::2]:
            self.progress['value'] = 0
            self.working_directory = i.rsplit('/', 1)[0]
            os.chdir(self.working_directory)
            nc_noExt = i.rsplit('/', 1)[1].rsplit('.', 1)[0]
            NetCDF_GPR = nc_noExt + '.nc'

            nc_ds = nc.Dataset(NetCDF_GPR)
            self.xpixels = nc_ds.dimensions['x'].size
            self.ypixels = nc_ds.dimensions['y'].size
            self.zpixels = nc_ds.dimensions['z'].size

            dset = xr.open_dataset(NetCDF_GPR)
            gpr = dset.gpr

            x_temp = str(dset.gpr['x'][0])
            x_temp2 = x_temp.rsplit('\n')[1]
            self.x_coor = float(x_temp2.strip('array(').strip(')'))
            x_temp3 = str(dset.gpr['x'][1])
            x_temp4 = x_temp3.rsplit('\n')[1]
            x_coor2 = float(x_temp4.strip('array(').strip(')'))
            self.pixelsize = round(abs(self.x_coor - x_coor2), 2)

            y_temp = str(dset.gpr['y'][0])
            y_temp2 = y_temp.rsplit('\n')[1]
            self.y_coor = y_temp2.strip('array(').strip(')')

            for i in range(depth_range_top, self.zpixels):

                fig = plt.figure(figsize=(self.xpixels / 100, self.ypixels / 100))
                fig.figimage(gpr.isel(z=i), cmap='Greys', origin='lower', vmin=vmin, vmax=vmax,
                            interpolation='bilinear', resample=False)

                upper = '{0:0=4d}'.format(5 * i)
                lower = '{0:0=4d}'.format(5 * i + 5)
                try:
                    os.chdir(self.working_directory)
                    os.makedirs('NetCDF_img_%s' % nc_noExt)
                    os.chdir(self.working_directory + '/NetCDF_img_%s' % nc_noExt)
                except FileExistsError:
                    os.chdir(self.working_directory + '/NetCDF_img_%s' % nc_noExt)

                newname = nc_noExt + "_" + upper + "_" + lower + '.jpg'
                plt.savefig(newname, quality=100)
                plt.close()
                root_2_vemop.update_idletasks()
                prog = 100/self.zpixels
                self.progress['value'] += prog

            self.missing_ds.insert(INSERT, 'Depthsslices for %s created \n' % NetCDF_GPR)

        self.missing_ds.insert(INSERT, 'Finished')

    def _on_mousewheel(self, event):
        self.input_Canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def exit():
    root_2_vemop.destroy()

def start_define_vemop():
    width = GetSystemMetrics(0)
    os.chdir(str(__file__).rsplit('\\', 1)[0])

    global root_2_vemop
    root_2_vemop = Toplevel()
    root_2_vemop.title('Define VEMOP project')
    root_2_vemop.geometry('%sx390+-7+-4' % width)
    root_2_vemop.iconbitmap('Gjellestad.ico')
    root_2_vemop.protocol('WM_DELETE_WINDOW', exit)
    root_2_vemop.resizable(False, False)
    root_2_vemop.attributes('-topmost', True)
    
    app = DefineVEMOP(root_2_vemop)
    app.mainloop()

#start_define_vemop()
