#Infinite Final GUI

from tkinter import Tk, Frame, Button, Label, ttk, PhotoImage, StringVar, Checkbutton, Entry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import collections
from threading import Thread
import time

import serial.tools
import serial.tools.list_ports


muestras=100

plot1, ax1 =plt.subplots(facecolor='#00774f', dpi=200, figsize=(4,2))
plt.title("IMU-Accel",color='white',size=12,family="Arial")
ax1.tick_params(direction='out',length=5,width=2,color= 'white',grid_color='r',grid_alpha=0.5)
line, = ax1.plot([],[], color= 'blue', linewidth=2,label='ax')
line2, = ax1.plot([],[], color= 'orange', linewidth=2,label='ay')
line3, = ax1.plot([],[], color= 'green', linewidth=2,label='az')
plt.legend(loc='upper right', facecolor="w", fontsize=3)
plt.xlim([0,muestras])
plt.ylim([-3,3])
datos_IMU1 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU2 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU3 = collections.deque([0]*muestras, maxlen=muestras)


plot3, ax3 =plt.subplots(facecolor='#00774f', dpi=200, figsize=(4,2))
plt.title("IMU-Gyro",color='white',size=12,family="Arial")
ax3.tick_params(direction='out',length=5,width=2,color= 'white',grid_color='r',grid_alpha=0.5)
line4, = ax3.plot([],[], color= 'red', linewidth=2,label='gx')
line5, = ax3.plot([],[], color= 'purple', linewidth=2,label='gy')
line6, = ax3.plot([],[], color= 'pink', linewidth=2,label='gz')
plt.legend(loc='upper right', facecolor="w", fontsize=3)
plt.xlim([0,muestras])
plt.ylim([-100,100]) # probar borrando esto
datos_IMU4 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU5 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU6 = collections.deque([0]*muestras, maxlen=muestras)


plot2, ax2 =plt.subplots(facecolor='#00774f', dpi=200, figsize=(4,2))
plt.title("8EMG",color='white',size=12,family="Arial")
ax2.tick_params(direction='out',length=5,width=2,color= 'white',grid_color='r',grid_alpha=0.5)
line81, = ax2.plot([],[], color= 'blue', linewidth=2,label='1Ch')
line82, = ax2.plot([],[], color= 'orange', linewidth=2,label='2Ch')
line83, = ax2.plot([],[], color= 'green', linewidth=2,label='3Ch')
line84, = ax2.plot([],[], color= 'red', linewidth=2,label='4Ch')
line85, = ax2.plot([],[], color= 'purple', linewidth=2,label='5Ch')
line86, = ax2.plot([],[], color= 'pink', linewidth=2,label='6Ch')
line87, = ax2.plot([],[], color= 'brown', linewidth=2,label='7Ch')
line88, = ax2.plot([],[], color= 'cyan',linewidth=2,label='8Ch')
plt.legend(loc='upper right', facecolor="w", fontsize=3)
plt.xlim([0,muestras])
plt.ylim([0,4])






root = Tk()
root.title("Infinite")

frame11=Frame(root, width = 100,height = 100, bg = "#00774f")
frame11.grid(row = 0,column = 0, padx = 1,pady = 1)
frame11.grid_propagate(False)
frame12=Frame(root, width = 100,height = 100, bg = "#00774f")
frame12.grid(row = 1,column = 0, padx = 1,pady = 1)
frame12.grid_propagate(False)
frame21=Frame(root, width = 100,height = 100, bg = "#00774f")
frame21.grid(row = 0,column = 1, padx = 1,pady = 1)
frame21.grid_propagate(False)
frame22=Frame(root, width = 800,height = 400, bg = "#00774f")
frame22.grid(row = 1,column = 1, padx = 1,pady = 1)
frame22.grid_propagate(False)
frame31=Frame(root, width = 300,height = 400, bg = "#00774f")
frame31.grid(row = 0,column = 2, padx = 1,pady = 1)
frame31.grid_propagate(False)
frame32=Frame(root, width = 300,height = 400, bg = "#00774f")
frame32.grid(row = 1,column = 2, padx = 1,pady = 1)
frame32.grid_propagate(False)


grafica1= FigureCanvasTkAgg(plot1, master=frame11)
grafica1.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')
grafica3= FigureCanvasTkAgg(plot3, master=frame12)
grafica3.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')
grafica2= FigureCanvasTkAgg(plot2, master=frame21)
grafica2.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')




label_nombre= StringVar(root, "Nombre:  ")
label_grip= StringVar(root, "Grip:  ")
label_ntext= StringVar(root, "#test:  ")
label_dtime= StringVar(root, "DesiredTime:  ")

