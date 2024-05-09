import pinouts

class Safe():
    brake_L_ON = True
    brake_R_ON = True
    bat_volt = 10
    bat_cur = 0
    bat_temp = 50
    lim_volt = 0
    lim_cur = 0
    lim_temp = 50
    vel = 0

def brakeCheck():
    if pinouts.getLBrakePos() and pinouts.getRBrakePos():
        pinouts.release_brakes()
        pinouts.apply_brakes()
    else:
        pinouts.apply_brakes()
        pinouts.release_brakes()
        pinouts.apply_brakes()
    
    
    