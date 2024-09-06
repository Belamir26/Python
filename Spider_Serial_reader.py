from tkinter import Tk, Frame, Button, Label, ttk, PhotoImage, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import collections
from threading import Thread
import time
import numpy as np

serial_port = 'COM8'  # Replace with your serial port
baud_rate = 115200  # Replace with your baud rate
ser = serial.Serial(serial_port, baud_rate)
ser.setRTS(False)
ser.setDTR(False)




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
def process():
    global datos
    hilo.start()


def acq_sensor():
    while True:
        global datos
        if ser.in_waiting > 0:
            datos = ser.readline().decode('utf-8').strip()
            dato = datos.split(",")
            print(dato)
            dato = dato[7:15]
            dato += dato[:1]
            lista_float = [float(elemento) for elemento in dato]
            ax.clear()
            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
            plt.xticks(angles[:-1], columns)
            plt.ylim([0, 3.5])
            ax.set_ylim([0, 3.5])
            ax.plot(angles, lista_float)
            # plt.ylim([0, 3.5])
            # ax.set_ylim([0, 3.5])
            grafica1.draw()
            






hilo= Thread(target=acq_sensor)
root = Tk()
root.title("Infinite")

frame1=Frame(root, width = 800,height = 800, bg = "#1003FC")
frame1.grid(row = 0,column = 0, padx = 1,pady = 1)

frame2=Frame(root, width = 800,height = 800, bg = "#7003FC")
frame2.grid(row = 1,column = 0, padx = 1,pady = 1)


grafica1= FigureCanvasTkAgg(fig, master=frame1)
grafica1.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')


bt_graficar= Button(frame2, command=process,text='Conectar', font=('Arial',12,'bold'), width=12,bg='green2',fg='white')
bt_graficar.pack(pady=5,expand=1)




root.mainloop()
