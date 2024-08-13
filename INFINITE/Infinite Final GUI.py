#Infinite Final GUI

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
# #Ojo tiene que ir en boton


muestras=50
datos_IMU1 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU2 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU3 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU4 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU5 = collections.deque([0]*muestras, maxlen=muestras)
datos_IMU6 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG1 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG2 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG3 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG4 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG5 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG6 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG7 = collections.deque([0]*muestras, maxlen=muestras)
datos_EMG8 = collections.deque([0]*muestras, maxlen=muestras)

plot1, ax1 =plt.subplots(facecolor='#00774f', dpi=200, figsize=(4,2))
plt.title("IMU-Accel",color='white',size=12,family="Arial")
ax1.tick_params(direction='out',length=5,width=2,color= 'white',grid_color='r',grid_alpha=0.5)
line, = ax1.plot([],[], color= 'blue', linewidth=2,label='ax')
line2, = ax1.plot([],[], color= 'orange', linewidth=2,label='ay')
line3, = ax1.plot([],[], color= 'green', linewidth=2,label='az')
plt.legend(loc='upper right', facecolor="w", fontsize=3)
plt.xlim([0,muestras])
plt.ylim([-3,3])


plot3, ax3 =plt.subplots(facecolor='#00774f', dpi=200, figsize=(4,2))
plt.title("IMU-Gyro",color='white',size=12,family="Arial")
ax3.tick_params(direction='out',length=5,width=2,color= 'white',grid_color='r',grid_alpha=0.5)
line4, = ax3.plot([],[], color= 'red', linewidth=2,label='gx')
line5, = ax3.plot([],[], color= 'purple', linewidth=2,label='gy')
line6, = ax3.plot([],[], color= 'pink', linewidth=2,label='gz')
plt.legend(loc='upper right', facecolor="w", fontsize=3)
plt.xlim([0,muestras])
plt.ylim([-100,100]) # probar borrando esto


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



#CV
columns = ['ax','ay','az','gx','gy','gz', 't' ,'s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8' ,'mili']


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
        except SerialException as e:
            print(f"Error al intentar conectar: {e}")
    else:
        print("Por favor, selecciona un puerto serial y una tasa de baudios.")

def actualizar_COM():
    comlist= [port.device for port in serial.tools.list_ports.comports()]
    com_combo.config(values=comlist)


def reanudar():
    pass

def pausar():
    pass



#Mejorar esto aca!!!
def salir():
    ser.close()
    pass


def bt_proceso():
    #take from GUI interface, the labels, check buttons, and combo boxes
    x=0
    name= name_entry.get()
    grip= grip_combo.get()  # espero que sea asi
    test= test_entry.get()
    destime= time_entry.get()

    x1=check_datos.get() # toca buscar cual es para iniciar el sub proceso 
    x2=check_grafica.get()

    


    if x1 and x2:
        x=1
        sub_proceso(x, destime, name, grip, test, labeltimer, labelestado, labelnumacc)
        messagebox.showinfo(message="Evento Datos y grafica", title="Infinite")

    elif x1:
        x=2
        messagebox.showinfo(message="Evento datos", title="Infinite")
        sub_proceso(x, destime, name, grip, test, labeltimer, labelestado, labelnumacc)

    elif x2:
        x=3
        messagebox.showinfo(message="Evento grafica", title="Infinite")
        sub_proceso(x, destime, name, grip, test, labeltimer, labelestado, labelnumacc)
    else:
        messagebox.showinfo(message="Evento no seleeccionado", title="Infinite")


def sub_proceso(x, destime, name, grip, test, labeltimer, labelestado,labelnumacc ):

    try:
        if x == 1:
            print("x=1")
            start_time = time.time()
            end_time = start_time + int(destime)
            Thread(target=acq_sensor_data, args=(name, grip, test, labeltimer, start_time, end_time, labelestado, labelnumacc)).start()
            iniciar_animaciones()

        elif x == 2:
            print("x=2")
            start_time = time.time()
            end_time = start_time + int(destime)
            Thread(target=acq_sensor_data, args=(name, grip, test, labeltimer, start_time, end_time, labelestado, labelnumacc)).start()

        elif x == 3:
            print("x=3")
            Thread(target=acq_sensor_plot).start()
            iniciar_animaciones()

    except Exception as e:
        print(f"Error en sub_proceso: {e}")



#SUBFUNCIONES

def add_to_dataframe(data):
    global df
    # Split the received data into individual data points
    data_points = data.split(',')

    # Create a list with the timestamp followed by the data points
    # row = [time.strftime('%H:%M:%S')] + data_points
    row = data_points

    # Append the new row to the DataFrame
    df.loc[len(df)] = row

