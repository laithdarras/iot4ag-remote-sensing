import threading
import socket
import struct
from queue import Queue
from flask import Flask, jsonify, render_template
from serial_receiver import get_latest_data, start_serial_listener
import sensor_pb2

# Flask app
app = Flask(__name__,
            template_folder="templates",
            static_folder="static"
            )

# Shared data storage
data_queue = Queue()
latest_data = None

# TCP listener function
def tcp_listener(host='127.0.0.1', port=12347):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"TCP Server listening on {host}:{port}...")

        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            with conn:
                try:
                    while True:
                        # Read 4-byte header
                        header = conn.recv(4)
                        if len(header) < 4:
                            print("Incomplete header received.")
                            break
                        packet_len = struct.unpack('>I', header)[0]

                        # Sanity check
                        if packet_len <= 0 or packet_len > 10**6:
                            print(f"Invalid packet length: {packet_len}")
                            break

                        # Read payload
                        payload = b''
                        while len(payload) < packet_len:
                            chunk = conn.recv(packet_len - len(payload))
                            if not chunk:
                                print("Connection closed during payload reception.")
                                break
                            payload += chunk

                        if len(payload) != packet_len:
                            print("Incomplete payload received.")
                            break

                        # Deserialize protobuf
                        sensor_data = sensor_pb2.SensorData()
                        sensor_data.ParseFromString(payload)
                        data_queue.put(sensor_data)

                except Exception as e:
                    print(f"[tcp_listener] Error: {e}")
                    continue

# Thread to update the latest data
def data_updater():
    global latest_data
    while True:
        latest_data = data_queue.get()

# Flask routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def get_data():
    data = get_latest_data()
    if data:
        return jsonify({
            "timestamp": data.timestamp,
            "co2": data.co2,
            "bme_temperature": data.bme_temperature,
            "bme_pressure": data.bme_pressure,
            "bme_altitude": data.bme_altitude,
            "bme_humidity": data.bme_humidity,
            "thermal": [list(row.pixel_temp) for row in data.row]
        })
    return jsonify({"error": "No data available"}), 404


if __name__ == "__main__":
    # start_serial_listener()  # Start reading from Arduino
    app.run(host="0.0.0.0", port=5000, debug=True)
