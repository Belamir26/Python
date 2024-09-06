import tkinter as tk
import time

class CronometroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cronómetro para Ejercicio")
        
        self.label_ejercicio = tk.Label(root, text="Ejercicio:", font=("Arial", 16))
        self.label_ejercicio.pack()

        self.cronometro_label = tk.Label(root, text="00:00:000", font=("Arial", 48))
        self.cronometro_label.pack()

        self.estado_label = tk.Label(root, text="", font=("Arial", 16))
        self.estado_label.pack()

        self.sets_label = tk.Label(root, text="Número de sets (reposo y acción):", font=("Arial", 12))
        self.sets_label.pack()

        self.sets_entry = tk.Entry(root)
        self.sets_entry.pack()

        self.accion_label = tk.Label(root, text="Acción 0", font=("Arial", 14))
        self.accion_label.pack()

        self.start_button = tk.Button(root, text="Iniciar", command=self.start_cronometro)
        self.start_button.pack()

        self.reset_button = tk.Button(root, text="Reiniciar", command=self.reset_cronometro)
        self.reset_button.pack()

        self.running = False
        self.start_time = 0
        self.time_elapsed = 0
        self.current_set = 0
        self.accion_count = 0
        self.rest_duration = 3
        self.action_duration = 5

    def update_cronometro(self):
        if self.running:
            now = time.time()
            self.time_elapsed = now - self.start_time
            millis = int((self.time_elapsed % 1) * 1000)
            seconds = int(self.time_elapsed) % 60
            minutes = int(self.time_elapsed // 60)
            self.cronometro_label.config(text=f"{minutes:02}:{seconds:02}:{millis:03}")
            
            # Lógica para cambio de reposo y acción
            total_duration = self.current_set * (self.rest_duration + self.action_duration) + self.rest_duration
            if self.time_elapsed >= total_duration:
                self.current_set += 1
                if self.current_set <= self.sets:
                    self.accion_count += 1
                    self.accion_label.config(text=f"Acción {self.accion_count}")
                else:
                    self.stop_cronometro()
                    self.estado_label.config(text="Fin del ejercicio")
                    return
            
            # Alternar entre reposo y acción
            if self.time_elapsed % (self.rest_duration + self.action_duration) < self.rest_duration:
                self.estado_label.config(text="Reposo", fg="green")
            else:
                self.estado_label.config(text="Acción", fg="red")
            
            self.root.after(1, self.update_cronometro)

    def start_cronometro(self):
        try:
            self.sets = int(self.sets_entry.get())
        except ValueError:
            self.sets_label.config(text="Introduce un número válido de sets", fg="red")
            return

        if not self.running:
            self.start_time = time.time() - self.time_elapsed
            self.running = True
            self.update_cronometro()

    def stop_cronometro(self):
        self.running = False

    def reset_cronometro(self):
        self.stop_cronometro()
        self.time_elapsed = 0
        self.cronometro_label.config(text="00:00:000")
        self.accion_count = 0
        self.current_set = 0
        self.accion_label.config(text="Acción 0")
        self.estado_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = CronometroApp(root)
    root.mainloop()
