#!/bin/bash

LOG_FILE="/var/log/devtoolkit_setup.log"
exec > >(tee -a $LOG_FILE) 2>&1
echo "Setup started at $(date)"

# Setup script for DevToolkit
# Load configuration
config_file="config/general.yaml"
if [ -f "$config_file" ]; then
    eval $(parse_yaml "$config_file")
else
    echo "Configuration file not found: $config_file"
    exit 1
fi

install_package() {
    if ! dpkg -l | grep -q "$1"; then
        echo "Installing $1..."
        sudo apt-get install -y "$1" || { echo "Failed to install $1"; exit 1; }
    else
        echo "$1 is already installed."
    fi
}
# Function to update configuration
update_config() {
    local key=$1
    local value=$2
    local file=$3
    sed -i "s|^$key:.*|$key: $value|" $file
}

# Interactive configuration update
update_interactive_config() {
    echo "Current configuration:"
    cat $config_file
    echo
    read -p "Enter the key to update (or 'q' to quit): " key
    if [ "$key" != "q" ]; then
        read -p "Enter the new value for $key: " value
        update_config $key "$value" $config_file
        echo "Configuration updated."
        update_interactive_config
    fi
}

# ... (rest of the script)

# Add option to update configuration
echo "Do you want to update the configuration? (y/n)"
read update_config_choice
if [ "$update_config_choice" = "y" ]; then
    update_interactive_config
fi

echo "DevToolkit setup completed. Activate the virtual environment with 'source devtoolkit_env/bin/activate'"
