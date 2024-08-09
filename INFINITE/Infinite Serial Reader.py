from tkinter import Tk, Frame, Button, Label, ttk, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import collections
from threading import Thread
import time


serial_port = 'COM14'  # Replace with your serial port
baud_rate = 115200  # Replace with your baud rate
ser = serial.Serial(serial_port, baud_rate)
ser.setRTS(False)
ser.setDTR(False)

muestras=100

plot1, ax1 =plt.subplots(facecolor='#000000', dpi=100, figsize=(4,2))
plt.title("POTENCIOMETRO 1",color='white',size=12,family="Arial")
ax1.tick_params(direction='out',length=5,width=2,color= 'white',grid_color='r',grid_alpha=0.5)
line, = ax1.plot([],[], color= 'm', marker='o',linewidth=2,markersize=1,markeredgecolor='m')
line2, = ax1.plot([],[], color= 'g', marker='o',linewidth=2,markersize=1,markeredgecolor='g')
plt.xlim([0,muestras])
plt.ylim([0,5000])
datos_uno_uno = collections.deque([0]*muestras, maxlen=muestras)
datos_uno_dos = collections.deque([0]*muestras, maxlen=muestras)



plot2, ax2 =plt.subplots(facecolor='#000000', dpi=100, figsize=(4,2))
plt.title("POTENCIOMETRO 2",color='white',size=12,family="Arial")
ax2.tick_params(direction='out',length=5,width=2,color= 'white',grid_color='r',grid_alpha=0.5)
line3, = ax2.plot([],[], color= 'm', marker='o',linewidth=2,markersize=1,markeredgecolor='m')
line4, = ax2.plot([],[], color= 'g', marker='o',linewidth=2,markersize=1,markeredgecolor='g')
plt.xlim([0,muestras])
plt.ylim([0,5000])

datos_dos_uno = collections.deque([0]*muestras, maxlen=muestras)
datos_dos_dos = collections.deque([0]*muestras, maxlen=muestras)


def process():
    global dato
    hilo.start()
    anim=animation.FuncAnimation(plot1,plotData1,interval=100,blit=False)
    anim2=animation.FuncAnimation(plot2,plotData2,interval=100,blit=False)
    grafica1.draw()
    grafica2.draw()

def acq_sensor():
    while True:
        global dato
        if ser.in_waiting > 0:
            datos = ser.readline().decode('utf-8').strip()
            dato = datos.split(",")
            
def plotData1(i):
    global dato
    dato1= float(dato[0])
    dato2= float(dato[1])
    datos_uno_uno.append(dato1)
    line.set_data(range(muestras),datos_uno_uno)
    datos_uno_dos.append(dato2)
    line2.set_data(range(muestras),datos_uno_dos)

def plotData2(i):
    dato3= float(dato[2])
    dato4= float(dato[3])
    line2.set_data(range(muestras),datos_uno_dos)
    datos_dos_uno.append(dato3)
    line3.set_data(range(muestras),datos_dos_uno)
    datos_dos_dos.append(dato4)
    line4.set_data(range(muestras),datos_dos_dos)
      

def plotData(i):
            global datos 

            dato = datos.split(",")
            dato1= float(dato[0])
            dato2= float(dato[1])
            dato3= float(dato[2])
            dato4= float(dato[3])
            datos_uno_uno.append(dato1)
            line.set_data(range(muestras),datos_uno_uno)
            datos_uno_dos.append(dato2)
            line2.set_data(range(muestras),datos_uno_dos)
            datos_dos_uno.append(dato3)
            line3.set_data(range(muestras),datos_dos_uno)
            datos_dos_dos.append(dato4)
            line4.set_data(range(muestras),datos_dos_dos)
            





hilo= Thread(target=acq_sensor)
root = Tk()
root.title("Infinite")

frame1=Frame(root, width = 400,height = 400, bg = "#1003FC")
frame1.grid(row = 0,column = 0, padx = 1,pady = 1)

frame2=Frame(root, width = 400,height = 400, bg = "#7003FC")
frame2.grid(row = 1,column = 0, padx = 1,pady = 1)

frame3=Frame(root, width = 400,height = 400, bg = "#7003FC")
frame3.grid(row = 0,column = 1, padx = 1,pady = 1)

grafica1= FigureCanvasTkAgg(plot1, master=frame1)
grafica1.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')
grafica2= FigureCanvasTkAgg(plot2, master=frame2)
grafica2.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')

bt_graficar= Button(frame3, command=process,text='Conectar', font=('Arial',12,'bold'), width=12,bg='green2',fg='white')
bt_graficar.pack(pady=5,expand=1)

root.mainloop()
