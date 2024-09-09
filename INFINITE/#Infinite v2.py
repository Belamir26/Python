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


#CV
columns = ['ax','ay','az','gx','gy','gz', 't' ,'s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8' ,'mili','Status']
IMUACCEL=[0,0,0]
IMUGYRO=[0,0,0,0]
EMG=[0,0,0,0,0,0,0,0]

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

columnss = ['EMG1', 'EMG2', 'EMG3', 'EMG4', 'EMG5', 'EMG6', 'EMG7', 'EMG8']
num_vars= len(columnss)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], columnss)
ax.plot([], [], linewidth=2, linestyle='solid')
plt.ylim([0,3.5])
ax.set_ylim([0, 3.5])
fig.patch.set_facecolor('#07396b')
ax.set_facecolor('#85b7e9')  # Color de fondo del gráfico



#Funciones GUI
def conectar():
    """
    Intenta establecer una conexión serial con los parámetros seleccionados.

    Returns:
        str: Mensaje indicando el estado de la conexión.
    """
    global ser
    baud_rate = baud_combo.get()
    serial_port = com_combo.get()
    
    if baud_rate and serial_port:
        try:
            ser = serial.Serial(serial_port, baud_rate)
            ser.setRTS(False)
            ser.setDTR(False)
            messagebox.showinfo(message=f"Conexión establecida con éxito en {serial_port} a {baud_rate} baudios.", title="Infinite")
            print(f"Conexión establecida con éxito en {serial_port} a {baud_rate} baudios.") 
            btConectar.config(state='disabled')
            btActualizar.config(state='disabled')
        except SerialException as e:
            print(f"Error al intentar conectar: {e}")
    else:
        print("Por favor, selecciona un puerto serial y una tasa de baudios.")

def actualizar_COM():
    comlist= [port.device for port in serial.tools.list_ports.comports()]
    com_combo.config(values=comlist)




def salir():
    btProceso.config(state='normal')
    if check_grafica.get():
        anim2.event_source.stop()
        anim3.event_source.stop()
    checkDatos.config(state='normal')
    checkGrafica.config(state='normal')
    global isRun
    isRun = False
    ser.close()
    btConectar.config(state='normal')
    btActualizar.config(state='normal')


def bt_proceso():
    global isRun
    isRun = True
    btProceso.config(state='disabled')
    btReanudar.config(state='disabled')
    checkDatos.config(state='disabled')
    checkGrafica.config(state='disabled')

    if check_datos.get():
        #take from GUI interface, the labels, check buttons, and combo boxes
        name= name_entry.get()
        grip= grip_combo.get()  
        test= test_entry.get()
        destime= time_entry.get()


    if check_datos.get() and check_grafica.get():
        Thread(target=acq_sensor_data, args=(name, grip, test, labeltimer, destime, labelestado)).start()
        iniciar_animaciones()
    elif check_datos.get():
        Thread(target=acq_sensor_data, args=(name, grip, test, labeltimer, destime, labelestado)).start()
    elif check_grafica.get():
        messagebox.showinfo(message="Grafica", title="Infinite")
        Thread(target=acq_sensor_plot).start()
        iniciar_animaciones()
    else:
        messagebox.showinfo(message="No se selecciono nada", title="Infinite")
        

def sub_proceso(x, destime, name, grip, test, labeltimer, labelestado ):
    global isRun
    isRun = True
    try:
        if x == 1:
            print("x=1")
            start_time = time.time()
            end_time = start_time + int(destime)
            Thread(target=acq_sensor_data, args=(x,name, grip, test, labeltimer, start_time, end_time, labelestado)).start()
            iniciar_animaciones()

        elif x == 2:
            print("x=2")
            start_time = time.time()
            end_time = start_time + int(destime)
            Thread(target=acq_sensor_data, args=(x,name, grip, test, labeltimer, start_time, end_time, labelestado)).start()

        elif x == 3:
            print("x=3")
            Thread(target=acq_sensor_plot).start()
            iniciar_animaciones()

    except Exception as e:
        print(f"Error en sub_proceso: {e}")


#Subfunciones

def plotDataAccel(i):
    global IMUACCEL
    datos_IMU1.append(IMUACCEL[0])
    line.set_data(range(muestras),datos_IMU1)
    datos_IMU2.append(IMUACCEL[1])
    line2.set_data(range(muestras),datos_IMU2)
    datos_IMU3.append(IMUACCEL[2])
    line3.set_data(range(muestras),datos_IMU3)

def plotDataGyro(i):
    global IMUGYRO
    label_temp.set("TEMP"+str(IMUGYRO[3])+ "°C")
    datos_IMU4.append(IMUGYRO[0])
    line4.set_data(range(muestras),datos_IMU4)
    datos_IMU5.append(IMUGYRO[1])
    line5.set_data(range(muestras),datos_IMU5)
    datos_IMU6.append(IMUGYRO[2])
    line6.set_data(range(muestras),datos_IMU6)

