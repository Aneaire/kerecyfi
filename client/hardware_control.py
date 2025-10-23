#!/usr/bin/env python3
# Hardware control module for Orange Pi

import time
import os

class HardwareController:
    """Control LEDs, sensors, and actuators on Orange Pi"""
    
    def __init__(self):
        self.led_pins = {
            'green': 17,   # Plastic accepted
            'blue': 27,    # Access granted  
            'red': 22      # Access denied/error
        }
        self.sensor_pin = 18  # Plastic detection sensor
        self.initialized = False
        
    def initialize(self):
        """Initialize GPIO pins"""
        try:
            # Try to import GPIO libraries for Orange Pi
            # This will vary based on Orange Pi model and OS
            try:
                import OPi.GPIO as GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)
                
                # Setup LED pins as output
                for led_pin in self.led_pins.values():
                    GPIO.setup(led_pin, GPIO.OUT)
                    GPIO.output(led_pin, GPIO.LOW)
                
                # Setup sensor pin as input
                GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                
                self.GPIO = GPIO
                self.initialized = True
                print("Hardware initialized successfully")
                
            except ImportError:
                print("GPIO library not available - using simulation mode")
                self.initialized = False
                
        except Exception as e:
            print(f"Hardware initialization failed: {e}")
            self.initialized = False
    
    def set_led(self, color, state):
        """Control LED color (True=on, False=off)"""
        if not self.initialized:
            print(f"SIMULATION: LED {color} {'ON' if state else 'OFF'}")
            return
            
        if color in self.led_pins:
            self.GPIO.output(self.led_pins[color], self.GPIO.HIGH if state else self.GPIO.LOW)
    
    def flash_led(self, color, duration=1.0, frequency=2):
        """Flash LED for specified duration"""
        end_time = time.time() + duration
        while time.time() < end_time:
            self.set_led(color, True)
            time.sleep(1.0 / (frequency * 2))
            self.set_led(color, False)
            time.sleep(1.0 / (frequency * 2))
    
    def read_sensor(self):
        """Read plastic detection sensor"""
        if not self.initialized:
            # Simulate sensor reading
            import random
            return random.choice([True, False])
            
        return self.GPIO.input(self.sensor_pin) == self.GPIO.LOW
    
    def wait_for_plastic(self, timeout=30):
        """Wait for plastic insertion"""
        print("Waiting for plastic insertion...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.read_sensor():
                print("Plastic detected!")
                return True
            time.sleep(0.1)
        
        print("Timeout - no plastic detected")
        return False
    
    def cleanup(self):
        """Cleanup GPIO resources"""
        if self.initialized and hasattr(self, 'GPIO'):
            self.GPIO.cleanup()

# LED control functions for easy access
def led_green_on():
    hw.set_led('green', True)

def led_green_off():
    hw.set_led('green', False)

def led_blue_on():
    hw.set_led('blue', True)

def led_blue_off():
    hw.set_led('blue', False)

def led_red_on():
    hw.set_led('red', True)

def led_red_off():
    hw.set_led('red', False)

# Global hardware controller instance
hw = HardwareController()