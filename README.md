# 3D Triangular Prism Control via MPU6050

Control a 3D triangular prism using an Arduino MPU6050 sensor via Bluetooth. The prism rotates in real-time based on the sensor orientation.

## Features
- Real-time 3D visualization with Pygame
- MPU6050 accelerometer-controlled rotation
- Automatic COM port detection
- Smooth 60 FPS animation

## Requirements
- Arduino + MPU6050 + Bluetooth module
- Python 3.x
- Libraries: `pygame`, `pyserial`

## Setup
1. Connect MPU6050 and Bluetooth to Arduino.
2. Upload Arduino code (`arduino_mpu6050.ino`).
3. Run `triangular_prism.py`.
4. Select the Arduino COM port when prompted.
5. Tilt Arduino to rotate the prism.

## Files
- `triangular_prism.py` → Python visualization
- `arduino_mpu6050.ino` → Arduino MPU6050 + Bluetooth code
