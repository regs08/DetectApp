#!/bin/bash

# Script to update, upgrade and install necessary packages on Raspberry Pi

echo -e "Starting system update and upgrade..."
sudo apt-get update && sudo apt-get upgrade -y || { echo "Update or upgrade failed"; exit 1; }

echo -e "Installing MQTT..."
sudo apt-get install -y mosquitto mosquitto-clients || { echo "MQTT installation failed"; exit 1; }
# Enable and start MQTT service
sudo systemctl enable mosquitto.service
sudo systemctl start mosquitto.service

echo -e "Installing libraries and dependencies..."
sudo apt-get install -y libatlas-base-dev libopenblas-dev || { echo "Library installation failed"; exit 1; }

# Instructions for modifying MQTT configuration
echo -e "Modify the MQTT configuration file:"
echo -e "Open the file with: sudo nano /etc/mosquitto/mosquitto.conf"
echo -e "Add the following lines to the end of the file:"
echo -e "listener 1883"
echo -e "allow_anonymous true"
echo -e ""

# Camera check (This is a placeholder. You need to replace it with actual check or instructions.)
echo -e "MAKE SURE CAMERA IS ENABLED!"
# Add here your camera check script or instructions on how to enable the camera

echo -e "Setup completed successfully!"
