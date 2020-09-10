from System import Int16
import sys
sys.path.insert(1, 'F:\PycharmProjects\Self_Driving\FreePie Scripts')
from feeding_vjoy import controls
import time

if starting:
	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 5
	x = 0
	y = 0
	max = 16000
	min = -max
	
	vjoy = vJoy[0]

x, y = controls()

x *= 16000
y *= 16000

if x > max:
	x = max
elif x < min:
	x = min

if y > max:
	y = max
elif y < min:
	y = min

vjoy.x = x
vjoy.y = y
diagnostics.watch(vJoy[0].x)
diagnostics.watch(vJoy[0].y)

# time.sleep(0.2)
