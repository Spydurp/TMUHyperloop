from gpiozero import LED
import time
import RpiPinouts

while True:
    RpiPinouts.fans_on()
    print("on")
    time.sleep(5)
    RpiPinouts.fans_off()
    print("off")
    time.sleep(5)
