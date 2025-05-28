from gpiozero import LED
import time

led = LED(3)
led.on()


count = 0
while count < 100:
    led.off()
    time.sleep(10)
    led.on()
    time.sleep(10)
    count += 1
