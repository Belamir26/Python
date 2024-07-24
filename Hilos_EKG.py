import PySimpleGUI as sg
import serial
import threading
import time
import serial
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd


# iMPORTS
import neurokit2
import wfdb
import wfdb.processing
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class SerialReader(threading.Thread):
    def __init__(self, ser):
        super().__init__()
        self.ser = ser
        self.data = []

    def run(self):
        while True:
            line = self.ser.readline().decode("utf-8").strip()
            self.data.append(int(line))
            if len(self.data) > 10000:
                ##solo almacena los ultimos 10000 datos
                self.data = self.data[-10000:]



while True:
    ser = serial.Serial("COM11", 115200, timeout=1)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    reader = SerialReader(ser)
    reader.start()
    time.sleep(10)
    data = np.array(reader.data)  # Convertir la lista en un array de numpy
    df = pd.DataFrame(data)
    df.to_csv("myfile.csv")
    plt.figure(figsize=(10,10))
    plt.imshow(data, cmap='viridis', origin='lower', extent=[0, 10, 0, 5])
    plt.colorbar(label="Valor")
    plt.show()