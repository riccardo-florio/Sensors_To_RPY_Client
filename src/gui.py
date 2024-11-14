# gui.py
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sensors import SensorManager
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt

class SensorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sensor Data Receiver")
        self.root.geometry("1280x900")  # Aumenta la dimensione della finestra
        self.root.minsize(1280, 900)
        self.running = False

        # Inizializzazione delle variabili
        self.alpha = 0.5
        self.filtered_roll = 0.0
        self.filtered_pitch = 0.0
        self.filtered_yaw = 0.0
        self.first_attempt = True

        # Dati per il grafico
        self.x_graph = []
        self.y_graph_roll = []
        self.y_graph_pitch = []
        self.y_graph_yaw = []

        # Creazione dei grafici
        self.fig, (self.ax_roll, self.ax_pitch, self.ax_yaw) = plt.subplots(3, 1, sharex=True, figsize=(10, 8))
        self.fig.tight_layout(pad=4.0)

        # Impostazioni dei grafici
        self.setup_plots()

        # Creazione della GUI
        self.create_widgets()

        # Inizializzazione del sensore
        self.sensor_manager = SensorManager(self)

        # Animazione del grafico
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=500, cache_frame_data=False)

    def setup_plots(self):
        self.ax_roll.set_title('Roll', fontsize=14)
        self.ax_roll.set_ylabel('Degrees (radians)', fontsize=12)

        self.ax_pitch.set_title('Pitch', fontsize=14)
        self.ax_pitch.set_ylabel('Degrees (radians)', fontsize=12)

        self.ax_yaw.set_title('Yaw', fontsize=14)
        self.ax_yaw.set_ylabel('Degrees (radians)', fontsize=12)
        self.ax_yaw.set_xlabel('Time', fontsize=12)

    def create_widgets(self):
        # Imposta il tema per ttk
        style = ttk.Style()
        style.theme_use('clam')

        # Personalizza gli stili
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 12))
        style.configure('TButton', font=('Helvetica', 12), padding=6)
        style.configure('TEntry', font=('Helvetica', 12))
        style.configure('TScale', font=('Helvetica', 12))

        # Creazione dei widget della GUI
        frame_connection = ttk.Frame(self.root, padding=(20, 10))
        frame_connection.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # Titolo della sezione sinistra
        ttk.Label(frame_connection, text="Impostazioni di Connessione", font=("Helvetica", 16, 'bold')).grid(row=0, column=0, pady=10, sticky='w')

        # Inserimento dell'IP del dispositivo
        ttk.Label(frame_connection, text="Inserisci l'IP del dispositivo:", font=('Helvetica', 12)).grid(row=1, column=0, pady=5, sticky='w')
        self.ip_entry = ttk.Entry(frame_connection, font=('Helvetica', 12))
        self.ip_entry.grid(row=2, column=0, pady=5, ipady=5, sticky='we')

        # Inserimento dei valori E, N, U
        ttk.Label(frame_connection, text="Inserisci il valore di E (µT):", font=('Helvetica', 12)).grid(row=3, column=0, pady=5, sticky='w')
        self.e_entry = ttk.Entry(frame_connection, font=('Helvetica', 12))
        self.e_entry.grid(row=4, column=0, pady=5, ipady=5, sticky='we')

        ttk.Label(frame_connection, text="Inserisci il valore di N (µT):", font=('Helvetica', 12)).grid(row=5, column=0, pady=5, sticky='w')
        self.n_entry = ttk.Entry(frame_connection, font=('Helvetica', 12))
        self.n_entry.grid(row=6, column=0, pady=5, ipady=5, sticky='we')

        ttk.Label(frame_connection, text="Inserisci il valore di U (µT):", font=('Helvetica', 12)).grid(row=7, column=0, pady=5, sticky='w')
        self.u_entry = ttk.Entry(frame_connection, font=('Helvetica', 12))
        self.u_entry.grid(row=8, column=0, pady=5, ipady=5, sticky='we')

        # Pulsante per ottenere i dati ENU
        link_button = ttk.Button(frame_connection, text="Ottieni i dati ENU", command=self.open_link)
        link_button.grid(row=9, column=0, pady=10, sticky='we')

        # Pulsante per avviare/fermare la connessione
        self.start_button = ttk.Button(frame_connection, text="Start", command=self.toggle_connection)
        self.start_button.grid(row=10, column=0, pady=10, sticky='we')

        # Pulsante per pulire il grafico
        clear_button = ttk.Button(frame_connection, text="Pulisci Grafico", command=self.clear_graph)
        clear_button.grid(row=11, column=0, pady=10, sticky='we')

        # Label per 'Filter β'
        ttk.Label(frame_connection, text='Filter β', font=('Helvetica', 12)).grid(row=12, column=0, pady=5, sticky='w')

        # Slider per il filtro beta
        self.alpha_slider = ttk.Scale(frame_connection, from_=0.0, to=1.0, orient=tk.HORIZONTAL, command=self.update_alpha)
        self.alpha_slider.set(self.alpha)
        self.alpha_slider.grid(row=13, column=0, pady=10, sticky='we')

        # Etichetta che mostra il valore corrente di β
        self.beta_value_label = ttk.Label(frame_connection, text=f"Valore corrente di β: {self.alpha:.2f}", font=('Helvetica', 12))
        self.beta_value_label.grid(row=14, column=0, pady=5, sticky='w')

        # Etichette esplicative per β→1 e β→0 (con testo ingrandito)
        ttk.Label(frame_connection, text='β→1 maggiore effetto filtrante', font=('Helvetica', 12)).grid(row=15, column=0, pady=2, sticky='w')
        ttk.Label(frame_connection, text='β→0 minore effetto filtrante', font=('Helvetica', 12)).grid(row=16, column=0, pady=2, sticky='w')

        # Aggiungi il canvas del grafico
        frame_graph = ttk.Frame(self.root, padding=(20, 10))
        frame_graph.grid(row=0, column=1, sticky='nsew', padx=20, pady=20)

        ttk.Label(frame_graph, text="Dati di Orientamento in Tempo Reale", font=("Helvetica", 16, 'bold')).pack(pady=10)

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_graph)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Imposta il comportamento responsivo
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        frame_connection.grid_columnconfigure(0, weight=1)

        # Gestione della chiusura della finestra
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def animate(self, i):
        if self.running:
            self.x_graph.append(dt.datetime.now())
            self.y_graph_roll.append(self.filtered_roll)
            self.y_graph_pitch.append(self.filtered_pitch)
            self.y_graph_yaw.append(self.filtered_yaw)

            # Limita il numero di punti per evitare sovraccarico
            max_points = 100
            if len(self.x_graph) > max_points:
                self.x_graph = self.x_graph[-max_points:]
                self.y_graph_roll = self.y_graph_roll[-max_points:]
                self.y_graph_pitch = self.y_graph_pitch[-max_points:]
                self.y_graph_yaw = self.y_graph_yaw[-max_points:]

            # Pulisce ciascun subplot
            self.ax_roll.cla()
            self.ax_pitch.cla()
            self.ax_yaw.cla()

            # Grafico per Roll
            self.ax_roll.plot(self.x_graph, self.y_graph_roll, color='blue')
            self.ax_roll.set_title('Roll', fontsize=14)
            self.ax_roll.set_ylabel('Degrees (radians)', fontsize=12)

            # Grafico per Pitch
            self.ax_pitch.plot(self.x_graph, self.y_graph_pitch, color='green')
            self.ax_pitch.set_title('Pitch', fontsize=14)
            self.ax_pitch.set_ylabel('Degrees (radians)', fontsize=12)

            # Grafico per Yaw
            self.ax_yaw.plot(self.x_graph, self.y_graph_yaw, color='red')
            self.ax_yaw.set_title('Yaw', fontsize=14)
            self.ax_yaw.set_ylabel('Degrees (radians)', fontsize=12)
            self.ax_yaw.set_xlabel('Time', fontsize=12)

            # Ruota le etichette dell'asse x
            plt.setp(self.ax_yaw.get_xticklabels(), rotation=45, ha='right')

            # Aggiorna il layout
            self.fig.tight_layout()
            self.canvas.draw()

    def update_alpha(self, val):
        self.alpha = float(val)
        self.beta_value_label.config(text=f"Valore corrente di β: {self.alpha:.2f}")

    def on_closing(self):
        self.sensor_manager.stop()
        self.root.quit()

    def run(self):
        self.root.mainloop()

    def toggle_connection(self):
        if not self.running:
            # Avvia la connessione
            try:
                self.sensor_manager.E = float(self.e_entry.get())
                self.sensor_manager.N = float(self.n_entry.get())
                self.sensor_manager.U = float(self.u_entry.get())  # Anche se U non viene utilizzato
            except ValueError:
                messagebox.showwarning("Errore di Input", "Per favore inserisci numeri validi per E, N e U.")
                return

            device_ip = self.ip_entry.get()
            if not device_ip:
                messagebox.showwarning("Errore di Input", "Per favore inserisci un indirizzo IP valido.")
                return

            url = f"{device_ip}/sensors/connect?types=[\"android.sensor.accelerometer\",\"android.sensor.gyroscope\",\"android.sensor.magnetic_field\"]"
            self.sensor_manager.connect(url)
            self.running = True
            self.start_button.config(text="Stop")
        else:
            # Ferma la connessione
            self.sensor_manager.stop()
            self.running = False
            self.start_button.config(text="Start")

    def clear_graph(self):
        # Pulisce i dati del grafico
        self.x_graph = []
        self.y_graph_roll = []
        self.y_graph_pitch = []
        self.y_graph_yaw = []

        # Pulisce ciascun subplot
        self.ax_roll.cla()
        self.ax_pitch.cla()
        self.ax_yaw.cla()

        # Reimposta le etichette
        self.setup_plots()

        # Aggiorna il layout
        self.fig.tight_layout()
        self.canvas.draw()

    def open_link(self):
        import webbrowser
        webbrowser.open("https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml#igrfwmm")
