import datetime
import tkinter
from tkinter import *
import os

import csv
import pandas as pd

import numpy

from main import runcurl

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np




nl="\n"
i1 = "Welcome to the curl analyzer, here are your instructions\n1. Press the Analyze my Curl Button\n"
i2=  "2. In 10 seconds, you should see a video opening up, to track your curl.\n"
i3=  "3. Start curling, do your reps and once you're done, hit Q\n"
i4=  "4. You can now get a graph of your exercise pattern.\n"
i5=  "5. Once you are done curling, hit what do my numbers mean to get a better analysis.\n"
i_net = i1+nl+i2+nl+i3+nl+i4+nl+i5

reps = []
time = []
max_time = 0
min_time = 0




root = Tk()

h = 700
w= 800




canvas = Canvas(root, height=h, width=w)
canvas.config(bg='#61ff8b')
canvas.pack()

Font_tuple1 = ("Comic Sans MS", 16, "bold")
Font_tuple2 = ("Times", "24", "bold italic")
Font_tuple3 = ("Helvetica", "15")

label=Label(canvas,text='The Bicep Curl Analyzer')
label.config(font=Font_tuple1)
label.place(relx=0.12, rely=0.08,relwidth=0.5,relheight=0.05)

frame =Frame(canvas,bg='white')
frame.place(relx=0.1,rely=0.2,relwidth = 0.6, relheight=0.7)

def plot_on_screen():
    for widgets in frame.winfo_children():
        widgets.destroy()
    date = datetime.date.today()
    date = str(date)


    a, b = runcurl()
    global reps
    global time
    global max_time
    global min_time
    reps = numpy.asarray(a)
    time = numpy.asarray(b)
    max_time = max(time)
    min_time = min(time[1:])

    fig = Figure(figsize=(5,4),dpi=100)
    fig.suptitle('Time vs Reps Graph', fontsize=15)
    fig.add_subplot(111).plot(reps,time)

    canvas = FigureCanvasTkAgg(fig, master=frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    path, dirs, files = next(os.walk("Plots/"))
    file_count = len(files)

    fig.savefig('Plots/'+str(date)+str(file_count))
    df = pd.read_csv('Curl_data.csv')
    temp = {'date': date , 'reps': len(reps) , 'max_time': max_time , 'min_time' : min_time}
    df = df.append(temp,ignore_index=True)
    df.to_csv('Curl_data.csv')

def get_instructions():
    for widgets in frame.winfo_children():
        widgets.destroy()

    text = Text(frame,font=Font_tuple3,padx=15,pady=15)
    text.insert(INSERT, i_net)
    text.pack()

def number_analysis():
    print(max_time)
    if(max_time==0):
        for widgets in frame.winfo_children():
            widgets.destroy()
        text = Text(frame, font=Font_tuple3, padx=15, pady=15)
        text.insert(INSERT, 'Analyse your curl to get time')

    else:
        for widgets in frame.winfo_children():
            widgets.destroy()
        t1 = "Maximum time taken:" + str(max_time) + '\n'
        t2 = "Minimum time taken:" + str(min_time) + '\n'
        t4 = '\n'
        t3 = "Your maximum time taken in a set has a direct correlation with your Rate of Perceived Exhaustion\n"
        t5= "Between 0 to 2 => RPE of 1 to 4, You need to train harder\n"
        t6 ="Between 2 to 5 => RPE of 5 to 7, You are in the sweet spot. Train at this intensity\n"
        t7 = "Above 5 => You have trained pretty hard. You may not be able to sustain this intensity."
        t_net = t1 + nl + t2 + nl + t3 + nl + t4 + nl + t5 + nl + t6 + nl + t7

        text = Text(frame, font=Font_tuple3, padx=15, pady=15)
        text.insert(INSERT, t_net)
    text.pack()





button1 = Button(canvas,text='Analyze your Curl',bg='#ffff70',fg='gray',bd=5,command=plot_on_screen)
button1.place(relx=0.75,rely=0.2,relwidth=0.22,relheight=0.1)

button2 = Button(canvas,text='Instructions',bg='#ffff70',fg='gray',bd=5, command = get_instructions)
button2.place(relx=0.75,rely=0.4,relwidth=0.22,relheight=0.1)

button3 = Button(canvas,text='What do my numbers mean?',bg='#ffff70',fg='gray',bd=5,command = number_analysis)
button3.place(relx=0.75,rely=0.6,relwidth=0.22,relheight=0.1)

button4 = Button(canvas,text='Quit',bg='#ffff70',fg='gray',bd=5,command=root.destroy)
button4.place(relx=0.75,rely=0.8,relwidth=0.22,relheight=0.1)






root.mainloop()