import streamlit as st
import serial
import time
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load the MP3 file
sound_path = "squid.mp3"  # Replace with the full path to your sound file
try:
    pygame.mixer.music.load(sound_path)
except pygame.error as e:
    st.error(f"Could not load the sound file: {e}")

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

def toggle_sweeper_with_sound():
    """Send 'toggle_sweeper' command, wait 5 seconds, then play a sound."""
    pygame.mixer.music.play()  # Play the loaded sound
    time.sleep(5)  # Wait for 5 seconds
    send_command('toggle_sweeper')  # Send the command to the Arduino

st.title("Arduino Servo Controller")

if st.button("Activate Jawharino"):
    send_command('true')

if st.button("Toggle Sweeper"):
    toggle_sweeper_with_sound()

st.write("Click buttons to control the Arduino. Make sure it's connected to the correct port.")

if arduino:
    arduino.close()
