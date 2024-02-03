#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python is not installed. Please install Python."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &>/dev/null; then
    echo "Pip is not installed. Installing pip..."
    sudo apt update
    sudo apt install python3-pip -y
fi

# Check for requirements file
if [ -f requirements.txt ]; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
else
    echo "No requirements.txt file found. Skipping installation of dependencies."
fi


chmod u+x trovappello
sudo mv trovappello /usr/local/bin/trovappello


