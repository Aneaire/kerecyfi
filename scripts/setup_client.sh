#!/bin/bash
# Setup script for Orange Pi RecyFi client

echo "Setting up Orange Pi for RecyFi client..."

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
echo "Installing Python dependencies..."
sudo apt install -y python3 python3-pip python3-venv

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv /home/orange_pi/recyfi_env
source /home/orange_pi/recyfi_env/bin/activate

# Install Python packages
echo "Installing Python packages..."
pip install requests

# Try to install Orange Pi GPIO library
echo "Installing Orange Pi GPIO library..."
pip install OPi.GPIO || echo "GPIO library installation failed - will use simulation mode"

# Create directories
echo "Creating directories..."
mkdir -p /home/orange_pi/logs
mkdir -p /home/orange_pi/client

# Copy client files (assuming they're in the current directory)
echo "Copying client files..."
cp -r client/* /home/orange_pi/client/
cp -r scripts/* /home/orange_pi/

# Set permissions
echo "Setting permissions..."
chmod +x /home/orange_pi/client/*.py
chmod +x /home/orange_pi/scripts/*.sh

# Create systemd service for auto-start
echo "Creating systemd service..."
sudo tee /etc/systemd/system/recyfi-client.service > /dev/null <<EOF
[Unit]
Description=RecyFi Client Service
After=network.target

[Service]
Type=simple
User=orange_pi
WorkingDirectory=/home/orange_pi/client
Environment=PATH=/home/orange_pi/recyfi_env/bin
ExecStart=/home/orange_pi/recyfi_env/bin/python3 orange_pi_client.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
echo "Enabling RecyFi client service..."
sudo systemctl daemon-reload
sudo systemctl enable recyfi-client.service
sudo systemctl start recyfi-client.service

echo "Setup complete!"
echo "Check service status with: sudo systemctl status recyfi-client"
echo "View logs with: journalctl -u recyfi-client -f"