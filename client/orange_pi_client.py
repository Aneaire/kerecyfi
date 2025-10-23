#!/usr/bin/env python3
# Orange Pi client for RecyFi kiosk

import requests
import time
import json
import os
from datetime import datetime
from hardware_control import hw, led_green_on, led_green_off, led_blue_on, led_blue_off, led_red_on, led_red_off

SERVER_URL = "http://localhost:80"  # Change to your server IP
LOG_FILE = "../logs/client.log"

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_message(message):
    """Log messages to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + '\n')

def simulate_plastic_insertion():
    """Simulate plastic insertion and get voucher from server"""
    try:
        log_message("Simulating plastic insertion...")
        led_green_on()  # Turn on green LED
        
        response = requests.post(f"{SERVER_URL}/insert", timeout=10)
        
        if response.status_code == 200:
            log_message("Plastic accepted by server")
            # Extract voucher from response (simplified - in real implementation, parse HTML)
            log_message("Check server response for voucher details")
            time.sleep(2)  # Keep LED on for 2 seconds
            led_green_off()
            return True
        else:
            log_message(f"Server error: {response.status_code}")
            led_red_on()  # Error indication
            time.sleep(1)
            led_red_off()
            led_green_off()
            return False
            
    except requests.exceptions.RequestException as e:
        log_message(f"Connection error: {e}")
        led_red_on()  # Error indication
        time.sleep(1)
        led_red_off()
        led_green_off()
        return False

def validate_voucher(voucher):
    """Validate voucher with server"""
    try:
        log_message(f"Validating voucher: {voucher}")
        response = requests.post(f"{SERVER_URL}/validate", 
                               data={'voucher': voucher}, timeout=10)
        
        if response.status_code == 200:
            log_message("Voucher validated - Access granted")
            led_blue_on()  # Success indication
            time.sleep(2)
            led_blue_off()
            return True
        else:
            log_message("Voucher validation failed")
            led_red_on()  # Error indication
            time.sleep(1)
            led_red_off()
            return False
            
    except requests.exceptions.RequestException as e:
        log_message(f"Connection error: {e}")
        led_red_on()  # Error indication
        time.sleep(1)
        led_red_off()
        return False

def check_server_connection():
    """Check if server is reachable"""
    try:
        response = requests.get(f"{SERVER_URL}/", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def main():
    """Main client loop"""
    log_message("Orange Pi RecyFi Client starting...")
    
    # Initialize hardware
    hw.initialize()
    
    # Check server connection
    if not check_server_connection():
        log_message("ERROR: Cannot connect to server")
        hw.cleanup()
        return
    
    log_message("Connected to server successfully")
    
    # Simulate the kiosk workflow
    while True:
        print("\n=== RecyFi Kiosk Menu ===")
        print("1. Simulate plastic insertion")
        print("2. Validate voucher")
        print("3. Check server status")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == '1':
            simulate_plastic_insertion()
        elif choice == '2':
            voucher = input("Enter voucher: ").strip()
            validate_voucher(voucher)
        elif choice == '3':
            status = "Connected" if check_server_connection() else "Disconnected"
            log_message(f"Server status: {status}")
        elif choice == '4':
            log_message("Client shutting down...")
            hw.cleanup()
            break
        else:
            log_message("Invalid choice")
        
        time.sleep(1)

if __name__ == "__main__":
    main()