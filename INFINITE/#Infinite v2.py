from tkinter import Tk, Frame, Button, Label, ttk, PhotoImage, StringVar, Checkbutton, Entry,IntVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
from serial import SerialException
import collections
from threading import Thread
import time
import pandas as pd
from openpyxl import Workbook

import serial.tools
import serial.tools.list_ports
from tkinter import messagebox

from PIL import Image, ImageTk
import numpy as np


Xpadx=10
Ypaxy=2
#Graficas
muestras=50
datos_IMU1 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU2 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU3 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU4 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU5 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU6 = collections.deque([0]*muestras, maxlen=muestras)

plotAccel, ax3 =plt.subplots(facecolor='#07396b', dpi=100, figsize=(4,2))
plt.title("IMU-Gyro",color='white',size=12,family="Arial")
ax3.tick_params(direction='out',length=5,width=2,color= 'white',grid_color='r',grid_alpha=0.5)
line4, = ax3.plot([],[], color= 'red', linewidth=2,label='gx')
line5, = ax3.plot([],[], color= 'purple', linewidth=2,label='gy')
line6, = ax3.plot([],[], color= 'pink', linewidth=2,label='gz')
plt.legend(loc='upper right', facecolor="w", fontsize=3)
plt.xlim([0,muestras])
plt.ylim([-100,100]) # probar borrando esto

plotGyro, ax1 =plt.subplots(facecolor='#07396b', dpi=100, figsize=(4,2))
plt.title("IMU-Accel",color='white',size=12,family="Arial")
ax1.tick_params(direction='out',length=5,width=2,color= 'white',grid_color='r',grid_alpha=0.5)
line, = ax1.plot([],[], color= 'blue', linewidth=2,label='ax')
line2, = ax1.plot([],[], color= 'orange', linewidth=2,label='ay')
line3, = ax1.plot([],[], color= 'green', linewidth=2,label='az')
plt.legend(loc='upper right', facecolor="w", fontsize=3)
plt.xlim([0,muestras])
plt.ylim([-3,3])

columns = ['EMG1', 'EMG2', 'EMG3', 'EMG4', 'EMG5', 'EMG6', 'EMG7', 'EMG8']
num_vars= len(columns)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], columns)
ax.plot([], [], linewidth=2, linestyle='solid')
plt.ylim([0,3.5])
ax.set_ylim([0, 3.5])
fig.patch.set_facecolor('#07396b')
ax.set_facecolor('#85b7e9')  # Color de fondo del gráfico



#Funciones







root = Tk()
root.title("Infinite")

frame1 = Frame(root, width=700, height=350, bg="#07396b")
frame1.grid(row=0, column=0)
frame1.propagate(False)
frame2_left = Frame(root, width=350, height=200, bg="#07396b")
frame2_left.grid(row=1, column=0, sticky="w", padx = 1,pady = 1)
frame2_left.propagate(False)
frame2_right = Frame(root, width=350, height=200, bg="green")
frame2_right.grid(row=1, column=0, sticky="e", padx = 1,pady = 1)
frame2_right.propagate(False)
frame3=Frame(root, width = 400,height = 350, bg = "#07396b")
frame3.grid(row = 0,column = 1, padx = 1,pady = 1)
frame3.grid_propagate(False)
frame4=Frame(root, width = 400,height = 200, bg = "#07396b")
frame4.grid(row = 1,column = 1, padx = 1,pady = 1)
frame4.grid_propagate(False)
frame5=Frame(root, width = 330,height = 550, bg = "#07396b")
frame5.grid(row = 0,column = 2, padx = 1,pady = 1,rowspan=2)
frame5.grid_propagate(False)


#FRAME 1
grafica1= FigureCanvasTkAgg(fig, master=frame1)
grafica1.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')


#FRAME 2
graficaACCEL= FigureCanvasTkAgg(plotAccel, master=frame2_left)
graficaACCEL.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')
graficaGYRO= FigureCanvasTkAgg(plotGyro, master=frame2_right)
graficaGYRO.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')


#FRAME 3
label_nombre= StringVar(root, "Name:")
label_grip= StringVar(root, "Grip:")
label_ntext= StringVar(root, "Tag:")
label_dtime= StringVar(root, "DesiredTime:")
agarres = ['Test','Cilindric','CloseHand','Handle', 'Pinch', 'PointTripod', 'Tripod']
check_grafica = IntVar()
check_datos = IntVar()


