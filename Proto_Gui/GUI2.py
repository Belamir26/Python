import serial,time,collections
import matplotlib.pyplot as plt
import matplotlib.animation as animacion
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
from tkinter import Tk, Frame, StringVar, Label,Button,Entry



# , figsize=(6, 5)   tamaño / , dpi=75  zoom / plt.cla()  borra  nombres x e y /
fig = plt.figure(facecolor="0.55",figsize=(6, 4), clear=True, dpi=100)

ax = plt.axes(xlim=(0,100),ylim=(0,5000))
plt.title("8EMG",color='red',size=16, family="Tahoma")
ax.set_ylabel("V")
lines = ax.plot([] ,[], 'r')[0]


fig2 = plt.figure(facecolor="0.55",figsize=(6, 4), clear=True, dpi=100)
ax2 = plt.axes(xlim=(0,400),ylim=(0,3000))
plt.title("IMU",color='red',size=16, family="Tahoma")
lines2 = ax2.plot([] ,[], 'g')[0]


    
raiz = Tk()
raiz.protocol("WM_DELATE_WINDOW")
raiz.config(bg = "black")
raiz.title("  \t\t\t\t Infinite")
raiz.geometry("1000x804")
raiz.resizable(1,1)




lienzo = FigureCanvasTkAgg(fig, master = raiz )
lienzo._tkcanvas.grid(row = 0,column = 0, padx = 1,pady = 1)
lienzo2 = FigureCanvasTkAgg(fig2, master = raiz )
lienzo2._tkcanvas.grid(row = 1,column = 0, padx = 1,pady = 1)


frameconect=Frame(raiz, width = 400,height = 400, bg = "#7003FC")
frameconect.grid(row = 0,column = 1, padx = 1,pady = 1)
frameconect.grid_propagate(False)
frametiempo= Frame(raiz, width = 400,height = 400, bg = "#2003FC")
frametiempo.grid(row = 1,column = 1, padx = 1,pady = 1)
frametiempo.grid_propagate(False)


label_Com = StringVar(raiz, "COM: ")
label_Baud= StringVar(raiz, "BaudRate")
label_accion= StringVar(raiz, "Accion")
label_reposo= StringVar(raiz, "Reposo")
label_nombre= StringVar(raiz, "Nombre")
label_grip= StringVar(raiz, "Agarre")


labelcom = Label(frameconect,textvariable = label_Com, bg= "#5CFE05",fg="black", font="Helvetica 13 bold",width=11 ,justify="left")
labelcom.grid(row=0,column=0, padx=5,ipady=8, pady=10)
labelbaud = Label(frameconect,textvariable = label_Baud, bg= "#5CFE05",fg="black", font="Helvetica 13 bold",width=11 ,justify="left")
labelbaud.grid(row=1,column=0, padx=5,ipady=8, pady=10)
labelnombre = Label(frametiempo,textvariable = label_nombre, bg= "#5CFE05",fg="black", font="Helvetica 13 bold",width=11 ,justify="left")
labelnombre.grid(row=0,column=0, padx=5,ipady=8, pady=10)
labelgrip = Label(frametiempo,textvariable = label_grip, bg= "#5CFE05",fg="black", font="Helvetica 13 bold",width=11 ,justify="left")
labelgrip.grid(row=1,column=0, padx=5,ipady=8, pady=10)
labelaccion = Label(frametiempo,textvariable = label_accion, bg= "#5CFE05",fg="black", font="Helvetica 13 bold",width=11 ,justify="left")
labelaccion.grid(row=2,column=0, padx=5,ipady=8, pady=10)
labelreposo = Label(frametiempo,textvariable = label_reposo, bg= "#5CFE05",fg="black", font="Helvetica 13 bold",width=11 ,justify="left")
labelreposo.grid(row=2,column=1, padx=5,ipady=8, pady=10)


btConectar = Button(frameconect,command= None, text= "Conectar ",bg="blue",fg="white", font="Helvetica 14 bold",width=9,justify="center")
btConectar.grid(row=2,column=0, padx=5,pady=5)
btgraficar = Button(master=raiz,command= None, text= "Graficar ",bg="blue",fg="white", font="Helvetica 14 bold",width=9,justify="center")
btgraficar.grid(row=3,column=0, padx=5,pady=5)
btdatos = Button(frametiempo,command= None, text= "Tomar Datos ",bg="blue",fg="white", font="Helvetica 14 bold",width=9,justify="center")
btdatos.grid(row=3,column=0, padx=5,pady=5)




raiz.mainloop()
