import pinouts
import serial

class Safe():
    brake_L_ON = True
    brake_R_ON = True
    brake_L_OFF = False
    brake_R_OFF = False
    bat_volt = 10
    bat_cur = 0
    bat_temp = 50
    lim_volt = 0
    lim_cur = 0
    lim_temp = 50
    vel = 0

def brakeCheck():
    if pinouts.getLBrakePos() and pinouts.getRBrakePos():
        release = pinouts.release_brakes()
        apply = pinouts.apply_brakes()
    else:
        apply = pinouts.apply_brakes()
        release = pinouts.release_brakes()
        apply = pinouts.apply_brakes()
    if apply and release:
        return True
    else:
        return False

def launch(SBL: serial.Serial):
    pinouts.release_brakes()
    pinouts.lim_power_on()
    SBL.write("!r")

    
    
    