def plotDataEMG(i):
    global EMG
    EMGdatos= EMG
    EMGdatos += EMG[:1]

    ax.clear()
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], columnss)
    plt.ylim([0, 3.5])
    ax.set_ylim([0, 3.5])
    ax.plot(angles, EMGdatos)
    # plt.ylim([0, 3.5])
    # ax.set_ylim([0, 3.5])
    graficaEMG.draw()

def iniciar_animaciones():
    global anim1,anim2, anim3
    anim2 = animation.FuncAnimation(plotAccel, plotDataAccel, interval=100, blit=False)
    anim3 = animation.FuncAnimation(plotGyro, plotDataGyro, interval=100, blit=False)
    anim1 = animation.FuncAnimation(fig, plotDataEMG, interval=100, blit=False)
    graficaEMG.draw()
    graficaACCEL.draw()
    graficaGYRO.draw()

#Hilos
def acq_sensor_plot():
    global isRun
    global EMG, IMUACCEL,IMUGYRO
    
    while isRun:
        
        if ser.in_waiting > 0:
            datos = ser.readline().decode('utf-8').strip()
            data = datos.split(',')
            if len(data)==16:
                data = [float(elemento) for elemento in data]
                data[7:15] = [0 if x > 3.4 else x for x in data[7:15]]
                IMUACCEL = data[0:3]
                IMUGYRO= data[3:7]
                EMG= data[7:15]
            else:
                print(data)


def acq_sensor_data(name,grip, test, labeltimer, destime, labelestado):
    global EMG, IMUACCEL,IMUGYRO

    global df
    global datos
    df = pd.DataFrame(None)
    df = pd.DataFrame(columns=columns)
    global anim1, anim2, anim3
    accion=0
    last_action_time=0
    label_numacc.set("#Accion " + str(accion))
    rest_duration=3
    action_duration=5
    current_set=0
    start_time = time.time()
    if check_tiempo.get():
        end_time =  start_time + int(destime)*8 + 3
        sets = int(destime)
    else:
        end_time = start_time + int(destime)
        sets = int((int(destime) - 3 )/8)

    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)
        labeltimer.config(text=f"{minutes:02}:{seconds:02}:{milliseconds:03}")

        

        if ser.in_waiting > 0:
            datos = ser.readline().decode('utf-8').strip()
            data = datos.split(',')
            if len(data)==16:
                data = [float(elemento) for elemento in data]
                data[7:15] = [0 if x > 3.4 else x for x in data[7:15]]
                IMUACCEL = data[0:3]
                IMUGYRO= data[3:7]
                EMG= data[7:15]
                if elapsed_time % (rest_duration + action_duration) < rest_duration:
                    data.append(0)
                else:
                    data.append(1) #Este apend depende del combobox                   
                df.loc[len(df)] = data

            else:
                print(data)


        total_duration = current_set * (rest_duration + action_duration) + rest_duration
        if elapsed_time >= total_duration:
            current_set +=1
            if current_set <= sets:
                accion += 1
                label_numacc.set("#Accion " + str(accion))

        if elapsed_time % (rest_duration + action_duration) < rest_duration:
            tiempo_set = seconds- current_set*(8)  +1
            labelestado.config(text="Reposo: "+ str(tiempo_set), background="#22a374")
        else:
            tiempo_set = seconds- ((current_set- 1) * 8) -3   +1
            labelestado.config(text="Accion: "+ str(tiempo_set), background="#CB4154")

            
            

        
        time.sleep(0.001)
    file_name = f"{name}_{grip}_{test}_{time.strftime('%m_%d_%H_%M_%S')}.xlsx"
    df.to_excel(file_name, index=False)
    print(f"Archivo guardado como {file_name}")


    if check_grafica.get():
        anim1.event_source.stop()
        anim2.event_source.stop()
        anim3.event_source.stop()
    ser.close()





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
graficaEMG= FigureCanvasTkAgg(fig, master=frame1)
graficaEMG.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')


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
check_tiempo = IntVar()

