	# =============================================================================================
	# /////////////////////////////// F1 2014 Mouse Steering Script ///////////////////////////////
	# =============================================================================================
	# This is a modified script, the original script was written by Skagen 
	# url: https://www.lfs.net/forum/post/1862759#post1862759
	# =============================================================================================
	# This script will use 3 axes 
	# 1. Steering (X-Axis)
	# 2. Throttle (Y-Axis)
	# 3. Brake (Z-Axis)
	# =============================================================================================
	# Use vJoy Feeder to set the axes in game
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
    # Mouse settings
    # =============================================================================================
    global mouse_sensitivity
    mouse_sensitivity = 10
    # =============================================================================================
    # Throttle & Brake Key:
    # =============================================================================================
    global throttle_key, brake_key
    throttle_key = Key.E
    brake_key = Key.W
    # Additional controls: Wheel Up = Reset Steering to Center @ Line 89
    # =============================================================================================
    # Throttle settings
    # =============================================================================================
    # Set throttle behaviour with the increase and decrease time (ms)
    # the actual increase and decrease rates are calculated automatically
    throttle_increase_time = 600
    throttle_decrease_time = 600
    # Init values, do not change
    global throttle, throttle_max, throttle_min, throttle_increase_rate, throttle_decrease_rate
    throttle_max = int32_max
    throttle_min = int32_min
    throttle = throttle_min
    throttle_increase_rate = calculate_rate(throttle_max, throttle_increase_time)
    throttle_decrease_rate = calculate_rate(throttle_max, throttle_decrease_time) * -1
    # =============================================================================================
    # Braking settings
    # =============================================================================================
    # Set brake behaviour with the increase and decrease time (ms)
    # the actual increase and decrease rates are calculated automatically
    braking_increase_time = 200
    braking_decrease_time = 100
    # Init values, do not change
    global braking, braking_max, braking_min, braking_increase_rate, braking_decrease_rate
    braking_max = int32_max
    braking_min = int32_min
    braking = braking_min
    braking_increase_rate = calculate_rate(braking_max, braking_increase_time)
    braking_decrease_rate = calculate_rate(braking_max, braking_decrease_time) * -1  
    # =============================================================================================
    # Steering settings
    # =============================================================================================
    global steering, steering_max, steering_min    
    # Init values, do not change
    steering = 0.0
    steering_max = float(int32_max)
    steering_min = float(int32_min)
# =================================================================================================
# LOOP START
# =================================================================================================
# Steering logic
# =================================================================================================
if mouse.wheelUp:
	steering = 0.0
steering = steering + ((float(mouse.deltaX) * mouse_sensitivity))
if steering > steering_max:
    steering = steering_max
elif steering < steering_min:
    steering = steering_min
v.x = int(round(steering))
# =================================================================================================
# Throttle logic
# =================================================================================================
if keyboard.getKeyDown(throttle_key):
    throttle = throttle + throttle_increase_rate
else:
    throttle = throttle + throttle_decrease_rate
if throttle > throttle_max:
    throttle = throttle_max
elif throttle < throttle_min:
    throttle = throttle_min
v.y = throttle
# =================================================================================================
# Braking logic
# =================================================================================================
if keyboard.getKeyDown(brake_key):
    braking = braking + braking_increase_rate
else:
    braking = braking + braking_decrease_rate
if braking > braking_max:
    braking = braking_max
elif braking < braking_min:
    braking = braking_min
v.z = braking
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
diagnostics.watch(v.z)