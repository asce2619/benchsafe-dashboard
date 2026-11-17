import serial
import requests
import time

# Update 'COM3' to match your actual port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Mac/Linux)
PORT = "COM3" 
BAUD_RATE = 115200
API_URL = "http://localhost:8000/api/events"

print(f"[*] Connecting to hardware on {PORT}...")

while True:
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
        print(f"[+] Successfully connected to {PORT}. Listening for serial telemetry...")
        
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"[Hardware Log]: {line}")
                
                # Check if the incoming serial message indicates a warning or alarm
                if "ALARM" in line or "WARNING" in line or "CRITICAL" in line:
                    payload = {
                        "source": "SENSOR",
                        "detail": line,
                        "cutoff_active": True
                    }
                    try:
                        res = requests.post(API_URL, json=payload)
                        print(f" -> Forwarded to Dashboard: {res.json().get('report')}")
                    except requests.exceptions.ConnectionError:
                        print(" [!] Warning: Could not reach FastAPI backend (is main.py running?)")
                        
    except (serial.SerialException, OSError):
        print(f"[-] Port {PORT} not found or disconnected. Retrying in 3 seconds...")
        time.sleep(3)