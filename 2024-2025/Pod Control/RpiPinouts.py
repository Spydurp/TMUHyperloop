import RPi.GPIO as GPIO
import time

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

# Brake Sensor Input Pins
brake_sensors = {
    "Brake 1 (D)": 17,
    "Brake 1 (R)": 27,
    "Brake 2 (D)": 22,
    "Brake 2 (R)": 23,
    "Brake 3 (D)": 24,
    "Brake 3 (R)": 25,
    "Brake 4 (D)": 5,
    "Brake 4 (R)": 6
}

# Set up input pins with pull-down resistors
for pin in brake_sensors.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    #Default to Low (0v)

# Output Pins
led_pins = {
    "LED 1": 12,
    "LED 2": 13,
    "LED 3": 19
}

brake_control_pins = {
    "Brake Control S1": 16,
    "Brake Control S2": 20,
    "Brake Control S3": 21,
    "Brake Control S4": 18  #Optional 4th brake switch
}

vfd_pin = 26

# Set up all output pins
for pin in led_pins.values():
    GPIO.setup(pin, GPIO.OUT)

for pin in brake_control_pins.values():
    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(vfd_pin, GPIO.OUT)


# Main Loop
try:
    print("Monitoring brake sensors... (Ctrl+C to stop)\n")

    # Optional test: Turn all outputs ON briefly
    for pin in led_pins.values():
        GPIO.output(pin, GPIO.HIGH)
    for pin in brake_control_pins.values():
        GPIO.output(pin, GPIO.HIGH)
    GPIO.output(vfd_pin, GPIO.HIGH)

    time.sleep(1)  # wait 1 sec

    # Turn all outputs OFF
    for pin in led_pins.values():
        GPIO.output(pin, GPIO.LOW)
    for pin in brake_control_pins.values():
        GPIO.output(pin, GPIO.LOW)
    GPIO.output(vfd_pin, GPIO.LOW)

    # Begin sensor monitoring loop
    while True:
        for name, pin in brake_sensors.items():
            state = GPIO.input(pin)
            print(f"{name}: {'ENGAGED' if state else 'OFF'}")
        print("-" * 40)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.cleanup()
