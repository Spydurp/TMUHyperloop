import time
import gpiozero

TIMEOUT = 5 # Seconds before timeout for brake check

# Brake Sensor Input Pins

brake_sensors = {
    "Brake 1 (D)": gpiozero.Button(17), # pull_up by default, connect other side of button to ground.
    "Brake 1 (R)": gpiozero.Button(27),
    "Brake 2 (D)": gpiozero.Button(22),
    "Brake 2 (R)": gpiozero.Button(23),
    "Brake 3 (D)": gpiozero.Button(24),
    "Brake 3 (R)": gpiozero.Button(25),
    "Brake 4 (D)": gpiozero.Button(5),
    "Brake 4 (R)": gpiozero.Button(6)
}

# Output Pins
led_pins = {
    "LED 1": gpiozero.LED(12),
    "LED 2": gpiozero.LED(13),
    "LED 3": gpiozero.LED(19)
}

brake_power_pins = {
    "Brake Control S1": gpiozero.OutputDevice(16),
    "Brake Control S2": gpiozero.OutputDevice(20),
    "Brake Control S3": gpiozero.OutputDevice(21),
    "Brake Control S4": gpiozero.OutputDevice(18) 
}

vfd_pin = gpiozero.OutputDevice(26)

main_circuit_pins = {
    "Main Switch" : gpiozero.OutputDevice(14),
    "VFD Switch 1" : gpiozero.OutputDevice(15),
    "VFD Switch 2" : gpiozero.OutputDevice(2)
}

def brake_check() -> bool:

    retract = retract_brakes()

    deploy = deploy_brakes()
    
    return retract and deploy

def deploy_brakes() -> bool:
    brake_power_pins["Brake Control S1"].on()
    brake_power_pins["Brake Control S2"].on()
    brake_power_pins["Brake Control S3"].on()
    brake_power_pins["Brake Control S4"].on()

    # wait until brakes are fully deployed
    t = time.perf_counter()
    brake_sensors["Brake 1 (R)"].wait_for_inactive(TIMEOUT)
    brake_sensors["Brake 1 (D)"].wait_for_active(TIMEOUT)
    brake_sensors["Brake 2 (R)"].wait_for_inactive(TIMEOUT)
    brake_sensors["Brake 2 (D)"].wait_for_active(TIMEOUT)
    brake_sensors["Brake 3 (R)"].wait_for_inactive(TIMEOUT)
    brake_sensors["Brake 3 (D)"].wait_for_active(TIMEOUT)
    brake_sensors["Brake 4 (R)"].wait_for_inactive(TIMEOUT)
    brake_sensors["Brake 4 (D)"].wait_for_active(TIMEOUT)

    t = time.perf_counter() - t
    if t > 2*TIMEOUT:
        return False
    
    return True

def retract_brakes() -> bool:
    # retract brakes
    brake_power_pins["Brake Control S1"].off()
    brake_power_pins["Brake Control S2"].off()
    brake_power_pins["Brake Control S3"].off()
    brake_power_pins["Brake Control S4"].off()
    
    #Wait until brakes are fully retracted
    t = time.perf_counter()
    brake_sensors["Brake 1 (D)"].wait_for_inactive(TIMEOUT)
    brake_sensors["Brake 1 (R)"].wait_for_active(TIMEOUT)
    brake_sensors["Brake 2 (D)"].wait_for_inactive(TIMEOUT)
    brake_sensors["Brake 2 (R)"].wait_for_active(TIMEOUT)
    brake_sensors["Brake 3 (D)"].wait_for_inactive(TIMEOUT)
    brake_sensors["Brake 3 (R)"].wait_for_active(TIMEOUT)
    brake_sensors["Brake 4 (D)"].wait_for_inactive(TIMEOUT)
    brake_sensors["Brake 4 (R)"].wait_for_active(TIMEOUT)

    t = time.perf_counter() - t
    if t > 2*TIMEOUT:
        return False

    return True

def main_power_on() -> None:
    main_circuit_pins["Main Switch"].on()
    main_circuit_pins["VFD Switch 1"].on()
    main_circuit_pins["VFD Switch 2"].on()

def main_power_off() -> None:
    main_circuit_pins["Main Switch"].off()
    main_circuit_pins["VFD Switch 1"].off()
    main_circuit_pins["VFD Switch 2"].off()