from gpiozero import LED
import time
import RpiPinouts

RpiPinouts.fans_off()
while True:
    RpiPinouts.main_power_on()
    print("on")
    time.sleep(1)
    RpiPinouts.main_power_off()
    print("off")
    time.sleep(1)
