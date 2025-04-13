import socket
import time
import protobuf.sensor_pb2 as sensor_pb2

def receive_sensor_data(host='localhost', port=12347):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.settimeout(5)

    while True:
        try:
            data_len_bytes = sock.recv(4)
            if not data_len_bytes:
                break
            msg_len = int.from_bytes(data_len_bytes, byteorder='big')

            data = b''
            while len(data) < msg_len:
                packet = sock.recv(msg_len - len(data))
                if not packet:
                    break
                data += packet

            sensor_data = sensor_pb2.SensorData()
            sensor_data.ParseFromString(data)
            yield sensor_data

        except Exception as e:
            print(f"Error receiving sensor data: {e}")
            break