def save_excel_file(name, grip, test):
    global df
    
    # Crear el nombre del archivo
    file_name = f"{name}_{grip}_{test}_{time.strftime('%m_%d_%H_%M_%S')}.xlsx"
    
    # Guardar el archivo
    df.to_excel(file_name, index=False)
    print(f"Archivo guardado como {file_name}")

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

    #OPTIMIZAR
    if EMG1 > 8:
        EMG1 = 0
    if EMG2 > 8:
        EMG2 = 0
    if EMG3 > 8:
        EMG3 = 0
    if EMG4 > 8:
        EMG4 = 0
    if EMG5 > 8:
        EMG5 = 0
    if EMG6 > 8:
        EMG6 = 0
    if EMG7 > 8:
        EMG7 = 0
    if EMG8 > 8:
        EMG8 = 0

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

def iniciar_animaciones():
    anim = animation.FuncAnimation(plot1, plotData1, interval=100, blit=False)
    anim2 = animation.FuncAnimation(plot2, plotData2, interval=100, blit=False)
    anim3 = animation.FuncAnimation(plot3, plotData3, interval=100, blit=False)
    grafica1.draw()
    grafica2.draw()
    grafica3.draw()


#HILos
def acq_sensor_plot():
    while True:
        global datos
        if ser.in_waiting > 0:
            datos = ser.readline().decode('utf-8').strip()

def acq_sensor_data(name,grip, test, labeltimer, start_time, end_time, labelestado, labelnumacc):
    global df
    global datos
    df = pd.DataFrame(None)
    df = pd.DataFrame(columns=columns)

    
    accion=0
    last_action_time=0
    label_numacc.set("#Accion " + str(accion))

    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)

        if ser.in_waiting > 0:
            datos = ser.readline().decode('utf-8').strip()
            data = datos.split(',')
            data = [0 if float(x) > 8 else float(x) for x in data] # errores de 12V 
            
            df.loc[len(df)] = data
        

        if elapsed_time - last_action_time >= 20:
            accion += 1
            label_numacc.set("#Accion " + str(accion))
            last_action_time = elapsed_time

        

        if seconds % 20 < 10:
            labelestado.config(text="Reposo", background="red")
        else:
            labelestado.config(text="Acción", background="green")
            

        labeltimer.config(text=f"{minutes:02}:{seconds:02}:{milliseconds:03}")
        time.sleep(0.001)
    file_name = f"{name}_{grip}_{test}_{time.strftime('%m_%d_%H_%M_%S')}.xlsx"
    df.to_excel(file_name, index=False)
    print(f"Archivo guardado como {file_name}")
    ser.close()




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


check_grafica = IntVar()
check_datos = IntVar()
checkGrafica = Checkbutton(frame22, text='Plot', bg='white', fg='black', font="Helvetica 14 bold",width=10,justify="center", variable=check_grafica)
checkGrafica.grid(row=4,column=1, padx=10,pady=5)
checkDatos = Checkbutton(frame22, text='Data ACQ', bg='white', fg='black', font="Helvetica 14 bold",width=10,justify="center", variable=check_datos)
checkDatos.grid(row=4,column=3, padx=10,pady=5)

btProceso = Button(frame22,command= bt_proceso, text= "Proceso ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btProceso.grid(row=5,column=2, padx=10,pady=5)
btReanudar = Button(frame22,command= None, text= "Reanudar ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btReanudar.grid(row=5,column=1, padx=10,pady=5)
btPausar = Button(frame22,command= None, text= "Pausar ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btPausar.grid(row=5,column=3, padx=10,pady=5)
btSalir = Button(frame22,command= salir, text= "Salir ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
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

labelestado = Label(frame31,text="Reposo/Accion", bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelestado.grid(row=2,column=1, padx=5,ipady=8, pady=5)



label_numacc= StringVar(frame31, "#Accion 0")
labelnumacc = Label(frame31,textvariable = label_numacc, bg= "#57bd9e",fg="black", font="Helvetica 14 bold",width=12 ,justify="left")
labelnumacc.grid(row=3,column=1, padx=5,ipady=8, pady=5)


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

btConectar = Button(frame32,command= conectar, text= "Conectar ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btConectar.grid(row=5,column=1, padx=10,pady=5)
btActualizar = Button(frame32,command= actualizar_COM, text= "Actualizar COM ",bg="white",fg="black", font="Helvetica 14 bold",width=12,justify="center")
btActualizar.grid(row=6,column=1, padx=10,pady=5)

root.mainloop()
