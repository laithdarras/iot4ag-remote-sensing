import serial
import struct
import threading
import time
import sensor_pb2

SERIAL_PORT = "COM3"
BAUD_RATE = 115200
latest_data = None

def get_latest_data():
    return latest_data

def _read_packet(ser):
    try:
        header = ser.read(4)
        if len(header) < 4:
            return None
        packet_len = struct.unpack(">I", header)[0]
        if packet_len <= 0 or packet_len > 1024:
            print(f"[Packet Error] Invalid length: {packet_len}")
            return None
        payload = ser.read(packet_len)
        if len(payload) != packet_len:
            print(f"[Packet Error] Incomplete payload: got {len(payload)}, expected {packet_len}")
            return None
        return payload
    except Exception as e:
        print(f"[Read Error] {e}")
        return None

def _decode_protobuf(payload):
    try:
        sensor_data = sensor_pb2.SensorData()
        sensor_data.ParseFromString(payload)
        return sensor_data
    except Exception as e:
        print(f"[Decode Error] {e}")
        return None

def _print_sensor_data(sensor_data):
    print("======== [Sensor Data Packet] ========")
    print(f"CO2 (ppm)      : {sensor_data.co2}")
    print(f"Temperature    : {sensor_data.bme_temperature:.2f} C")
    print(f"Pressure       : {sensor_data.bme_pressure:.2f} Pa")
    print(f"Altitude       : {sensor_data.bme_altitude:.2f} m")
    print(f"Humidity       : {sensor_data.bme_humidity:.2f} %")
    if sensor_data.row:
        print(f"Thermal Pixels : {list(sensor_data.row[0].pixel_temp)[:6]} ...")
    print("======================================\n")

def _serial_thread():
    global latest_data
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"[Serial] Connected to {SERIAL_PORT} at {BAUD_RATE}")
    except Exception as e:
        print(f"[Serial Init Failed] {e}")
        return

    while True:
        packet = _read_packet(ser)
        if packet:
            data = _decode_protobuf(packet)
            if data:
                latest_data = data
                _print_sensor_data(data)

def start_serial_listener():
    t = threading.Thread(target=_serial_thread, daemon=True)
    t.start()