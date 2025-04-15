import serial

try:
    ser = serial.Serial("COM3", 115200, timeout=1)
    print("Serial connection to COM3 successful.")
    ser.close()
except Exception as e:
    print(f"Serial connection failed: {e}")