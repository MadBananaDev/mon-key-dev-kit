#!/bin/bash

# Setup script for DevToolkit

# Exit immediately if a command exits with a non-zero status
set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Python
if ! command_exists python3; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check for pip
if ! command_exists pip3; then
    echo "pip3 is not installed. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# Check for virtualenv
if ! command_exists virtualenv; then
    echo "virtualenv is not installed. Installing virtualenv..."
    pip3 install virtualenv
fi

# Create a virtual environment
echo "Creating a virtual environment..."
virtualenv devtoolkit_env

# Activate the virtual environment
source devtoolkit_env/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Install system dependencies (example for Ubuntu/Debian)
if command_exists apt-get; then
    echo "Installing system dependencies..."
    sudo apt-get update
    sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev
fi

# Install additional tools
echo "Installing additional development tools..."
pip install jupyter black flake8 mypy

# Create a simple test to verify installation
echo "import sys
import requests
import matplotlib
import numpy
import PIL
import radon
import flask
import 
