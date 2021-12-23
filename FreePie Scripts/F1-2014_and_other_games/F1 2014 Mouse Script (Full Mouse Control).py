	# =============================================================================================
	# /////////////////////////////// F1 2014 Mouse Steering Script ///////////////////////////////
	# =============================================================================================
	# This is a modified script, the original script was written by Skagen 
	# url: https://www.lfs.net/forum/post/1862759#post1862759
	# =============================================================================================
	# This script will use 2 axes 
	# 1. Steering (X-Axis)
	# 2. Throttle and Brake (Y-Axis)
	# =============================================================================================
	# Use vJoy Feeder to set the axes in game
	# This script allows full car control with just the mouse
	# Move the mouse up to control the throttle and down for brakes
	# =============================================================================================
if starting:    
    system.setThreadTiming(TimingTypes.HighresSystemTimer)
    system.threadExecutionInterval = 5
    def calculate_rate(max, time):
        if time > 0:
            return max / (time / system.threadExecutionInterval)
        else:
            return max

    int32_max = (2 ** 14) - 1
    int32_min = (( 2** 14) * -1) + 1
    
    v = vJoy[0]
    v.x, v.y, v.z, v.rx, v.ry, v.rz, v.slider, v.dial = (int32_min,) * 8
    # =============================================================================================
    # //////////////////////////////////////// SETTINGS ///////////////////////////////////////////
    # =============================================================================================
    # Mouse settings - Change the sensitivity here
    # =============================================================================================
    global mouse_sensitivity, mouse_throttle_sensitivity
    mouse_throttle_sensitivity = 50
    mouse_sensitivity = 38
    # Additional controls: Wheel Up = Reset Steering to Center @ Line 89
    # =============================================================================================
    # Throttle settings
    # Init values, do not change
    global throttle, throttle_max, throttle_min
    throttle_max = int32_max
    throttle_min = int32_min
    throttle = throttle_min 
    # =============================================================================================
    # Steering settings
    # =============================================================================================
    global steering, steering_max, steering_min, steering_center_reduction    
    # Init values, do not change
    steering = 0.0
    steering_max = float(int32_max)
    steering_min = float(int32_min)
    steering_center_reduction = 1.0
# =================================================================================================
# LOOP START
# =================================================================================================
# Steering logic
# =================================================================================================
if mouse.wheelUp:
	steering = 0.0
	throttle = 0
if keyboard.getKeyDown(Key.Return):
	steering = 0.0
	throttle = 0
steering = steering + (float(mouse.deltaX) * mouse_sensitivity)
if steering > steering_max:
    steering = steering_max
elif steering < steering_min:
    steering = steering_min
v.x = int(round(steering))
# =================================================================================================
# Throttle logic and Braking logic
# =================================================================================================
throttle = throttle + (float(-mouse.deltaY) * mouse_throttle_sensitivity)
if throttle > throttle_max:
    throttle = throttle_max
elif throttle < steering_min:
    throttle = throttle_min
v.y = int(round(throttle))
# =================================================================================================
# vJoy BUTTONS 
# F1 2014 allows keyboard controls mixed with other input devices, so we don't need to set any more
# =================================================================================================
v.setButton(0,int(mouse.leftButton))
v.setButton(1,int(mouse.rightButton))
v.setButton(2,int(mouse.middleButton))
# =================================================================================================
# PIE diagnostics logic
# =================================================================================================
diagnostics.watch(v.x)
diagnostics.watch(v.y)