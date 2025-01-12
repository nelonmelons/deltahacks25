import streamlit as st
import serial
import time

try:
    arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)  # Replace 'COM4' with your Arduino's port
except serial.SerialException:
    st.error("Could not connect to the Arduino. Check the port and connection.")
    arduino = None

def send_command(command):
    """Send a command to the Arduino."""
    if arduino:
        arduino.write((command + '\n').encode())  # Send command as bytes
        time.sleep(0.1)  # Give Arduino time to process
        st.write(f"Command '{command}' sent to Arduino!")

st.title("Arduino Servo Controller")

if st.button("Activate Jawharino"):
    send_command('true')

if st.button("Toggle Sweeper"):
    send_command('toggle_sweeper')

st.write("Click buttons to control the Arduino. Make sure it's connected to the correct port.")

if arduino:
    arduino.close()
