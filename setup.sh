#!/bin/bash

# DevToolkit Setup Script
# This script initializes the development environment and installs required dependencies

# Exit on any error
set -e

echo "🚀 Starting DevToolkit Setup..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print status messages
print_status() {
    echo "📝 $1"
}

# Check for required system tools
print_status "Checking system requirements..."

# Check for Python 3
if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check for pip
if ! command_exists pip3; then
    print_status "Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# Check for git
if ! command_exists git; then
    echo "❌ Git is required but not installed. Please install Git and try again."
    exit 1
fi

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
print_status "Creating project structure..."
mkdir -p {config,logs,data,tests}

# Copy default configuration files
print_status "Setting up configuration files..."
if [ ! -f "config/general.yaml" ]; then
    cp config/general.yaml.example config/general.yaml
fi

# Set up git hooks
print_status "Setting up git hooks..."
if [ -d ".git" ]; then
    cp git-hooks/* .git/hooks/
    chmod +x .git/hooks/*
fi

# Initialize logging
print_status "Initializing logging..."
touch logs/devtoolkit.log

# Final setup steps
print_status "Running final setup steps..."
python3 scripts/post_setup.py

echo "✅ DevToolkit setup completed successfully!"
echo "🔧 To start using DevToolkit:"
echo "   1. Activate the virtual environment: source .venv/bin/activate"
echo "   2. Review the configuration in config/general.yaml"
echo "   3. Run 'python3 -m pytest tests/' to verify the installation"
echo "📚 For more information, see the documentation in docs/"
