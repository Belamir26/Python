import tkinter as tk
from tkinter import ttk
import serial
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración del puerto serial
SERIAL_PORT = 'COM10'  # Cambiar por el puerto serial correcto
BAUD_RATE = 9600

# Configuración de las columnas para el spider plot
columns = ['EMG1', 'EMG2', 'EMG3', 'EMG4', 'EMG5', 'EMG6', 'EMG7', 'EMG8']

class SerialReader:
    def __init__(self, port, baud_rate):
        self.ser = serial.Serial(port, baud_rate, timeout=1)
        self.is_running = False
    
    def start(self):
        self.is_running = True
        threading.Thread(target=self.read_serial, daemon=True).start()
    
    def read_serial(self):
        while self.is_running:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                data = list(map(float, line.split(','))) # cambiar esto solo para los canales de EMG
                if len(data) == len(columns):
                    self.callback(data)
            time.sleep(0.1)
    
    def set_callback(self, callback):
        self.callback = callback

    def stop(self):
        self.is_running = False
        self.ser.close()

class SpiderPlotApp(tk.Tk):
    def __init__(self, serial_reader):
        super().__init__()
        self.title("Spider Plot Serial Monitor")
        
        self.serial_reader = serial_reader
        self.serial_reader.set_callback(self.update_plot)
        
        # Crear el lienzo de matplotlib para integrar en Tkinter
        self.figure, self.ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Crear el botón de inicio
        self.start_button = ttk.Button(self, text="Start", command=self.start_reading)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Crear el botón de stop
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_reading)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)

    def start_reading(self):
        self.serial_reader.start()
    
    def stop_reading(self):
        self.serial_reader.stop()

    def update_plot(self, data):
        self.ax.clear()
        
        num_vars = len(columns)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        data += data[:1]
        angles += angles[:1]

        self.ax.set_theta_offset(np.pi / 2)
        self.ax.set_theta_direction(-1)
        self.ax.plot(angles, data, linewidth=2, linestyle='solid')
        self.ax.fill(angles, data, 'b', alpha=0.25)
        self.ax.set_xticks(angles[:-1])
        self.ax.set_xticklabels(columns)

        self.canvas.draw()

if __name__ == "__main__":
    serial_reader = SerialReader(SERIAL_PORT, BAUD_RATE)
    app = SpiderPlotApp(serial_reader)
    app.mainloop()