labeldata = Label(frame3,text="Data", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelnombre = Label(frame3,textvariable = label_nombre, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="center")
labelgrip = Label(frame3,textvariable = label_grip, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="center")
labelntext = Label(frame3,textvariable = label_ntext, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="center")
labeldtime = Label(frame3,textvariable = label_dtime, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="center")
name_entry= Entry(frame3, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=18 ,justify="left")
test_entry= Entry(frame3, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=18 ,justify="left")
time_entry= Entry(frame3, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=18 ,justify="left")
grip_combo= ttk.Combobox(frame3, values=agarres,background= "#bdffff",foreground="black", font="Helvetica 14 bold",width=12 ,justify="center" )
checkGrafica = Checkbutton(frame3, text='Plot', bg='white', fg='black', font="Helvetica 14 bold",width=10, variable=check_grafica)
checkDatos = Checkbutton(frame3, text='Data ACQ', bg='white', fg='black', font="Helvetica 14 bold",width=10, variable=check_datos)
btProceso = Button(frame3,command= None, text= "Proceso ",bg="white",fg="black", font="Helvetica 14 bold",width=12)
btReanudar = Button(frame3,command= None, text= "Reanudar ",bg="white",fg="black", font="Helvetica 14 bold",width=12)
btPausar = Button(frame3,command= None, text= "Pausar ",bg="white",fg="black", font="Helvetica 14 bold",width=12)
btSalir = Button(frame3,command= None, text= "Salir ",bg="white",fg="black", font="Helvetica 14 bold",width=12)

labeldata.grid(row=0,column=0,columnspan=2, padx=Xpadx,pady=20)
labelnombre.grid(row=1,column=0, padx=Xpadx,pady=Ypaxy)
labelgrip.grid(row=2,column=0, padx=Xpadx,pady=Ypaxy)
labelntext.grid(row=3,column=0, padx=Xpadx,pady=Ypaxy)
labeldtime.grid(row=4,column=0, padx=Xpadx,pady=Ypaxy)
name_entry.grid(row=1,column=1, padx=Xpadx,pady=Ypaxy)
test_entry.grid(row=2,column=1, padx=Xpadx,pady=Ypaxy)
time_entry.grid(row=3,column=1, padx=Xpadx,pady=Ypaxy)
grip_combo.grid(row=4,column=1, padx=Xpadx,pady=Ypaxy)
checkGrafica.grid(row=5,column=0, padx=Xpadx,pady=Ypaxy)
checkDatos.grid(row=5,column=1, padx=Xpadx,pady=Ypaxy)
btReanudar.grid(row=6,column=0, padx=Xpadx,pady=Ypaxy)
btProceso.grid(row=6,column=1, padx=Xpadx,pady=Ypaxy)
btPausar.grid(row=7,column=0, padx=Xpadx,pady=Ypaxy)
btSalir.grid(row=7,column=1, padx=Xpadx,pady=Ypaxy)




#FRAME 4
comlist= [port.device for port in serial.tools.list_ports.comports()]
baudlist = ['9600','115200']

labelserial = Label(frame4,text="Serial", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelcom = Label(frame4,text="COM", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelbaud = Label(frame4,text="Baudrates", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
com_combo= ttk.Combobox(frame4, values=comlist,background= "#bdffff",foreground="black", font="Helvetica 14 bold",width=12 ,justify="left" )
baud_combo= ttk.Combobox(frame4, values=baudlist,background= "#bdffff",foreground="black", font="Helvetica 14 bold",width=12 ,justify="left" )
btConectar = Button(frame4,command= None, text= "Conectar ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btActualizar = Button(frame4,command= None, text= "Actualizar COM ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")

labelserial.grid(row=0,column=0,columnspan=2, padx=Xpadx,pady=20)
labelcom.grid(row=1,column=0,  padx=20,pady=Ypaxy)
labelbaud.grid(row=2,column=0,  padx=20,pady=Ypaxy)
com_combo.grid(row=1,column=1,  padx=20,pady=Ypaxy)
baud_combo.grid(row=2,column=1,  padx=20,pady=Ypaxy)
btConectar.grid(row=3,column=0,  padx=20,pady=Ypaxy)
btActualizar.grid(row=3,column=1,  padx=20,pady=Ypaxy)

#FRAME 5
label_temp= StringVar(frame5, "TEMP: 0.0°C")
label_numacc= StringVar(frame5, "#Accion 0")

protlogo = ImageTk.PhotoImage(Image.open("menu-logo.jpg").resize((140, 80))) 
senselogo = ImageTk.PhotoImage(Image.open("sense.jpg").resize((140, 80))) 
infinitlogo = ImageTk.PhotoImage(Image.open("logo2.jpg").resize((250, 250))) 
labeltemp = Label(frame5,textvariable = label_temp, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labeltimer = Label(frame5,text="00:00:000", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelestado = Label(frame5,text="Reposo/Accion", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelnumacc = Label(frame5,textvariable = label_numacc, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
imageprot = Label(frame5, image=protlogo)
imagesense = Label(frame5, image=senselogo)
imageinfinit = Label(frame5, image=infinitlogo)

labeltemp.grid(row=2,column=0, padx=Xpadx,pady=Ypaxy,columnspan=2)
labeltimer.grid(row=3,column=0,  padx=Xpadx,pady=Ypaxy,columnspan=2)
labelestado.grid(row=4,column=0,  padx=Xpadx,pady=Ypaxy,columnspan=2)
labelnumacc.grid(row=5,column=0,  padx=Xpadx,pady=Ypaxy,columnspan=2)
imageprot.grid(row=0,column=0, padx=Xpadx,pady=20)
imagesense.grid(row=0,column=1, padx=Xpadx,pady=20)
imageinfinit.grid(row=6,column=0, padx=Xpadx,pady=20,columnspan=2)
root.mainloop()
