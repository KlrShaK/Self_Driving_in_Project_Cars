from System import Int16

if starting:
	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 5
	x = 0
	y = 0
	max = 16000
	min = -max
	#joystick max 16000
	#joystick min -16000
	#could make cahnge the range from -16000 to 16000 to -1 to 1 but i dont need to
	
	v = vJoy[0]
	sensX = 50
	sensY = 50

y -= mouse.deltaY * sensY
x += mouse.deltaX * sensX

if x > max:
	x = max
elif x < min:
	x = min

if y > max:
	y = max
elif y < min:
	y = min

v.x = x
v.y = y
diagnostics.watch(vJoy[0].x)
diagnostics.watch(vJoy[0].y)


	
		
	