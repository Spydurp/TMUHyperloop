from gpiozero import LED, OutputDevice

#LED GPIO pins
red_LED_pin = 17 #G17
yellow_LED_pin = 16 #G16
green_LED_pin = 13 #G13

#Brake power pins
brakes_on_pin = 4 #G4
brakes_off_pin = 5 #G5

#LIM power pin
LIM_power_pin = 6 #G6

#Brake and LIM outputs
brakes_on = OutputDevice(brakes_on_pin)
brakes_off = OutputDevice(brakes_off_pin)
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
    brakes_on_pin.on()

def release_brakes():
    brakes_off_pin.off()

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


