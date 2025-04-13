import time
import socket
import argparse

import yaml

from sensors.co2 import CO2SensorEmulator
from sensors.temperature import TempSensorEmulator
from sensors.pressure import PressureSensorEmulator
from sensors.altitude import AltitudeSensorEmulator
from sensors.humidity import HumiditySensorEmulator
from sensors.thermalcamera import ThermalCameraSensorEmulator

import sensor_pb2

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sensor Station Argparser")
    parser.add_argument(
        "--config",
        type=str,
        help="Sensor Station YAML config file",
        default="app/config/config.yaml",
    )

    args = parser.parse_args()

    with open(args.config, "r") as file:
        config = yaml.safe_load(file)

    # initialize TCP socket connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect((config["host"], config["port"]))

    temp_sensor = TempSensorEmulator()
    co2_sensor = CO2SensorEmulator()
    pressure_sensor = PressureSensorEmulator()
    altitude_sensor = AltitudeSensorEmulator()
    humidity_sensor = HumiditySensorEmulator()
    thermal_camera_sensor = ThermalCameraSensorEmulator()

    while True:
        sensor_data = sensor_pb2.SensorData()

        time.sleep(1)
        temp = temp_sensor.read_temp()
        co2 = co2_sensor.read_co2()
        pressure = pressure_sensor.read_pa()
        alt = altitude_sensor.read_alt()
        humidity = humidity_sensor.read_rh()
        thermal_image = thermal_camera_sensor.read_image()
        # protobuf construction
        sensor_data.timestamp = time.time()
        sensor_data.co2 = co2
        sensor_data.bme_temperature = temp
        sensor_data.bme_pressure = pressure
        sensor_data.bme_altitude = alt
        sensor_data.bme_humidity = humidity
        for row in thermal_image:
            new_row = sensor_data.row.add()
            new_row.pixel_temp.extend(row)

        print("\n[Sending Sensor Packet]")
        print("\n[Sending Sensor Packet]")
        print(f"  Timestamp       : {sensor_data.timestamp}")
        print(f"  CO2             : {sensor_data.co2}")
        print(f"  Temperature     : {sensor_data.bme_temperature}")
        print(f"  Pressure        : {sensor_data.bme_pressure}")
        print(f"  Altitude        : {sensor_data.bme_altitude}")
        print(f"  Humidity        : {sensor_data.bme_humidity}")
        print(f"  Thermal Row 0   : {sensor_data.row[0].pixel_temp[:5]}..." if sensor_data.row else "  No thermal data")
        encoded_data = sensor_data.SerializeToString()

        # header data of packet length
        msg_length = len(encoded_data).to_bytes(4, byteorder="big")

        client_socket.sendall(msg_length + encoded_data)

    client_socket.close()
