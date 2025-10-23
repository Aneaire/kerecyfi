# RecyFi - Wi-Fi Kiosk for Plastic Recycling

## Overview
RecyFi is a kiosk that grants timed Wi-Fi access in exchange for plastic items. This implementation focuses on the software side, simulating sensor input and providing a captive portal for voucher-based access.

## Setup Instructions

### Prerequisites
- Orange Pi One (or equivalent ARM SBC) with Armbian installed
- TP-Link router (preferably with OpenWrt support, e.g., Archer C7)
- Ethernet cable for Orange Pi to TP-Link connection

### Orange Pi Setup
1. Flash Armbian on SD card and boot Orange Pi.
2. Run `scripts/setup_orange_pi.sh` to configure AP and captive portal.
3. Copy `server/` to Orange Pi and install dependencies: `pip install -r server/requirements.txt`
4. Run the server: `cd server && python3 app.py`

### TP-Link Setup
1. Flash OpenWrt on TP-Link if supported.
2. SSH into TP-Link and run `scripts/setup_tp_link.sh`.

### Testing
- Connect to "RecyFi" Wi-Fi.
- Access any URL to reach captive portal.
- Simulate insertion via web interface.
- Enter voucher to get 5 min internet.

## Architecture
- **Server**: Flask app for captive portal and voucher management.
- **AP**: hostapd + openNDS for Wi-Fi hotspot.
- **Internet**: Via TP-Link router.
- **Logging**: CSV logs in `logs/`.
- **UX**: Console prints simulating LEDs.

## Limitations
- Sensor simulation only; no real ESP32 integration.
- No ML classification yet.
- Offline core functionality.
