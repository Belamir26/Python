#Pruebas aka spider

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D



data= [
            [3.3, 2.4, 2.03, 1.03,4.00, 4.06, 0.01, 0.00],
            [3.35, 3.4, 2.04, 2.05, 0.00, 0.02, 2.01, 2.00],
            [3.5, 3.4, 2.85, 1.19, 0.05, 0.10, 0.00, 0.00],
            [2.5, 3.4, 2.07, 2.01, 0.21, 0.98, 0.00, 3.00],
            [2.5, 3, 2.02, 1.71, 0.70, 0.00, 4.00, 0.00]
            ]




import numpy as np
import matplotlib.pyplot as plt

def spider_plot(data, columns):
    num_vars = len(columns)
    
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    data += data[:1]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    plt.xticks(angles[:-1], columns)
    
    ax.plot(angles, data, linewidth=2, linestyle='solid')
    ax.fill(angles, data, 'b', alpha=0.25)
    
    plt.show()

def plot_data_series(data_series, columns):
    for i, data in enumerate(data_series):
        print(f"Plotting dataset {i + 1}")
        spider_plot(data, columns)

# Ejemplo de uso:
columns = ['EMG1', 'EMG2', 'EMG3', 'EMG4', 'EMG5', 'EMG6', 'EMG7', 'EMG8']


plot_data_series(data, columns)

