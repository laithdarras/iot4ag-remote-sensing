FROM python:3.10.12 AS builder
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

FROM python:3.10.12 AS base

COPY --from=builder /usr/local /usr/local

RUN apt update && \
    apt install -y protobuf-compiler

WORKDIR /sensor-station

COPY app/ ./app
COPY protobuf/ ./protobuf

RUN protoc --python_out=app/ protobuf/sensor.proto

FROM base AS prod

WORKDIR /sensor-station

CMD ["python3", "app/sensorstation.py"]
