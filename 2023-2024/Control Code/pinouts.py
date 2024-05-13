from gpiozero import LED, OutputDevice, Button
import time

#LED GPIO pins
red_LED_pin = 17 #G17
yellow_LED_pin = 16 #G16
green_LED_pin = 13 #G13

#Brake power pins
brakes_S_pin1 = LED(4) #G4
brakes_S_pin2 = LED(5) #G5

#Brake Position Pins
brake_L_ON = Button(9)
brake_R_ON = Button(10)
brake_L_OFF = Button(11)
brake_R_OFF = Button(12)

#LIM power pin
LIM_power_pin = 6 #G6

#Brake and LIM outputs
#brakes_ = OutputDevice(brakes_on_pin1, brakes_on_pin2)
#brakes_off = OutputDevice(brakes_off_pin1, brakes_off_pin2)
LIM_power = OutputDevice(LIM_power_pin)

#LED indicators

#   malfunctioning battery: blinking red
#   other errors: constant red
red_led = LED(red_LED_pin) 

#   standby state: blinking yellow
yellow_led = LED(yellow_LED_pin)

#   moving (main power on): constant green
#   braking and coasting (main power on): blinking green
green_led = LED(green_LED_pin)

def apply_brakes():
    brakes_S_pin1.on()
    brakes_S_pin2.off()
    time.sleep(6)
    brakes_S_pin1.off()
    if brake_L_ON.is_active and brake_R_ON.is_active and not brake_R_OFF.is_active and not brake_L_OFF.is_active:
        return True
    else:
        return False
    

def release_brakes():
    brakes_S_pin1.off()
    brakes_S_pin2.on()
    time.sleep(6)
    brakes_S_pin2.off()
    if not brake_L_ON.is_active and not brake_R_ON.is_active and brake_R_OFF.is_active and brake_L_OFF.is_active:
        return True
    else:
        return False

def lim_power_on():
    LIM_power_pin.on()

def lim_power_off():
    LIM_power_pin.off()

def battery_malfunction():
    red_LED_pin.blink()

def other_error():
    red_LED_pin.on()

def standby():
    yellow_LED_pin.on()

def moving():
    green_LED_pin.on()

def braking_coasting():
    green_LED_pin.blink() # Implement blinking function, use multithreading

def getLBrakePos():
    if brake_L_ON == False and brake_L_OFF == True:
        return 0
    if brake_L_ON == True and brake_L_OFF == False:
        return 1
    return 2 # If neither is true, fault

def getRBrakePos():
    if brake_R_ON == False and brake_R_OFF == True:
        return 0
    if brake_R_ON == True and brake_R_OFF == False:
        return 1
    return 2 # If neither is true, fault


