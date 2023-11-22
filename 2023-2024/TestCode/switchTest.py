from gpiozero import Button
switch = Button(5)
while True:
	if switch.is_pressed:
		print("Button is pressed") 
	else:
		print("Button is not pressed")