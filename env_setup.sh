#!/bin/bash

# Script for setting up Python environment and cloning Git repository on Raspberry Pi
# do ths in the project dir

echo -e "Checking Python Version...Must be 3.9!"
python3 -V 

echo -e "Upgrading Pip..."
python3 -m pip install --upgrade pip

echo -e "Installing and creating virtual environment 'env'..."
sudo -H python3 -m pip install virtualenv || { echo "Failed to install virtualenv"; }
python3 -m virtualenv env || { echo "Failed to create virtual environment";}

echo -e "Activating virtual environment..."
source env/bin/activate || { echo "Failed to activate virtual environment"; }

echo -e "Installing requirements via pip..."
pip install -r requirements.txt || { echo "Failed to install requirements";}

echo -e "Setup completed successfully!"
