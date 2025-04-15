# IoT4Ag Hackathon Project 2025 - Remote Sensor Station

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
[![GitHub](https://img.shields.io/badge/GitHub-ucmercedrobotics-181717.svg?style=flat&logo=github)](https://github.com/ucmercedrobotics)
[![Website](https://img.shields.io/badge/Website-UCMRobotics-5087B2.svg?style=flat&logo=telegram)](https://robotics.ucmerced.edu/)
[![Python](https://img.shields.io/badge/Python-3.10.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

---

## Overview

This project was built during the **IoT4Ag Hackathon 2025**, hosted by UC Merced and the USDA-funded IoT4Ag Center. Our goal: design a **low-power, long-range, modular sensor station** for remote agricultural monitoring.

Using **LoRa communication**, **Protocol Buffers**, and **real-time dashboards**, we developed a wireless system to collect and transmit environmental data—like CO2, temperature, and altitude—from a base station to a remote dashboard.

---

## Impact

Traditional sensor deployments can be **costly and hard to maintain** in large fields. By using **LoRa** (Long Range, Low Power), we enable farmers and researchers to:
- Deploy sensors in **remote locations** without relying on cellular or Wi-Fi
- **Visualize conditions in real time** from any location
- **Extend battery life** thanks to LoRa’s low energy footprint

This is a step toward scalable, intelligent agriculture infrastructure.

---

## Example Data Packet
```bash
[Sending Sensor Packet] 
Timestamp : 1744511744.0 
CO2 : 395 
Temperature : 16.57 C 
Pressure : 102247.7 Pa 
Altitude : 175.4 m 
Humidity : 36.65 % 
Thermal Row 0: [13.52, 12.75, 11.76, ...]
```

---

## Tech Stack

- **LoRa** for long-range wireless transmission
- **Arduino MKR WAN 1310** for LoRa
- **Teensy board** with environmental sensors
- **Protocol Buffers (protobuf)** for compact, efficient data serialization
- **Flask + JavaScript + Chart.js** for web dashboard
- **Docker** for streamlined simulation environment

---

## Getting Started (Simulation Mode)

### Prerequisites
- Docker Desktop
- Make (`choco install make` on Windows)
- [Ncat](https://nmap.org/ncat/) (for testing TCP streaming)

### Run Simulation
1. **Terminal 1: Start TCP listener**
   ```bash
   ncat -l -p 12347  # (Linux/macOS)
   "C:\Program Files (x86)\Nmap\ncat.exe" -l -p 12347  # (Windows)
   ```
2. Terminal 2: Start Dockerized sensor stream: Run `make prod`

---

## Data Format

### TCP + Protobuf Layout

| Field   | Bytes | Description                    |
|---------|--------|--------------------------------|
| Header  | 4      | Length of Protobuf payload     |
| Payload | Varies | Protobuf-encoded sensor data   |

### Protobuf Schema

| Field            | Type     | Description                 |
|------------------|----------|-----------------------------|
| timestamp        | float    | Time from epoch             |
| co2              | int32    | CO2 level (ppm)             |
| bme_temperature  | float    | Temperature (°C)            |
| bme_pressure     | float    | Pressure (Pa)               |
| bme_altitude     | float    | Altitude (m)                |
| bme_humidity     | float    | Humidity (%)                |
| thermal.row[]    | float[]  | 2D array of pixel temps     |

---

## LoRa Transmission Format

### Sensor Station (Transmission)

| Field           | Type     | Length    | Notes                                      |
|------------------|----------|-----------|--------------------------------------------|
| Sync Marker      | uint8[]  | 2 bytes   | Header ID                                  |
| Message Length   | uint8[]  | 2 bytes   | Length of payload (little endian)          |
| Packet Payload   | byte[]   | Variable  | Protobuf-encoded sensor data               |

### LoRa Chunk (per packet)

| Field         | Type   | Length      | Description                          |
|---------------|--------|-------------|--------------------------------------|
| Chunk Index   | uint8  | 1 byte      | Index of this chunk                  |
| Total Chunks  | uint8  | 1 byte      | Total number of chunks               |
| Chunk Payload | byte[] | ≤253 bytes  | Part of Protobuf packet              |

> **Note:** Protobuf chunks must be reassembled before decoding.

---

## Arduino Setup

| Component        | Description                                                        |
|------------------|---------------------------------------------------------------------|
| **Sender** | Reads serial data from Teensy board<br>Chunks it and sends via LoRa |
| **Receiver** | Listens for incoming LoRa packets<br>Reassembles and forwards raw bytes to host PC via Serial (COM3) |
| **Backend (Python)** | Listens to COM3<br>Deserializes and parses Protobuf packets<br>Feeds live Flask API to dashboard |

---

## Status
- ✅ Protobuf Streaming
- ✅ Serial Listener & Decoder
- ✅ Flask Backend + API
- ✅ Chart.js Dashboard (Mock Data)
- ❌ Full integration of live hardware-to-frontend

---

## Credits
- Built during the IoT4Ag Hackathon 2025 at UC Merced
- Special thanks to Marcos S., our mentor and event organizer

---

### Read the full technical recap [here](https://laith.vercel.app/blog/iot4ag-hackathon.html/)