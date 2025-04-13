import streamlit as st
import numpy as np
import cv2
import time
from collections import deque
from sensor_client import receive_sensor_data
import protobuf.sensor_pb2 as sensor_pb2

# Session state for storing data
if "temp_vals" not in st.session_state:
    st.session_state.temp_vals = deque(maxlen=100)
    st.session_state.timestamps = deque(maxlen=100)
    st.session_state.humidity_vals = deque(maxlen=100)
    st.session_state.co2_vals = deque(maxlen=100)

st.title("🛰️ Sensor Station Dashboard")
chart_temp = st.line_chart()
chart_humidity = st.line_chart()
chart_co2 = st.line_chart()
thermal_placeholder = st.empty()

def display_thermal_image(sensor_data):
    if len(sensor_data.row) > 0:
        thermal_array = np.array([[pixel for pixel in row.pixel_temp] for row in sensor_data.row], dtype=np.float32)
        thermal_normalized = cv2.normalize(thermal_array, None, 0, 255, cv2.NORM_MINMAX)
        thermal_uint8 = np.uint8(thermal_normalized)
        color_thermal = cv2.applyColorMap(thermal_uint8, cv2.COLORMAP_JET)
        thermal_placeholder.image(color_thermal, channels="BGR", caption="Thermal Camera View")

sensor_stream = receive_sensor_data()

for data in sensor_stream:
    # Store data
    st.session_state.temp_vals.append(data.bme_temperature)
    st.session_state.humidity_vals.append(data.bme_humidity)
    st.session_state.co2_vals.append(data.co2)
    st.session_state.timestamps.append(time.strftime('%H:%M:%S', time.localtime(data.timestamp)))

    # Update charts
    chart_temp.line_chart(list(st.session_state.temp_vals))
    chart_humidity.line_chart(list(st.session_state.humidity_vals))
    chart_co2.line_chart(list(st.session_state.co2_vals))

    # Show thermal
    display_thermal_image(data)

    # Sleep to let UI update
    time.sleep(1)
