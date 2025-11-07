from gpiozero import LED
import time
import RpiPinouts

RpiPinouts.fans_on()
while True:
    RpiPinouts.retract_brakes()
    print(RpiPinouts.brakeLeftStatus())
    print(RpiPinouts.brakeRightStatus())
    time.sleep(10)
    RpiPinouts.deploy_brakes()
    print(RpiPinouts.brakeLeftStatus())
    print(RpiPinouts.brakeRightStatus())
    time.sleep(1)
