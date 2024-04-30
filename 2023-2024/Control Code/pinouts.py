from gpiozero import LED, OutputDevice

#LED GPIO pins
red_LED_pin = 17 #G17
yellow_LED_pin = 16 #G16
green_LED_pin = 13 #G13

#Brake power pins
brakes_on_pin1 = 2 #G2
brakes_on_pin2 = 3 #G3
brakes_off_pin1 = 4 #G4
brakes_off_pin2 = 5 #G5

#Brake Position Pins
brake_L_ON = 9
brake_R_ON = 10
brake_L_OFF = 11
brake_R_OFF = 12

#LIM power pin
LIM_power_pin = 6 #G6

#Brake and LIM outputs
brakes_on = OutputDevice(brakes_on_pin1, brakes_on_pin2)
brakes_off = OutputDevice(brakes_off_pin1, brakes_off_pin2)
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
    brakes_off_pin1.off()
    brakes_off_pin2.off()
    brakes_on_pin1.on()
    brakes_on_pin2.on()

def release_brakes():
    brakes_on_pin1.off()
    brakes_on_pin2.off()
    brakes_off_pin1.on()
    brakes_off_pin2.on()

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
    green_LED_pin.blink()


