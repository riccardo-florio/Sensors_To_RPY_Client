# sensors.py
import websocket
import json
import threading
import numpy as np
import math
from utils import normalize_angle

class SensorManager:
    def __init__(self, app):
        self.app = app
        self.ws = None
        self.running = False
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.E = 0.0
        self.N = 0.0
        self.U = 0.0  # Anche se U non viene utilizzato

    def connect(self, url):
        self.ws = websocket.WebSocketApp(url,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def on_open(self, ws):
        self.running = True
        print("Connected to sensor")

    def on_message(self, ws, message):
        values = json.loads(message)['values']
        sensor_type = json.loads(message)['type']

        if sensor_type == 'android.sensor.accelerometer':
            a_sx, a_sy, a_sz = values
            self.roll = math.atan2(a_sy, a_sz)
            self.pitch = math.atan2(a_sx, math.sqrt(a_sy ** 2 + a_sz ** 2))

        if sensor_type == 'android.sensor.magnetic_field':
            m_sx, m_sy, m_sz = values
            alpha_mf = m_sx * math.cos(self.pitch) + (m_sz * math.cos(self.roll) + m_sy * math.sin(self.roll)) * math.sin(self.pitch)
            beta_mf = m_sx * math.sin(self.roll) - m_sy * math.cos(self.roll)
            matr = np.array([[alpha_mf, beta_mf], [-beta_mf, alpha_mf]])
            try:
                matr_inv = np.linalg.inv(matr)
                vett = np.array([self.E, self.N])
                ris = np.dot(matr_inv, vett)
                c_y, s_y = ris[0], ris[1]
                self.yaw = math.atan2(c_y, s_y)
            except np.linalg.LinAlgError:
                print("Matrix inversion failed due to a singular matrix.")
                return

        # Applica il filtro
        if self.app.first_attempt:
            self.app.filtered_roll = self.roll
            self.app.filtered_pitch = self.pitch
            self.app.filtered_yaw = self.yaw
            self.app.first_attempt = False
        else:
            alpha = self.app.alpha
            self.app.filtered_roll = alpha * self.app.filtered_roll + (1 - alpha) * self.roll
            self.app.filtered_pitch = alpha * self.app.filtered_pitch + (1 - alpha) * self.pitch
            self.app.filtered_yaw = alpha * self.app.filtered_yaw + (1 - alpha) * self.yaw

        # Normalizza gli angoli
        self.app.filtered_roll = normalize_angle(self.app.filtered_roll)
        self.app.filtered_pitch = normalize_angle(self.app.filtered_pitch)
        self.app.filtered_yaw = normalize_angle(self.app.filtered_yaw)

        print("Filtered Roll = {:.4f}, Pitch = {:.4f}, Yaw = {:.4f}".format(
            self.app.filtered_roll, self.app.filtered_pitch, self.app.filtered_yaw))

    def on_error(self, ws, error):
        print("Error:", error)

    def on_close(self, ws, close_code, reason):
        self.running = False
        print("Connection closed")

    def stop(self):
        if self.ws:
            self.ws.close()
