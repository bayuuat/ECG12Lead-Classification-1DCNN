import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path

import matplotlib.pyplot as plt
#from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import serial.tools.list_ports

import re
#import csv
import threading
import time
from datetime import datetime
import pandas as pd

import csv
import json
#from typing import Counter
import requests
import numpy as np
from scipy import stats
import tensorflow as tf
from tensorflow import keras


class RootGUI():
    def __init__(self, serial):
        self.root = tk.Tk()
        self.root.title("Aplikasi Rekam Jantung")
        # self.root.geometry("4x600")
        self.root.attributes('-fullscreen', True)
        self.root.config(bg="white")

        self.serial = serial

        self.container = tk.Frame(self.root, bg="white", padx=5, pady=5)
        self.container.pack()

        self.label_header = tk.Label(
            self.container, text="Aplikasi Rekam Jantung", bg="white")
        self.label_header.config(font=("TkDefaultFont", 14, "bold"))
        self.label_header.grid(row=0, column=0, pady=10,
                               columnspan=7)

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        print("Closing the window and exit")
        self.root.destroy()
        try:
            self.serial.SerialClose(self)
        except:
            pass
        self.serial.threading = False


class ComGUI():
    def __init__(self, root, serial, data):
        '''
        Initialize the connexion GUI and initialize the main widgets
        '''
        # Initializing the Widgets
        self.root = root
        self.serial = serial
        self.data = data

        self.frame = tk.LabelFrame(
            root, text="Record Manager", bg="white", padx=10, pady=10)
        self.label_com = tk.Label(
            self.frame, text="Port  : ", bg="white", width=10, anchor="w")
        self.label_dur = tk.Label(
            self.frame, text="Duration  : ", bg="white", width=10, anchor="w")

        # Setup the Drop option menu
        self.baudOptionMenu()
        self.comOptionMenu()
        self.durationOptionMenu()
        self.checkMenu()

        # Add the control buttons for refreshing the COMs & Connect
        self.btn_reset = tk.Button(self.frame, text="Reset",
                                   width=5, command=self.com_reset)
        self.btn_connect = tk.Button(self.frame, text="Connect",
                                     width=5, state="disable",
                                     command=self.serial_connect)

        # Put on the grid all the elements
        self.GUIOpen()

    def GUIOpen(self):
        '''
         Method to display all the Widget of the main frame
        '''

        self.frame.grid(row=1, column=4, rowspan=2,
                        columnspan=4)
        self.label_com.grid(column=0, row=0, pady=(0, 5))
        self.label_dur.grid(column=0, row=1)

        self.drop_com.grid(column=1, row=0, pady=(0, 5))
        self.drop_baud.grid(column=2, row=0, padx=5, pady=(0, 5))
        self.drop_dur.grid(column=1, row=1)
        self.save_check.grid(column=2, row=1)

        self.btn_reset.grid(column=3, row=0, pady=(0, 5))
        self.btn_connect.grid(column=3, row=1, pady=(0, 5))

    def comOptionMenu(self):
        '''
         Method to Get the available COMs connected to the PC
         and list them into the drop menu
        '''
        # Generate the list of available coms
        self.serial.getCOMList()

        self.clicked_com = tk.StringVar()
        self.clicked_com.set("Select Port")
        self.drop_com = tk.OptionMenu(
            self.frame, self.clicked_com, *self.serial.com_list,
            command=self.connect_ctrl)
        self.drop_com.config(width=10)

    def baudOptionMenu(self):
        '''
         Method to list all the baud rates in a drop menu
        '''
        self.clicked_bd = tk.StringVar()
        bds = ["9600",
               "115200",
               "256000"]
        self.clicked_bd.set("Select Baudrate")
        # self.clicked_bd.trace("w",self.clicked_bd.get())
        self.drop_baud = tk.OptionMenu(
            self.frame, self.clicked_bd, *bds,
            command=self.connect_ctrl)
        self.drop_baud.config(width=10)

    def durationOptionMenu(self):
        '''
         Method to list all the duration in a drop menu
        '''

        self.clicked_dur = tk.StringVar()
        # self.clicked_com.set(self.serial.com_list[0])
        dur = ["10 Seconds", "20 Seconds", "30 Seconds", "1 Minute",
               "2 Minutes", "5 Minutes", "10 Minutes", "15 Minutes"]
        self.clicked_dur.set("Select Duration")
        # self.clicked_dur.trace("w",self.clicked_dur.get())
        self.drop_dur = tk.OptionMenu(
            self.frame, self.clicked_dur, *dur,
            command=self.connect_ctrl)
        self.drop_dur.config(width=10)

    def checkMenu(self):
        self.save = False
        self.SaveVar = tk.IntVar()
        self.save_check = tk.Checkbutton(self.frame, text="Save and Upload Data", variable=self.SaveVar,
                                         onvalue=1, offvalue=0, bg="white", state="disable",
                                         command=self.connect_ctrl)

    def connect_ctrl(self, *args):
        '''
        Mehtod to keep the connect button disabled if all the
        conditions are not cleared
        '''
        print("===Connect ctrl===")
        # Checking the logic consistency to keep the connection btn
        if ("Select Baudrate" in self.clicked_bd.get()
                or "-" in self.clicked_com.get()
                or "Select Duration" in self.clicked_dur.get()
                or "Select Port" in self.clicked_com.get()):

            self.btn_connect["state"] = "disabled"
            self.save_check["state"] = "disable"
            self.SaveVar.set(0)

        else:
            if (len(self.data.user_webid) > 0):
                self.save_check["state"] = "active"
            else:
                self.save_check["state"] = "disable"
                self.SaveVar.set(0)
            self.btn_connect["state"] = "active"
        print("PORT: " + self.clicked_com.get())
        print("BAUDRATE: " + self.clicked_bd.get())
        print("DURATION: " + self.clicked_dur.get())
        print("Save Data: " + str(self.SaveVar.get()))

    def com_reset(self):
        print("===Resetting===")
        # Get the Widget destroyed
        self.drop_com.destroy()
        self.drop_baud.destroy()
        self.drop_dur.destroy()

        # Refresh the list of available Coms
        self.comOptionMenu()
        self.baudOptionMenu()
        self.durationOptionMenu()

        # Open the this new droplet
        self.drop_com.grid(column=1, row=0, pady=(0, 5))
        self.drop_baud.grid(column=2, row=0, padx=10, pady=(0, 5))
        self.drop_dur.grid(column=1, row=1)

        # Just in case to secure the connect logic
        logic = []
        self.connect_ctrl(logic)

    def serial_connect(self):
        '''
        Method that Updates the GUI during connect / disconnect status
        Manage serials and data flows during connect / disconnect status
        '''

        if self.btn_connect["text"] in "Connect":
            # Start the serial communication
            self.serial.SerialOpen(self)

            # If connection established move on
            if self.serial.ser.status:
                # Update the COM manager
                self.btn_connect["text"] = "Disconnect"
                self.save_check["state"] = "disable"
                self.btn_reset["state"] = "disable"
                self.drop_baud["state"] = "disable"
                self.drop_dur["state"] = "disable"
                self.drop_com["state"] = "disable"
                UserMaster.btn_update["state"] = "disable"
                UserMaster.drop_user["state"] = "disable"
                UserMaster.btn_submit["state"] = "disable"

                get_duration = self.clicked_dur.get()
                get_duration = get_duration.split(" ")
                if "Minute" in get_duration[1] or "Minutes" in get_duration[1]:
                    get_duration[0] = int(get_duration[0]) * 60
                self.data.period_time = int(get_duration[0])

                # InfoMsg = f"Successful UART connection using {self.clicked_com.get()}"
                # messagebox.showinfo("showinfo", InfoMsg)

                # Display the channel manager
                # self.conn = ConnGUI(self.root, self.serial, self.data)
                #
                self.serial.t1 = threading.Thread(
                    target=self.serial.SerialDataStream, args=(self,))
                # self.serial.t2 = threading.Thread(
                #     target=PlotMaster.UpdateChart(), args=(self,))
                self.serial.t1.start()
                PlotMaster.UpdateChart()

            else:
                self.errorMsg()
        else:
            self.completeMsg()

    def completeMsg(self):
        self.serial.threading = False
        self.serial.SerialClose()
        DetectionGUI(self.root, self.serial, self.data)
        saving_gui = SavingGUI(self.root, self.serial, self.data)
        self.data.SaveDataforClassify(saving_gui)
        saving_gui.close()

        if self.SaveVar.get() > 0:
            saving_gui = SavingGUI(self.root, self.serial, self.data)
            awal = time.time()
            self.data.SaveData(saving_gui)
            akhir = time.time()
            print("time save = ", akhir-awal)
            saving_gui.uploadGUI()
            self.data.send_json()
            saving_gui.close()
            # self.SaveVar.set(0)

        self.data.ClearData()
        PlotMaster.kill_chart()

        # InfoMsg = f"UART connection using {self.clicked_com.get()} is now closed"
        # messagebox.showwarning("showinfo", InfoMsg)
        self.btn_connect["text"] = "Connect"
        self.btn_connect["state"] = "active"
        self.btn_reset["state"] = "active"
        self.drop_baud["state"] = "active"
        self.drop_dur["state"] = "active"
        self.drop_com["state"] = "active"

        if UserMaster.btn_submit["text"] == "Submit":
            UserMaster.btn_update["state"] = "active"
            UserMaster.drop_user["state"] = "active"
        else:
            UserMaster.btn_submit["state"] = "active"

    def errorMsg(self):
        self.serial.threading = False
        self.serial.SerialClose()

        self.data.ClearData()
        PlotMaster.kill_chart()

        ErrorMsg = f"Failure to estabish UART connection using {self.clicked_com.get()} "
        messagebox.showerror("showerror", ErrorMsg)
        self.btn_connect["text"] = "Connect"
        self.btn_connect["state"] = "active"
        self.btn_reset["state"] = "active"
        self.drop_baud["state"] = "active"
        self.drop_dur["state"] = "active"
        self.drop_com["state"] = "active"

        if UserMaster.btn_submit["text"] == "Submit":
            UserMaster.btn_update["state"] = "active"
            UserMaster.drop_user["state"] = "active"
        else:
            UserMaster.btn_submit["state"] = "active"


