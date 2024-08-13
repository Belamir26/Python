from tkinter import Tk, Frame, Button, Label, ttk, PhotoImage, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import collections
from threading import Thread
import time


serial_port = 'COM3'  # Replace with your serial port
baud_rate = 115200  # Replace with your baud rate
ser = serial.Serial(serial_port, baud_rate)
ser.setRTS(False)
ser.setDTR(False)

muestras=50

plot1, ax1 =plt.subplots(facecolor='#000000', dpi=200, figsize=(4,2))
plt.title("IMU-Accel",color='white',size=12,family="Arial")
ax1.tick_params(direction='out',length=5,width=2,color= 'white',grid_color='r',grid_alpha=0.5)
line, = ax1.plot([],[], color= 'blue', linewidth=2,label='ax')
line2, = ax1.plot([],[], color= 'orange', linewidth=2,label='ay')
line3, = ax1.plot([],[], color= 'green', linewidth=2,label='az')
plt.legend(loc='upper right', facecolor="w", fontsize=3)
plt.xlim([0,muestras])
plt.ylim([-2,2])
datos_IMU1 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU2 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU3 = collections.deque([0]*muestras, maxlen=muestras)




plot3, ax3 =plt.subplots(facecolor='#000000', dpi=200, figsize=(4,2))
plt.title("IMU-Gyro",color='white',size=12,family="Arial")
ax3.tick_params(direction='out',length=5,width=2,color= 'white',grid_color='r',grid_alpha=0.5)
line4, = ax3.plot([],[], color= 'red', linewidth=2,label='gx')
line5, = ax3.plot([],[], color= 'purple', linewidth=2,label='gy')
line6, = ax3.plot([],[], color= 'pink', linewidth=2,label='gz')
plt.legend(loc='upper right', facecolor="w", fontsize=3)
plt.xlim([0,muestras])
plt.ylim([-100,100])
datos_IMU4 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU5 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU6 = collections.deque([0]*muestras, maxlen=muestras)



plot2, ax2 =plt.subplots(facecolor='#000000', dpi=200, figsize=(4,2))
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
plt.ylim([0,3.5])

datos_EMG1 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG2 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG3 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG4 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG5 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG6 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG7 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG8 = collections.deque([0]*muestras, maxlen=muestras)


def process():
    global datos
    hilo.start()
    anim=animation.FuncAnimation(plot1,plotData1,interval=100,blit=False)
    anim2=animation.FuncAnimation(plot2,plotData2,interval=100,blit=False)
    anim3=animation.FuncAnimation(plot3,plotData3,interval=100,blit=False)
    grafica1.draw()
    grafica2.draw()
    grafica3.draw()

def acq_sensor():
    while True:
        global datos
        if ser.in_waiting > 0:
            datos = ser.readline().decode('utf-8').strip()
            
            
def plotData1(i):
    global datos
    datox = datos.split(",")
    IMU1= float(datox[0])
    IMU2= float(datox[1])
    IMU3= float(datox[2])
    tempp= float(datox[6])
    label_temp.set("TEMP"+str(tempp)+ "°C")

    datos_IMU1.append(IMU1)
    line.set_data(range(muestras),datos_IMU1)
    datos_IMU2.append(IMU2)
    line2.set_data(range(muestras),datos_IMU2)
    datos_IMU3.append(IMU3)
    line3.set_data(range(muestras),datos_IMU3)

def plotData3(i):
    global datos
    datoxx = datos.split(",")
    IMU4= float(datoxx[3])
    IMU5= float(datoxx[4])
    IMU6= float(datoxx[5])

    datos_IMU4.append(IMU4)
    line4.set_data(range(muestras),datos_IMU4)
    datos_IMU5.append(IMU5)
    line5.set_data(range(muestras),datos_IMU5)
    datos_IMU6.append(IMU6)
    line6.set_data(range(muestras),datos_IMU6)



def plotData2(i):
    global datos
    dato = datos.split(",")
    EMG1=float(dato[7])
    EMG2=float(dato[8])
    EMG3=float(dato[9])
    EMG4=float(dato[10])
    EMG5=float(dato[11])
    EMG6=float(dato[12])
    EMG7=float(dato[13])
    EMG8=float(dato[14])

    datos_EMG1.append(EMG1)
    line81.set_data(range(muestras),datos_EMG1)
    datos_EMG2.append(EMG2)
    line82.set_data(range(muestras),datos_EMG2)
    datos_EMG3.append(EMG3)
    line83.set_data(range(muestras),datos_EMG3)
    datos_EMG4.append(EMG4)
    line84.set_data(range(muestras),datos_EMG4)
    datos_EMG5.append(EMG5)
    line85.set_data(range(muestras),datos_EMG5)
    datos_EMG6.append(EMG6)
    line86.set_data(range(muestras),datos_EMG6)
    datos_EMG7.append(EMG7)
    line87.set_data(range(muestras),datos_EMG7)
    datos_EMG8.append(EMG8)
    line88.set_data(range(muestras),datos_EMG8)


    
      

# def plotData(i):
#             global datos 

#             dato = datos.split(",")
#             dato1= float(dato[0])
#             dato2= float(dato[1])
#             dato3= float(dato[2])
#             dato4= float(dato[3])
#             datos_uno_uno.append(dato1)
#             line.set_data(range(muestras),datos_uno_uno)
#             datos_uno_dos.append(dato2)
#             line2.set_data(range(muestras),datos_uno_dos)
#             datos_dos_uno.append(dato3)
#             line3.set_data(range(muestras),datos_dos_uno)
#             datos_dos_dos.append(dato4)
#             line4.set_data(range(muestras),datos_dos_dos)
            





hilo= Thread(target=acq_sensor)
root = Tk()
root.title("Infinite")

frame1=Frame(root, width = 800,height = 800, bg = "#1003FC")
frame1.grid(row = 0,column = 0, padx = 1,pady = 1)

frame2=Frame(root, width = 800,height = 800, bg = "#7003FC")
frame2.grid(row = 1,column = 0, padx = 1,pady = 1)

frame3=Frame(root, width = 800,height = 800, bg = "#7003FC")
frame3.grid(row = 0,column = 1, padx = 1,pady = 1)

grafica1= FigureCanvasTkAgg(plot1, master=frame1)
grafica1.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')

grafica3= FigureCanvasTkAgg(plot3, master=frame1)
grafica3.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')

grafica2= FigureCanvasTkAgg(plot2, master=frame3)
grafica2.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')

bt_graficar= Button(frame2, command=process,text='Conectar', font=('Arial',12,'bold'), width=12,bg='green2',fg='white')
bt_graficar.pack(pady=5,expand=1)

label_temp= StringVar(frame2, "TEMP: 0.0°C")
labeltemp= Label(frame2,textvariable=label_temp, bg="#5CFE05", fg="black", font=('Arial',12,'bold'),width=12)
labeltemp.pack(pady=5,expand=1)


root.mainloop()
