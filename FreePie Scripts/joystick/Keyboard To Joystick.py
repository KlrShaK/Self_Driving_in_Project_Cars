from System import Int16

if starting:
	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 5
	x = 0
	y = 0
	controller = vJoy[0]
	sensitivity = 100
	slowRate = sensitivity * 1.5
	max = 16000
	min = -max

if keyboard.getKeyDown(Key.D):
	x += 1 * sensitivity
elif keyboard.getKeyUp(Key.D) and keyboard.getKeyUp(Key.A):
	if x > 0:
		x -= 1 * slowRate
	if x < 0:
		x += 1 * slowRate
if keyboard.getKeyDown(Key.A):
	x -= 1 * sensitivity
elif keyboard.getKeyUp(Key.A) and keyboard.getKeyUp(Key.D):
	if x > 0:
		x -= 1 * slowRate
	if x < 0:
		x += 1 * slowRate
if keyboard.getKeyDown(Key.W):
	y += 1 * sensitivity
elif keyboard.getKeyUp(Key.W) and keyboard.getKeyUp(Key.S):
	if y > 0:
		y -= 1 * slowRate
	if y < 0:
		y += 1 * slowRate
if keyboard.getKeyDown(Key.S):
	y -= 1 * sensitivity
elif keyboard.getKeyUp(Key.S) and keyboard.getKeyUp(Key.W):
	if y > 0:
		y -= 1 * slowRate
	if y < 0:
		y += 1 * slowRate
	
if x > max:
	x = max
elif x < min:
	x = min

if y > max:
	y = max
elif y < min:
	y = min
	
controller.x = x
controller.y = y

diagnostics.watch(vJoy[0].x)
diagnostics.watch(vJoy[0].y)
	