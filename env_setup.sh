#!/bin/bash

# Script for setting up Python environment and cloning Git repository on Raspberry Pi

echo -e "Checking Python Version..."
python3 -V || { echo "Python3 is not installed"; exit 1; }

echo -e "Making and changing directories..."
mkdir -p project
cd project || { echo "Failed to create or move to 'project' directory"; exit 1; }

echo -e "Cloning Git Repository..."
git clone https://github.com/regs08/DetectApp.git || { echo "Failed to clone repository"; exit 1; }
cd DetectApp || { echo "Failed to move to 'DetectApp' directory"; exit 1; }

echo -e "Installing and creating virtual environment 'env'..."
sudo -H python3 -m pip install virtualenv || { echo "Failed to install virtualenv"; exit 1; }
python3 -m virtualenv env || { echo "Failed to create virtual environment"; exit 1; }

echo -e "Activating virtual environment..."
source env/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

echo -e "Installing requirements via pip..."
pip install -r requirements.txt || { echo "Failed to install requirements"; exit 1; }

echo -e "Setup completed successfully!"