class UserGUI():
    def __init__(self, root, data, com):
        '''
        Initialize the connexion GUI and initialize the main widgets
        '''
        # Initializing the Widgets
        self.root = root
        self.data = data
        self.com = com

        self.opt_webid = []
        self.opt_id = []
        self.opt_name = []
        self.frame = tk.LabelFrame(
            root, text="User Menu", bg="white", padx=10, pady=10)
        self.label_user = tk.Label(
            self.frame, text="Patient ID  : ", bg="white", width=15, anchor="w")
        self.label_name = tk.Label(
            self.frame, text="Patient Name  :", bg="white", width=15, anchor="w")

        self.user_name = tk.Label(
            self.frame, text="[Null]", bg="white", width=15, anchor="w")

        # Setup the Drop option menu
        # self.baudOptionMenu()
        self.userOptionMenu()

        # Add the control buttons for refreshing the COMs & Connect
        self.btn_update = tk.Button(self.frame, text="Update",
                                    width=10, command=self.add_option)
        self.btn_submit = tk.Button(self.frame, text="Submit",
                                    width=10, state="disable",
                                    command=self.user_submit)

        # Put on the grid all the elements
        self.GUIOpen()

    def GUIOpen(self):
        '''
         Method to display all the Widget of the main frame
        '''

        self.frame.grid(row=1, column=0, rowspan=2,
                        columnspan=3)
        self.label_user.grid(column=0, row=0, pady=(0, 5))
        self.label_name.grid(column=0, row=1)

        self.drop_user.grid(column=1, row=0, padx=(5, 10), pady=(0, 5))
        self.user_name.grid(column=1, row=1, padx=(5, 10))

        self.btn_update.grid(column=2, row=0, pady=(0, 5))
        self.btn_submit.grid(column=2, row=1, pady=(0, 5))

    def userOptionMenu(self):

        self.get_opt_patient()

        self.clicked_user = tk.StringVar()
        self.clicked_user.set("Select Patient ID")
        self.drop_user = tk.OptionMenu(
            self.frame, self.clicked_user, *self.opt_id, command=self.user_ctrl)
        self.drop_user.config(width=15, anchor="w")

    def add_option(self):
        json = 'http://ecg.komputer-its.com/Data/alatGetDataPasien/c4ca4238a0b923820dcc509a6f75849b'
        df = pd.read_json(json, dtype={'NIK': str})
        # df.to_csv(r'/home/pi/EKG/person/pasien.txt', index=False)x
        df.to_csv(r'D:/EKG/person/pasien.txt', index=False)

        self.drop_user.destroy()

        self.user_name["text"] = "[Null]"

        self.userOptionMenu()

        self.drop_user.grid(column=1, row=0, padx=(5, 10), pady=(0, 5))

        logic = []
        self.user_ctrl(logic)

    def get_opt_patient(self):
        nameTmp = []
        idTmp = []
        id_webTmp = []
        # with open('/home/pi/EKG/person/pasien.txt', 'r') as f:
        with open('D:/EKG/person/pasien.txt', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                id_webTmp.append(row[1])
                idTmp.append(row[5])
                nameTmp.append(row[4])
            if (len(idTmp) > 0):
                id_webTmp.pop(0)
                idTmp.pop(0)
                nameTmp.pop(0)
            else:
                idTmp = "-"

        self.opt_webid = id_webTmp
        self.opt_id = idTmp
        self.opt_name = nameTmp

    def user_ctrl(self, *args):
        if ("-" in self.clicked_user.get() or
                "Select ID Patient" in self.clicked_user.get()):
            self.btn_submit["state"] = "disabled"
        else:
            self.btn_submit["state"] = "active"
            get_id = self.clicked_user.get()
            i = 0
            for _ in range(len(self.opt_id)):
                if (get_id == self.opt_id[i]):
                    self.var_pick = i
                    break
                i += 1
            self.user_name['text'] = self.opt_name[self.var_pick]

    def user_submit(self):
        if self.btn_submit["text"] in "Submit":
            self.data.user_webid = self.opt_webid[self.var_pick]
            if self.com.btn_connect["state"] == "active":
                self.com.save_check["state"] = "active"
            self.btn_update["state"] = "disable"
            self.drop_user["state"] = "disable"
            self.btn_submit["text"] = "Clear"

        else:
            self.data.user_webid = []
            self.com.SaveVar.set(0)
            self.com.save_check['state'] = "disable"
            self.btn_update["state"] = "active"
            self.drop_user["state"] = "active"
            self.btn_submit["text"] = "Submit"
            self.btn_submit["state"] = "active"


class PlotGUI():
    def __init__(self, root, serial, data):

        self.root = root
        self.serial = serial
        self.data = data

        self.frame = tk.LabelFrame(
            root, text="Plot Graph", bg="white", padx=5, pady=5)

        self.label_lead = tk.Label(
            self.frame, text="Lead  : ", bg="white", anchor="w", width=5)

        self.label_time = tk.Label(
            self.frame, text="Timeleft  : ", bg="white", anchor="w", width=10)

        self.label_timeleft = tk.Label(
            self.frame, text=str(self.data.period_time), bg="white", anchor="w", width=15)

        self.plotOptionMenu()

        self.init_graph()
        self.GraphOpen()

    def GraphOpen(self):
        self.frame.grid(row=3, column=0, padx=5, pady=5, columnspan=7)

        self.label_lead.grid(column=0, row=0)

        self.drop_plot.grid(column=1, row=0, sticky="w")

        self.label_time.grid(column=2, row=0, sticky="e")
        self.label_timeleft.grid(column=3, row=0, sticky="w")

    def plotOptionMenu(self):
        self.clicked_plot = tk.StringVar()
        self.plot = ["Lead I",
                     "Lead II",
                     "Lead III",
                     "Lead V1",
                     "Lead V2",
                     "Lead V3",
                     "Lead V4",
                     "Lead V5",
                     "Lead V6",
                     "Lead aVL",
                     "Lead aVR",
                     "Lead aVF", ]
        self.clicked_plot.set(self.plot[1])
        self.drop_plot = tk.OptionMenu(
            self.frame, self.clicked_plot, *self.plot, command=self.channel_ctrl)
        self.drop_plot.config(width=15, anchor="w")

    def channel_ctrl(self, *args):
        get_ch = self.clicked_plot.get()
        # print(get_ch)
        i = 0
        for _ in range(len(self.plot)):
            if (get_ch == self.plot[i]):
                self.data.ch_lead = i
            i += 1
        #self.data.data_plot = []
        self.kill_chart()
        # print(self.ch_lead)

    def init_graph(self):
        plt.style.use('ggplot')

        self.fig = plt.Figure(figsize=(10, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(1, 1, 1)

        self.ax1.set_xlim(0, self.data.DISPLAY_SIZE - 1)
        self.ax1.set_ylim([-2, 2])
        self.ax1.set_ylabel("Amplitude")
        self.ax1.set_xlabel("Sample")

        grid_x_ticks_major = np.arange(0, self.data.DISPLAY_SIZE - 1, 40)
        grid_x_ticks_minor = np.arange(0, self.data.DISPLAY_SIZE - 1, 8)
        grid_y_ticks_major = np.arange(-2, 2, 0.5)
        grid_y_ticks_minor = np.arange(-2, 2, 0.1)

        self.ax1.set_xticks(grid_x_ticks_minor, minor=True)
        self.ax1.set_xticks(grid_x_ticks_major)
        self.ax1.set_yticks(grid_y_ticks_minor, minor=True)
        self.ax1.set_yticks(grid_y_ticks_major)

        self.ax1.grid(which='both', color="white")

        self.ax1.grid(which='minor', alpha=0.5, linestyle='--')

        self.line1, = self.ax1.plot(self.data.data_plot, lw=1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(
            column=0, row=1, columnspan=7)

        self.canvas.draw()  # note that the first draw comes before setting data

        # cache the background
        self.axbackground = self.canvas.copy_from_bbox(self.ax1.bbox)

        plt.show(block=False)

        self.k = 0.

    def UpdateChart(self):
        try:
            # update here
            self.k += 0.11

            self.line1.set_ydata(self.data.data_plot)
            # restore background
            self.canvas.restore_region(self.axbackground)

            # redraw just the points
            self.ax1.draw_artist(self.line1)

            # fill in the axes rectangle
            self.canvas.blit(self.ax1.bbox)

            # in this post http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
            # it is mentionned that blit causes strong memory leakage.
            # however, I did not observe that.

            self.canvas.flush_events()

        except Exception as e:
            # print(type(self.data_plot))
            # print(type(self.line1))
            print("Plot Error: ", e)
        if self.serial.threading:
            self.label_timeleft['text'] = str(
                int(self.data.period_time - (self.data.read_time - self.data.start_time))) + " seconds left"

            self.root.after(1, self.UpdateChart)
        else:
            self.label_timeleft['text'] = "0"

    def kill_chart(self):
        for _ in self.data.data_plot:
            self.line1.set_ydata(self.data.data_plot)


class SavingGUI():
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data = data

        self.frame = tk.Toplevel(self.root)
        self.frame.title("Progress")
        # self.frame.geometry("320x240")

        screen_width = self.frame.winfo_screenwidth()
        screen_height = self.frame.winfo_screenheight()

        size = tuple(int(_)
                     for _ in self.frame.geometry().split('+')[0].split('x'))
        # print(size)
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2

        self.frame.geometry("+%d+%d" % (x, y))

        self.percent = tk.StringVar()

        self.bar = ttk.Progressbar(
            self.frame, orient="horizontal", length=300, mode='determinate')
        self.percentLabel = tk.Label(self.frame, textvariable=self.percent)

        #self.taskLabel = tk.Label(self.frame, textvariable=self.text)

        self.total = len(self.data.lead_1)

        self.open()

    def open(self):
        self.bar.pack(padx=10, pady=5)
        self.percentLabel.pack(padx=10, pady=5)
        # self.taskLabel.pack()

    def close(self):
        self.frame.destroy()

    def updateBar(self):
        self.saved = self.data.progres_var
        if self.saved % 10 == 0:
            self.bar['value'] = int((self.saved/self.total)*100)
            self.percent.set("Saving Percentage: " +
                             str(int((self.saved/self.total)*100))+"%")
            self.root.update_idletasks()

    def uploadGUI(self):
        self.bar.destroy()
        self.percentLabel.destroy()

        self.uploadLabel = tk.Label(
            self.frame, text="Uploading Data...", width=45, height=5)
        self.uploadLabel.pack()


class DetectionGUI():
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data = data

        self.frame = tk.Toplevel(self.root)
        self.frame.title("Arrhythmia Detection")
        # self.frame.geometry("320x240")

        screen_width = self.frame.winfo_screenwidth()
        screen_height = self.frame.winfo_screenheight()

        size = tuple(int(_)
                     for _ in self.frame.geometry().split('+')[0].split('x'))
        # print(size)
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2

        self.frame.geometry("+%d+%d" % (x, y))

        self.btn_save = tk.Button(self.frame, text="Save Only",
                                  width=45, command=self.saving)
        self.btn_detect = tk.Button(self.frame, text="Save & Classify",
                                    width=45, command=self.clasifyFrame)

        self.btn_classify = tk.Button(
            self.frame, text="Classify", width=45, command=self.clasify_new)
        self.btn_done = tk.Button(
            self.frame, text="Done", width=45, command=self.close)

        self.open()

    def open(self):
        self.btn_save.grid(row=0, padx=10, pady=10)
        self.btn_detect.grid(row=1, padx=10, pady=10)

    def close(self):
        self.frame.destroy()

    def saving(self):
        self.close()
        saving_gui = SavingGUI(self.root, self.serial, self.data)
        print(self)
        print(saving_gui)
        self.data.SaveData(saving_gui)
        saving_gui.uploadGUI()
        self.data.send_json()
        saving_gui.close()
        InfoMsg = f"Done Uploaded"
        messagebox.showinfo("Saving", InfoMsg)

    def layoutClassify(self, konten, percentase, column):
        label = self.framelabel = tk.Label(
            self.frame, text=konten, padx=10, pady=10, anchor="w",)
        percent = self.framepercent = tk.Label(
            self.frame, text=percentase, padx=10, pady=10, anchor="w")

        label.grid(row=0, column=column)
        percent.grid(row=1, column=column)
        return label, percent

    def clasifyFrame(self):
        self.btn_detect.destroy()
        self.btn_save.destroy()

        self.layoutClassify('Normal', ' - ', column=0)
        self.layoutClassify('PVC', ' - ', column=1)
        self.layoutClassify('APB', ' - ', column=2)
        self.layoutClassify('RBBB', ' - ', column=3)
        self.btn_classify.grid(row=3, padx=10, pady=10, columnspan=4)

    def clasify(self):
        self.btn_classify.destroy()
        self.layoutClassify('Normal', '100%', column=0)
        self.layoutClassify('PVC', '0%', column=1)
        self.layoutClassify('APB', '0%', column=2)
        self.layoutClassify('RBBB', '0%', column=3)
        self.btn_done.grid(row=3, padx=10, pady=10, columnspan=4)

    def clasify_new(self):
        def feature_normalize(dataset):
            mu = np.mean(dataset, axis=0)
            sigma = np.std(dataset, axis=0)
            return (dataset - mu)/sigma

        def create_segments_and_labels(df, time_steps, step):
            N_FEATURES = 1
            # Number of steps to advance in each iteration (for me, it should always
            # be equal to the time_steps in order to have no overlap between segments)
            # step = time_steps
            segments = []
            for i in range(0, len(df), step):
                xs = df['I'].values[i: i + time_steps]
                # Retrieve the most often used label in this segment
                segments.append([xs])

            # Bring the segments into a better shape
            reshaped_segments = np.asarray(
                segments, dtype=np.float32).reshape(-1, time_steps, N_FEATURES)
            return reshaped_segments

        df = pd.read_csv('data_alat_siap.csv', float_precision='round_trip')
        df_test = df[df['id'] < 99000]

        df_test['II'] = feature_normalize(df_test['II'])

        df_test = df_test.round({'II': 6})
        LABELS = ["N", "V", "R", "A", "F"]
        TIME_PERIODS = 80
        STEP_DISTANCE = 80

        x_test = create_segments_and_labels(df_test,
                                            TIME_PERIODS,
                                            STEP_DISTANCE,)

        num_time_periods, num_sensors = x_test.shape[1], x_test.shape[2]
        input_shape = (num_time_periods*num_sensors)
        x_test = x_test.reshape(x_test.shape[0], input_shape)

        x_test = x_test.astype("float32")

        model = keras.models.load_model(
            'C:/Users/62812/PROJEK TA/model.h5')

        hasil = model.predict(x_test)
        hasil = np.argmax(hasil, axis=1)

        print(hasil)

        normal = 0
        rbbb = 0
        apb = 0
        fvn = 0
        pvc = 0
        total = len(hasil)
        for y in hasil:
            if(y == 0):
                normal += 1
            if(y == 1):
                pvc += 1
            if(y == 2):
                rbbb += 1
            if(y == 3):
                apb += 1
            # if(y == 4):
            #     pvc += 1

        normal = (normal/total)*100
        rbbb = (rbbb/total)*100
        apb = (apb/total)*100
        pvc = (pvc/total)*100

        print("\n\n======PREDICT======\n")
        print('normal : %05.2f%%' % normal)
        print('rbbb   : %05.2f%%' % rbbb)
        print('apb    : %05.2f%%' % apb)
        print('pvc    : %05.2f%%' % pvc)
        print("===================")
        self.btn_classify.destroy()
        self.layoutClassify('Normal', '%d %%' % normal, column=0)
        self.layoutClassify('PVC', '%d %%' % pvc, column=1)
        self.layoutClassify('APB', '%d %%' % apb, column=2)
        self.layoutClassify('RBBB', '%d %%' % rbbb, column=3)
        self.btn_done.grid(row=3, padx=10, pady=10, columnspan=4)


class ReadLine:
    def __init__(self, s):
        self.buffer = bytearray()
        self.s = s

    def read_until(self, expected=b"\n", size=None):
        """Read until an expected sequence is found.

        Read until an expected sequence is found ('\n' by default), the size
        is exceeded or until timeout occurs.
        """
        # timeout = Timeout(self._timeout)
        while True:
            if expected in self.buffer or (size is not None and len(self.buffer) >= size):
                eof_pos = self.buffer.find(expected)
                # The end slice index in python is not included as element
                frame = self.buffer[:eof_pos + 1]
                self.buffer = self.buffer[eof_pos + 1:]
                return frame

            self.buffer.extend(self.s.read(self.s.in_waiting or 1))


class SerialCtrl():
    def __init__(self):
        '''
        Initializing the main varialbles for the serial data
        '''
        self.ser = None

    def getCOMList(self):
        '''
        Method that get the lost of available coms in the system
        '''
        ports = serial.tools.list_ports.comports()
        self.com_list = [com[0] for com in ports]
        self.com_list.insert(0, "-")

    def SerialOpen(self, ComGUI):
        '''
        Method to setup the serial connection and make sure to go for the next only
        if the connection is done properly
        '''

        try:
            self.ser.is_open
        except:
            PORT = ComGUI.clicked_com.get()
            BAUD = ComGUI.clicked_bd.get()
            self.ser = serial.Serial()
            self.ser.baudrate = BAUD
            self.ser.port = PORT
            self.ser.timeout = 0.1

        try:
            if self.ser.is_open:
                print("Already Open")
                self.ser.status = True
            else:
                PORT = ComGUI.clicked_com.get()
                BAUD = ComGUI.clicked_bd.get()
                self.ser = serial.Serial()
                self.ser.baudrate = BAUD
                self.ser.port = PORT
                self.ser.timeout = 0.01
                self.ser.open()
                self.ser.status = True

        except:
            self.ser.status = False

        print("Serial status: " + str(self.ser.status))

    def SerialClose(self):
        '''
        Method used to close the UART communication
        '''
        try:
            # self.ser.is_open
            self.ser.close()
            self.ser.status = False
        except:
            self.ser.status = False

        print("Serial status: " + str(self.ser.status))

    def SerialDataStream(self, gui):
        self.threading = True
        gui.data.complete = False
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        serNew = (ReadLine(self.ser))
        while(self.threading):
            try:
                gui.data.ser_bytes = (serNew.read_until())
                if gui.data.data_fail < 10:
                    if gui.data.complete is False:
                        gui.data.DecodeData()
                        gui.data.read_time = time.time()
                        if len(gui.data.timestamp) < 1:
                            gui.data.start_time = gui.data.read_time
                            gui.data.FileNameFunc()
                        gui.data.buildLeadData()
                        gui.data.PlotData()
                        gui.data.timer()

                        # print(gui.data.lead_v6)
                    else:
                        #print("complete record in " + str(gui.clicked_dur.get()))
                        gui.completeMsg()
                        break
                else:
                    print("failed to collect data")
                    gui.errorMsg()
                    break
            except Exception as e:
                print("Stream Error: ", e)
                # gui.errorMsg()
                # gui.errorMsg()
                break


class DataMaster():
    def __init__(self):
        self.timestamp = []
        self.data_raw = []
        self.lead_1 = []
        self.lead_2 = []
        self.lead_3 = []
        self.lead_avr = []
        self.lead_avl = []
        self.lead_avf = []
        self.lead_v1 = []
        self.lead_v2 = []
        self.lead_v3 = []
        self.lead_v4 = []
        self.lead_v5 = []
        self.lead_v6 = []
        self.data_fail = 0
        self.DISPLAY_SIZE = 800
        self.h = 600
        self.data_plot = [-2] * self.DISPLAY_SIZE
        self.ch_lead = 1
        self.avg = [349, 341, 345, 342, 336, 341, 340, 355, 351]
        self.conv = [240, 190, 164, 269, 234, 145, 109, 126, 163]
        self.pos_plot = [0, 0.15, -0.1, 0, 0.1, -0.1, 0.1, 0.2, -0.2]

        self.period_time = 0
        self.start_time = 0
        self.read_time = 0

        self.progres_var = 0

        self.user_webid = []

    def FileNameFunc(self):
        now = datetime.now()
        # self.dir1 = "/home/pi/EKG/data/"
        self.dir1 = "D:/EKG/data/"
        if len(self.user_webid) > 0:
            self.filename = self.dir1 + \
                str(self.user_webid) + "-" + \
                now.strftime("%Y%m%d%H%M%S")+".csv"
        else:
            self.filename = "data_alat.csv"

    def SaveData(self, gui):
        # new_path = "D:/EKG/data/coba_1.csv"
        array_result = []
        index = 0
        for _ in self.lead_1:
            array_result.append([
                self.timestamp[index],
                self.lead_avf[index],
                self.lead_avl[index],
                self.lead_avr[index],
                self.lead_1[index],
                self.lead_2[index],
                self.lead_3[index],
                self.lead_v1[index],
                self.lead_v2[index],
                self.lead_v3[index],
                self.lead_v4[index],
                self.lead_v5[index],
                self.lead_v6[index]])

            index += 1
            # print(self.progres_var)
            gui.updateBar()
            self.progres_var += 1
            # print (index)

            # print(array_result)
            # save new file
        with open(self.filename, 'w', newline='') as file:
            file.write('timestamp,avf,avl,avr,i,ii,iii,v1,v2,v3,v4,v5,v6\n')
            my_writer = csv.writer(file, delimiter=',')
            my_writer.writerows(array_result)
        # gui.close()

    def SaveDataforClassify(self, gui):
        # new_path = "D:/EKG/data/coba_1.csv"
        array_result = []
        index = 0
        for _ in self.lead_1:
            array_result.append([
                self.timestamp[index],
                self.lead_avf[index],
                self.lead_avl[index],
                self.lead_avr[index],
                self.lead_1[index],
                self.lead_2[index],
                self.lead_3[index],
                self.lead_v1[index],
                self.lead_v2[index],
                self.lead_v3[index],
                self.lead_v4[index],
                self.lead_v5[index],
                self.lead_v6[index]])

            index += 1
            # print(self.progres_var)
            gui.updateBar()
            self.progres_var += 1
            # print (index)

            # print(array_result)
            # save new file
        with open(self.filename, 'w', newline='') as file:
            file.write('timestamp,avf,avl,avr,i,ii,iii,v1,v2,v3,v4,v5,v6\n')
            my_writer = csv.writer(file, delimiter=',')
            my_writer.writerows(array_result)
        # gui.close()

        no_id = 1
        header = ['id', 'time', 'AVF', 'AVL', 'AVR', 'I',
                  'II', 'III', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        with open('data_alat_siap.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

        pathAnno = ('annotasi.csv')
        pathECG = ('data_alat.csv')

        file = Path(pathAnno)
        if file.is_file():
            y = 0
            print("Reading ECG")
            anotasi = pd.read_csv(pathAnno)
            npanotasi = anotasi.values
            sample = npanotasi[:, 1]
            data = pd.read_csv(pathECG)
            npdata = data.values
            ecg = npdata[:, :]

            for x in sample:
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("data_alat_siap.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                no_id += 1
                y += 1

    def DecodeData(self):
        decoded_bytes = str(self.ser_bytes[0:len(
            self.ser_bytes) - 2].decode('utf8', errors='ignore'))
        # print(decoded_bytes)
        x = re.search(
            r"^[0-9]*,[0-9]*,[0-9]*,[0-9]*,[0-9]*,[0-9]*,[0-9]*,[0-9]*,[0-9]*$", decoded_bytes)
        if x:
            self.data_raw = decoded_bytes
            self.data_split = self.data_raw.split(",")
        else:
            self.data_fail += 1
            # print(self.data_)

    def ConvertData(self, i):
        data_new = (
            (float(self.data_split[i]) - self.avg[i]) / self.conv[i]) + float(self.pos_plot[i])
        return data_new

    def buildLeadData(self):
        try:
            self.avr = -((self.ConvertData(0) + self.ConvertData(1)) / 2)+0.05
            self.avl = self.ConvertData(0) - (self.ConvertData(1) / 2)+0.2
            self.avf = self.ConvertData(1) - (self.ConvertData(0) / 2)-0.4

            self.timestamp.append(self.read_time)
            self.lead_1.append(self.ConvertData(0))
            self.lead_2.append(self.ConvertData(1))
            self.lead_3.append(self.ConvertData(2))
            self.lead_avr.append(self.avr)
            self.lead_avl.append(self.avl)
            self.lead_avf.append(self.avf)
            self.lead_v1.append(self.ConvertData(3))
            self.lead_v2.append(self.ConvertData(4))
            self.lead_v3.append(self.ConvertData(5))
            self.lead_v4.append(self.ConvertData(6))
            self.lead_v5.append(self.ConvertData(7))
            self.lead_v6.append(self.ConvertData(8))

        except:
            print("error")
            pass

    def PlotData(self):
        try:
            # print(self.ch_lead)
            if self.ch_lead > 8:
                if self.ch_lead == 9:
                    lead_plot = self.avl
                if self.ch_lead == 10:
                    lead_plot = self.avr
                if self.ch_lead == 11:
                    lead_plot = self.avf
            else:
                lead_plot = self.ConvertData(self.ch_lead)
            # print(lead_plot)
            self.data_plot.append(lead_plot)
            self.data_plot.pop(0)

        except:
            pass

    def ClearData(self):
        self.timestamp = []
        self.data_raw = []
        self.lead_1 = []
        self.lead_2 = []
        self.lead_3 = []
        self.lead_avr = []
        self.lead_avl = []
        self.lead_avf = []
        self.lead_v1 = []
        self.lead_v2 = []
        self.lead_v3 = []
        self.lead_v4 = []
        self.lead_v5 = []
        self.lead_v6 = []
        self.data_split = []
        self.data_fail = 0
        self.data_plot = [-2] * self.DISPLAY_SIZE
        self.progres_var = 0

        self.period_time = 0
        self.start_time = 0
        self.read_time = 0

    def timer(self):
        # print(self.start_time, self.period_time)
        if time.time() >= self.start_time + self.period_time:
            self.complete = True
            return

    def make_json(self, csvFilePath, jsonFilePath):

        data = {}
        count = 0

        with open(csvFilePath, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf, delimiter=',')

            for rows in csvReader:
                key = count
                data[key] = rows
                count += 1

        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))

        result = json.dumps(data, indent=4)
        return result

    def send_json(self):

        csvFilePath = self.filename
        jsonFilePath = r'test.json'

        awal = time.time()
        result = self.make_json(csvFilePath, jsonFilePath)
        tengah = time.time()
        # url = 'http://localhost/ecg-hospital/Data/apiGetData/5/c4ca4238a0b923820dcc509a6f75849b'
        #url = "http://alive.b401telematics.com/Data/apiGetData/"+str(self.user_webid)+"/c4ca4238a0b923820dcc509a6f75849b"
        url = "http://ecg.komputer-its.com/Data/apiGetData/" + \
            str(self.user_webid)+"/c4ca4238a0b923820dcc509a6f75849b/0"

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=result, headers=headers, verify=False)
        akhir = time.time()
        print("time buat json = ", tengah - awal)
        print("time upload = ", akhir-tengah)
        # print(r.text)


MySerial = SerialCtrl()
MyData = DataMaster()
RootMaster = RootGUI(MySerial)

ComMaster = ComGUI(RootMaster.container, MySerial, MyData)
UserMaster = UserGUI(RootMaster.container, MyData, ComMaster)
PlotMaster = PlotGUI(RootMaster.container, MySerial, MyData)

#RecordMaster = RecordGUI(RootMaster.container)
if __name__ == '__main__':
    RootMaster.root.mainloop()
