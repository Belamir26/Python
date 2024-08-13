#Infinite GUI

import tkinter as tk
from tkinter import ttk
import time
import threading
import pandas as pd
from openpyxl import Workbook
import serial


# Serial port configuration
serial_port = 'COM13'  # Replace with your serial port
baud_rate = 115200  # Replace with your baud rate
ser = serial.Serial(serial_port, baud_rate)
ser.setRTS(False)
ser.setDTR(False)


columns = ['ax','ay','az','gx','gy','gz', 't' ,'s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8' ,'mili']
df = pd.DataFrame(columns=columns)

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



def update_timer(name, grip, test, label, start_time, end_time,estado_label):
    columns = ['ax','ay','az','gx','gy','gz', 't' ,'s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8' ,'mili']
    df = pd.DataFrame(columns=columns)
    interval = 0  # Milisegundos
    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)

        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Data: {data}")

            data = data.split(',')
            df.loc[len(df)] = data
            print(f"Data: {data}")
            




        # Cambiar color y texto cada 10 segundos
        if seconds % 20 < 10:
            estado_label.config(text="Reposo", background="red")
        else:
            estado_label.config(text="Acción", background="green")
        
        # Actualizar el cronómetro en la interfaz
        label.config(text=f"{minutes:02}:{seconds:02}:{milliseconds:03}")
        
        # Esperar un milisegundo antes de continuar
        interval += 1
        time.sleep(0.001)
    file_name = f"{name}_{grip}_{test}_{time.strftime('%m_%d_%H_%M_%S')}.xlsx"
    
    # Guardar el archivo
    df.to_excel(file_name, index=False)
    print(f"Archivo guardado como {file_name}")
    ser.close()




def process(destime, name,grip,test, timer_label,estado_label):
    start_time= time.time()
    end_time= time.time()+ int (destime)
    threading.Thread(target=update_timer, args=(name,grip,test,timer_label, start_time, end_time,estado_label)).start()
    



def bt_start():
    name= name_entry.get()
    grip= grip_entry.get()
    test= test_entry.get()
    destime= time_entry.get()
    
    if name and grip and test and destime:
        process(destime,name,grip,test, timer_label,estado_label)
    else:
        print("Por favor, complete todos los campos.")

#interfaz
root = tk.Tk()
root.title("Infinite")

ttk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
name_entry = ttk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Grip:").grid(row=1, column=0, padx=10, pady=5)
grip_entry = ttk.Entry(root)
grip_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="# Test:").grid(row=2, column=0, padx=10, pady=5)
test_entry = ttk.Entry(root)
test_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(root, text="DesiredTime:").grid(row=3, column=0, padx=10, pady=5)
time_entry = ttk.Entry(root)
time_entry.grid(row=3, column=1, padx=10, pady=5)

# Crear botón para iniciar el proceso
start_button = ttk.Button(root, text="Iniciar Proceso", command=bt_start)
start_button.grid(row=4, column=0, columnspan=2, pady=10)

# Crear una etiqueta para mostrar el cronómetro
timer_label = ttk.Label(root, text="00:00:000", font=("Helvetica", 24))
timer_label.grid(row=5, column=0, columnspan=2, pady=10)

# Crear una etiqueta para mostrar el estado de la acción/reposo
estado_label = ttk.Label(root, text="Reposo", font=("Helvetica", 18),background="red", width=20)
estado_label.grid(row=6, column=0, columnspan=2, pady=10)


root.mainloop()