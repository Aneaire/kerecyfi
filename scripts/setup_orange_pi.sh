#!/bin/bash
# Setup script for Orange Pi (Armbian)

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y hostapd dnsmasq opennds iptables-persistent python3-flask

# Enable services
sudo systemctl enable hostapd dnsmasq opennds

# Configure hostapd for AP
sudo tee /etc/hostapd/hostapd.conf > /dev/null <<EOF
interface=wlan0
driver=nl80211
ssid=RecyFi
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=recyfi123
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

# Configure dnsmasq
sudo tee /etc/dnsmasq.conf > /dev/null <<EOF
interface=wlan0
dhcp-range=192.168.100.10,192.168.100.100,255.255.255.0,12h
dhcp-option=3,192.168.100.1
dhcp-option=6,8.8.8.8,8.8.4.4
EOF

# Configure netplan for static IP on wlan0
sudo tee /etc/netplan/01-netcfg.yaml > /dev/null <<EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true
  wifis:
    wlan0:
      dhcp4: no
      addresses: [192.168.100.1/24]
EOF

# Apply netplan
sudo netplan apply

# Configure openNDS
sudo tee /etc/opennds/opennds.conf > /dev/null <<EOF
GatewayInterface wlan0
GatewayAddress 192.168.100.1
MaxClients 250
ClientIdleTimeout 480
ClientForceTimeout 1440
PreAuthIdleTimeout 30
AuthIdleTimeout 120
CheckInterval 60
FASPort 80
FASPath /fas/
Faskey changeme
EOF

# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf

# Set up NAT
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo netfilter-persistent save

# Start services
sudo systemctl start hostapd
sudo systemctl start dnsmasq
sudo systemctl start opennds

echo "Orange Pi AP setup complete. Connect to RecyFi Wi-Fi."