labeldata = Label(frame3,text="Data", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelnombre = Label(frame3,textvariable = label_nombre, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="center")
labelgrip = Label(frame3,textvariable = label_grip, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="center")
labelntext = Label(frame3,textvariable = label_ntext, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="center")
labeldtime = Label(frame3,textvariable = label_dtime, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="center")
name_entry= Entry(frame3, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=18 ,justify="left")
test_entry= Entry(frame3, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=18 ,justify="left")
time_entry= Entry(frame3, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=10 ,justify="left")
checkTiempo = Checkbutton(frame3,text='Sets', bg='white', fg='black', font="Helvetica 14 bold",width=3, variable=check_tiempo)
grip_combo= ttk.Combobox(frame3, values=agarres,background= "#bdffff",foreground="black", font="Helvetica 14 bold",width=12 ,justify="center" )
checkGrafica = Checkbutton(frame3, text='Plot', bg='white', fg='black', font="Helvetica 14 bold",width=10, variable=check_grafica)
checkDatos = Checkbutton(frame3, text='Data ACQ', bg='white', fg='black', font="Helvetica 14 bold",width=10, variable=check_datos)
btProceso = Button(frame3,command= bt_proceso, text= "Proceso ",bg="white",fg="black", font="Helvetica 14 bold",width=12)
btReanudar = Button(frame3,command= None, text= "Reanudar ",bg="white",fg="black", font="Helvetica 14 bold",width=12)
btPausar = Button(frame3,command= None, text= "Pausar ",bg="white",fg="black", font="Helvetica 14 bold",width=12)
btSalir = Button(frame3,command= salir, text= "Salir ",bg="white",fg="black", font="Helvetica 14 bold",width=12)




labeldata.grid(row=0,column=0,columnspan=3, padx=Xpadx,pady=20)

labelnombre.grid(row=1,column=0, padx=Xpadx,pady=Ypaxy)
labelgrip.grid(row=2,column=0, padx=Xpadx,pady=Ypaxy)
labelntext.grid(row=3,column=0, padx=Xpadx,pady=Ypaxy)
labeldtime.grid(row=4,column=0, padx=Xpadx,pady=Ypaxy)

name_entry.grid(row=1,column=1, padx=Xpadx,pady=Ypaxy,columnspan=2)
grip_combo.grid(row=2,column=1, padx=Xpadx,pady=Ypaxy,columnspan=2)
test_entry.grid(row=3,column=1, padx=Xpadx,pady=Ypaxy,columnspan=2)
time_entry.grid(row=4,column=1, padx=0,pady=0)
checkTiempo.grid(row=4,column=2, padx=0,pady=0)


checkGrafica.grid(row=5,column=0, padx=Xpadx,pady=Ypaxy)
checkDatos.grid(row=5,column=1, padx=Xpadx,pady=Ypaxy,columnspan=2)
btReanudar.grid(row=6,column=0, padx=Xpadx,pady=Ypaxy)
btProceso.grid(row=6,column=1, padx=Xpadx,pady=Ypaxy,columnspan=2)
btPausar.grid(row=7,column=0, padx=Xpadx,pady=Ypaxy)
btSalir.grid(row=7,column=1, padx=Xpadx,pady=Ypaxy,columnspan=2)




#FRAME 4
comlist= [port.device for port in serial.tools.list_ports.comports()]
baudlist = ['9600','115200']

labelserial = Label(frame4,text="Serial", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelcom = Label(frame4,text="COM", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelbaud = Label(frame4,text="Baudrates", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
com_combo= ttk.Combobox(frame4, values=comlist,background= "#bdffff",foreground="black", font="Helvetica 14 bold",width=12 ,justify="left" )
baud_combo= ttk.Combobox(frame4, values=baudlist,background= "#bdffff",foreground="black", font="Helvetica 14 bold",width=12 ,justify="left" )
btConectar = Button(frame4,command= conectar, text= "Conectar ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btActualizar = Button(frame4,command= actualizar_COM, text= "Actualizar COM ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")

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
labeltimer2 = Label(frame5,text="00", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=4 ,justify="left")


labelestado = Label(frame5,text="Reposo/Accion", bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelnumacc = Label(frame5,textvariable = label_numacc, bg= "#85b7e9",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
imageprot = Label(frame5, image=protlogo)
imagesense = Label(frame5, image=senselogo)
imageinfinit = Label(frame5, image=infinitlogo)

labeltemp.grid(row=2,column=0, padx=Xpadx,pady=Ypaxy,columnspan=2)
labeltimer.grid(row=3,column=0,  padx=Xpadx,pady=Ypaxy,columnspan=2)

# labeltimer2.grid(row=4,column=1,  padx=Xpadx,pady=Ypaxy)
labelestado.grid(row=4,column=0,  padx=Xpadx,pady=Ypaxy,columnspan=2)
labelnumacc.grid(row=5,column=0,  padx=Xpadx,pady=Ypaxy,columnspan=2)
imageprot.grid(row=0,column=0, padx=Xpadx,pady=20)
imagesense.grid(row=0,column=1, padx=Xpadx,pady=20)
imageinfinit.grid(row=6,column=0, padx=Xpadx,pady=20,columnspan=2)
root.mainloop()
