import serial
import pandas as pd

# Configuración del puerto serial
ser = serial.Serial('COM5',115200)  # Reemplaza 'COM3' con el puerto que estés usando

# Crear un DataFrame vacío con 10 columnas
columnas = ['accelX','accelY','accelZ','gyroX','gyroY','gyroZ','temp','emg1','emg2','emg3','emg4','emg5','emg6','emg7','emg8','Current', 'afterDatos', 'afterEnvio' ]
df = pd.DataFrame(columns=columnas)

try:
    while True:
        if ser.in_waiting > 0:
            # Leer línea del puerto serial
            line = ser.readline().decode('utf-8').strip()
            print(f'Dato recibido: {line}')
            
            # Separar los datos por comas y añadirlos al DataFrame
            datos = line.split(',')
            df.loc[len(df)] = datos
except KeyboardInterrupt:
    print('Lectura interrumpida por el usuario.')
    # Guardar el DataFrame en un archivo CSV
    df.to_excel('datos_serial.xlsx', index=False)
    print('Datos guardados en datos_serial.csv')

# Cerrar el puerto serial
ser.close()
