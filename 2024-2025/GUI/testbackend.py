import socket
import time
import json
import random

HOST = "192.168.1.100"  # Replace with your GUI's IP address
PORT = 12345  # Replace with your GUI's port

# Function to generate mock sensor data
def generate_sensor_data():
    return {
        "battery_temp": round(random.uniform(20.0, 50.0), 2),
        "velocity": round(random.uniform(0.0, 100.0), 2),
        "brake_engaged": random.choice([True, False])
    }

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}")
            while True:
                data = generate_sensor_data()
                s.sendall(json.dumps(data).encode("utf-8"))
                print(f"Sent: {data}")
                time.sleep(1)  # Adjust as needed
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("Disconnected.")

if __name__ == "__main__":
    main()
