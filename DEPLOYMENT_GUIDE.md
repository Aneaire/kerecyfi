# RecyFi Deployment Guide

## Overview
This guide walks you through deploying the RecyFi system on your Orange Pi and setting up the complete recycling kiosk with Wi-Fi voucher functionality.

## Prerequisites
- Orange Pi with Armbian installed
- Network connection (Ethernet or Wi-Fi)
- SSH access to Orange Pi
- Development machine with the RecyFi codebase

## Step 1: Test the Server Locally

First, verify the Flask server works on your development machine:

```bash
# Install server dependencies
pip install -r server/requirements.txt

# Run the server
cd server && python3 app.py
```

Test the server by opening `http://localhost:80` in your browser and clicking "Simulate Insert Plastic".

## Step 2: Connect to Orange Pi

Establish SSH connection to your Orange Pi:

```bash
# Using sshpass (if available)
sshpass -p 'ken' ssh root@<ORANGE_PI_IP>

# Or standard SSH
ssh root@<ORANGE_PI_IP>
```

**Note**: Replace `<ORANGE_PI_IP>` with the actual IP address of your Orange Pi.

## Step 3: Deploy Code to Orange Pi

Copy the RecyFi codebase to the Orange Pi:

```bash
# From your development machine
scp -r /home/aneaire/Desktop/CODES/rekrecyfy root@<ORANGE_PI_IP>:/home/root/
```

Or use rsync for faster transfers:
```bash
rsync -av /home/aneaire/Desktop/CODES/rekrecyfy/ root@<ORANGE_PI_IP>:/home/root/rekrecyfy/
```

## Step 4: Run Setup Scripts on Orange Pi

Once connected to the Orange Pi, navigate to the project directory and run the setup scripts:

```bash
# Navigate to project directory
cd /home/root/rekrecyfy

# Make scripts executable
chmod +x scripts/*.sh

# Run client setup (installs Python dependencies, creates services)
bash scripts/setup_client.sh

# Run AP setup (configures Wi-Fi access point)
bash scripts/setup_orange_pi.sh
```

## Step 5: Configure Network Settings

### Update Server URL
Edit the client configuration to point to your server:

```bash
nano /home/orange_pi/client/orange_pi_client.py
```

Change `SERVER_URL` from `"http://localhost:80"` to your actual server IP:
```python
SERVER_URL = "http://<YOUR_SERVER_IP>:80"
```

### Verify Network Connectivity
Test connectivity from Orange Pi to server:
```bash
ping <YOUR_SERVER_IP>
curl http://<YOUR_SERVER_IP>:80
```

## Step 6: Hardware Setup

### GPIO Pin Connections
Connect your hardware components according to these pin assignments:

- **Green LED** (Plastic accepted): GPIO 17
- **Blue LED** (Access granted): GPIO 27  
- **Red LED** (Error/Denied): GPIO 22
- **Plastic Sensor**: GPIO 18

### Wiring Example
```
Orange Pi GPIO 17 → 220Ω resistor → Green LED → GND
Orange Pi GPIO 27 → 220Ω resistor → Blue LED → GND
Orange Pi GPIO 22 → 220Ω resistor → Red LED → GND
Orange Pi GPIO 18 → Plastic sensor input
```

## Step 7: Start Services

### Manual Testing
Test the client manually first:

```bash
cd /home/orange_pi/client
source /home/orange_pi/recyfi_env/bin/activate
python3 orange_pi_client.py
```

### Service Management
The setup script creates a systemd service. Manage it with:

```bash
# Check service status
sudo systemctl status recyfi-client

# Start service
sudo systemctl start recyfi-client

# Stop service  
sudo systemctl stop recyfi-client

# View logs
journalctl -u recyfi-client -f
```

## Step 8: Test Complete System

### Test Workflow
1. **Start the server** on your development machine or another device
2. **Connect to Orange Pi** via SSH
3. **Run the client** (or ensure service is running)
4. **Test plastic insertion** using the client menu
5. **Verify LED responses** and server communication
6. **Test voucher validation** through the web portal

### Expected Behavior
- Green LED lights when plastic is "inserted"
- Server generates and stores voucher
- Blue LED lights for successful voucher validation
- Red LED indicates errors or invalid vouchers

## Step 9: Configure Access Point

The Orange Pi should now be broadcasting a Wi-Fi network named "RecyFi":

- **SSID**: RecyFi
- **Password**: recyfi123
- **IP Range**: 192.168.100.10-100

Connect a device to this network and navigate to any website to see the captive portal.

## Troubleshooting

### Common Issues

**SSH Connection Failed**
```bash
# Check if SSH is running
sudo systemctl status ssh

# Enable SSH if needed
sudo systemctl enable ssh
sudo systemctl start ssh
```

**GPIO Library Not Found**
The system will fall back to simulation mode if `OPi.GPIO` is not available. Install with:
```bash
pip install OPi.GPIO
```

**Service Won't Start**
```bash
# Check service logs
journalctl -u recyfi-client -n 50

# Check Python environment
source /home/orange_pi/recyfi_env/bin/activate
python3 -c "import requests; print('OK')"
```

**Network Issues**
```bash
# Check network interfaces
ip addr show

# Test connectivity
ping 8.8.8.8
```

### Log Files
- **Client logs**: `/home/orange_pi/logs/client.log`
- **Server logs**: Console output when running `python3 app.py`
- **System logs**: `journalctl -u recyfi-client`

## Production Deployment

For production use:

1. **Secure the system** - Change default passwords
2. **Configure firewall** - Only allow necessary ports
3. **Set up monitoring** - Monitor service health
4. **Backup configuration** - Save working configs
5. **Document network** - Record IP addresses and settings

## Next Steps

Once deployed, you can:

1. **Add real sensors** - Connect actual plastic detection hardware
2. **Enhance UI** - Improve the web portal interface  
3. **Add analytics** - Track usage statistics
4. **Implement admin panel** - Manage vouchers and users
5. **Add payment integration** - Optional paid access extensions

## Support

For issues:
1. Check log files for error messages
2. Verify network connectivity
3. Ensure all dependencies are installed
4. Test components individually before integration

---

**Congratulations!** Your RecyFi kiosk should now be fully operational and ready to provide Wi-Fi access in exchange for plastic recycling.