labelnombre = Label(frame22,textvariable = label_nombre, bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelnombre.grid(row=0,column=1, padx=75,ipady=8, pady=5)
labelgrip = Label(frame22,textvariable = label_grip, bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelgrip.grid(row=1,column=1, padx=5,ipady=8, pady=5)
labelntext = Label(frame22,textvariable = label_ntext, bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelntext.grid(row=2,column=1, padx=5,ipady=8, pady=5)
labeldtime = Label(frame22,textvariable = label_dtime, bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labeldtime.grid(row=3,column=1, padx=5,ipady=8, pady=5)

name_entry= Entry(frame22, bg= "#bdffff",fg="black", font="Helvetica 14 bold",width=20 ,justify="left")
name_entry.grid(row=0,column=2, padx=10,ipady=8,pady=5)

test_entry= Entry(frame22, bg= "#bdffff",fg="black", font="Helvetica 14 bold",width=20 ,justify="left")
test_entry.grid(row=2,column=2, padx=10,ipady=8,pady=5)

time_entry= Entry(frame22, bg= "#bdffff",fg="black", font="Helvetica 14 bold",width=20 ,justify="left")
time_entry.grid(row=3,column=2, padx=10,ipady=8,pady=5)



checkGrafica = Checkbutton(frame22, text='Plot', bg='white', fg='black', font="Helvetica 14 bold",width=10,justify="center")
checkGrafica.grid(row=4,column=1, padx=10,pady=5)
checkDatos = Checkbutton(frame22, text='Data ACQ', bg='white', fg='black', font="Helvetica 14 bold",width=10,justify="center")
checkDatos.grid(row=4,column=3, padx=10,pady=5)

btProceso = Button(frame22,command= None, text= "Proceso ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btProceso.grid(row=5,column=2, padx=10,pady=5)
btReanudar = Button(frame22,command= None, text= "Reanudar ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btReanudar.grid(row=5,column=1, padx=10,pady=5)
btPausar = Button(frame22,command= None, text= "Pausar ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btPausar.grid(row=5,column=3, padx=10,pady=5)
btSalir = Button(frame22,command= None, text= "Salir ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btSalir.grid(row=6,column=2, padx=10,pady=5)


agarres = ['TEST','POCILLO','CLOSE']
grip_combo= ttk.Combobox(frame22, values=agarres,background= "#bdffff",foreground="black", font="Helvetica 14 bold",width=20 ,justify="left" )
grip_combo.grid(row=1,column=2, padx=10,pady=5)



label_temp= StringVar(frame31, "TEMP: 0.0°C")
labeltemp = Label(frame31,textvariable = label_temp, bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labeltemp.grid(row=0,column=1, padx=5,ipady=8, pady=5)

##OJO CON ESTO-> PORQUE DEBERIA SER: tiempo variable como el de arriba
labeltimer = Label(frame31,text="00:00:000", bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labeltimer.grid(row=1,column=1, padx=5,ipady=8, pady=5)

labeltemp = Label(frame31,text="Reposo/Accion", bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labeltemp.grid(row=2,column=1, padx=5,ipady=8, pady=5)

label_temp= StringVar(frame31, "#Accion: 0")
labeltemp = Label(frame31,textvariable = label_temp, bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labeltemp.grid(row=3,column=1, padx=5,ipady=8, pady=5)




labelserial = Label(frame32,text="Serial", bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelserial.grid(row=0,column=1, padx=5,ipady=8, pady=5)
labelcom = Label(frame32,text="COM", bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelcom.grid(row=1,column=1, padx=5,ipady=8, pady=5)


comlist= [port.device for port in serial.tools.list_ports.comports()]
com_combo= ttk.Combobox(frame32, values=comlist,background= "#bdffff",foreground="black", font="Helvetica 14 bold",width=20 ,justify="left" )
com_combo.grid(row=2,column=1, padx=10,pady=5)

labelbaud = Label(frame32,text="Baudrates", bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelbaud.grid(row=3,column=1, padx=5,ipady=8, pady=5)

baudlist = ['9600','115200']
baud_combo= ttk.Combobox(frame32, values=baudlist,background= "#bdffff",foreground="black", font="Helvetica 14 bold",width=20 ,justify="left" )
baud_combo.grid(row=4,column=1, padx=10,pady=5)

btConectar = Button(frame32,command= None, text= "Conectar ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btConectar.grid(row=5,column=1, padx=10,pady=5)
btActualizar = Button(frame32,command= None, text= "Actualizar COM ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btActualizar.grid(row=6,column=1, padx=10,pady=5)

root.mainloop()
