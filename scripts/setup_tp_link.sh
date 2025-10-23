#!/bin/bash
# Setup script for TP-Link with OpenWrt (run on router via SSH)

# Install nodogsplash
opkg update
opkg install nodogsplash

# Configure nodogsplash
uci set nodogsplash.@nodogsplash[0].enabled=1
uci set nodogsplash.@nodogsplash[0].gatewayinterface='br-lan'
uci set nodogsplash.@nodogsplash[0].redirecturl='http://192.168.100.1/portal'  # Point to Orange Pi portal
uci commit nodogsplash

# Restart nodogsplash
/etc/init.d/nodogsplash restart

# Set up firewall to allow internet after auth
uci add firewall zone
uci set firewall.@zone[-1].name='captive'
uci set firewall.@zone[-1].input='ACCEPT'
uci set firewall.@zone[-1].output='ACCEPT'
uci set firewall.@zone[-1].forward='ACCEPT'
uci add_list firewall.@zone[-1].network='lan'
uci commit firewall
/etc/init.d/firewall restart

echo "TP-Link setup complete. Clients authenticated on Orange Pi will get internet."