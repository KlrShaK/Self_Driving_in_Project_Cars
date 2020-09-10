	# ==================================================================================================
	# ///////////////////////////////// DiRT 3 Mouse Steering Script ///////////////////////////////////
	# ==================================================================================================
	# This is a modified script, the original script was written by Skagen 
	# url: https://www.lfs.net/forum/post/1862759#post1862759
	# ==================================================================================================
	# This script will use 3 axes 
	# 1. Steering (X-Axis)
	# 2. Throttle (Y-Axis)
	# 3. Brake (Z-Axis)
	# ==================================================================================================
	# How to use this script:
	# 1. Configure vJoy with at least 20 buttons
	# 2. Make a backup copy of "wm_keyboard.xml" found here ("E:\Games\DiRT 3\actionmap\")
	# 3. Replace the current "wm_keyboard.xml" with the one provided in the zip file
	# 4. Modify your desired keys in this script starting from line 140
	# 5. Set Steering Deadzone and Linearity to 0, but feel free to play around with it
	# *To add or change buttons use the .XML file "wm_keyboard"
	#  Make sure the buttons assigned in the .XML matches with the buttons in this script
	#  Input codes that the game uses can be found here ("E:\Games\DiRT 3\gameconfig\input_names.xml")
	# ==================================================================================================
if starting:    
    system.setThreadTiming(TimingTypes.HighresSystemTimer)
    system.threadExecutionInterval = 5
    
    def set_button(button, key):
        if keyboard.getKeyDown(key):
            v.setButton(button, True)
        else:
            v.setButton(button, False)
    
    def calculate_rate(max, time):
        if time > 0:
            return max / (time / system.threadExecutionInterval)
        else:
            return max   
			
    int32_max = (2 ** 14) - 1
    int32_min = (( 2** 14) * -1) + 1
    
    v = vJoy[0]
    v.x, v.y, v.z, v.rx, v.ry, v.rz, v.slider, v.dial = (int32_min,) * 8
    v.y = 0
    v.z = 0
    # =============================================================================================
    # //////////////////////////////////////// SETTINGS ///////////////////////////////////////////
    # =============================================================================================
    # Mouse settings
    # =============================================================================================
    global mouse_sensitivity, sensitivity_center_reduction
    mouse_sensitivity = 5
    sensitivity_center_reduction = 0.1
    # =============================================================================================
    # Throttle & Brake Key:
    # =============================================================================================
    global throttle_key, brake_key
    throttle_key = Key.E
    brake_key = Key.W
    # Additional controls: Wheel Up = Reset Steering to Center @ Line 83
    # =============================================================================================
    # Throttle settings
    # =============================================================================================
    # Set throttle behaviour with the increase and decrease time (ms)
    # the actual increase and decrease rates are calculated automatically
    throttle_increase_time = 200
    throttle_decrease_time = 100
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
    braking_increase_time = 180
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
    global steering, steering_max, steering_min, steering_center_reduction    
    # Init values, do not change
    steering = 0.0
    steering_max = float(int32_max)
    steering_min = float(int32_min)
    steering_center_reduction = 1.0
# =================================================================================================
# Steering logic
# =================================================================================================
if mouse.wheelUp:
	steering = 0.0
if keyboard.getKeyDown(Key.Return):
	steering = 0.0	
if steering > 0:
    steering_center_reduction = sensitivity_center_reduction ** (1 - (steering / steering_max))
elif steering < 0:
    steering_center_reduction = sensitivity_center_reduction ** (1 - (steering / steering_min))
steering = steering + ((float(mouse.deltaX) * mouse_sensitivity) / steering_center_reduction)
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
# vJoy BUTTONS / 0 = Button 1, 1 = Button 2 etc...
# =================================================================================================
# Gear Up
v.setButton(0,int(mouse.leftButton))
# Gear Down
v.setButton(1,int(mouse.rightButton))
# E-Brake
global eb_key, eb_button
eb_key = Key.LeftAlt
eb_button = 2
set_button(eb_button, eb_key)
# Look Back
global lb_key, lb_button
lb_key = Key.D3
lb_button = 3
set_button(lb_button, lb_key)
# Change Camera
global cam_key, cam_button
cam_key = Key.C
cam_button = 4
set_button(cam_button, cam_key)
# Horn
global horn_key, horn_button
horn_key = Key.H
horn_button = 5
set_button(horn_button, horn_key)
# Instant Replay / Flashback / Replay Jump In
global flash_key, flash_button
flash_key = Key.F
flash_button = 6
set_button(flash_button, flash_key)
# Menu Back / Pause / Replay Exit
global esc_key, esc_button
esc_key = Key.Escape
esc_button = 7
set_button(esc_button, esc_key)
# Look / Menu Left
global lml_key, lml_button
lml_key = Key.LeftArrow
lml_button = 8
set_button(lml_button, lml_key)
# Look / Menu Right
global lmr_key, lmr_button
lmr_key = Key.RightArrow
lmr_button = 9
set_button(lmr_button, lmr_key)
# Look / Menu Up
global lmu_key, lmu_button
lmu_key = Key.UpArrow
lmu_button = 10
set_button(lmu_button, lmu_key)
# Look / Menu Down
global lmd_key, lmd_button
lmd_key = Key.DownArrow
lmu_key = 11
set_button(lmu_key, lmd_key)
# Menu Select / Start
global start_key, start_button
start_key = Key.Return
start_button = 12
set_button(start_button, start_key)
# Replay Rewind
global replayr_key, replayr_button
replayr_key = Key.F2
replayr_button = 13
set_button(replayr_button, replayr_key)
# Replay Fast Forward
global replayf_key, replayf_button
replayf_key = Key.F3
replayf_button = 14
set_button(replayf_button, replayf_key)
# Replay Pause
global replayp_key, replayp_button
replayp_key = Key.F1
replayp_button = 15
set_button(replayp_button, replayp_key)
# Replay Next Camera
global replayn_key, replayn_button
replayn_key = Key.F8
replayn_button = 16
set_button(replayn_button, replayn_key)
# Replay Prev Camera
global replayc_key, replayc_button
replayc_key = Key.F7
replayc_button = 17
set_button(replayc_button, replayc_key)
# Replay UI On Off
global replayo_key, replayo_button
replayo_key = Key.F9
replayo_button = 18
set_button(replayo_button, replayo_key)
# =================================================================================================
# PIE diagnostics logic
# =================================================================================================
diagnostics.watch(v.x)
diagnostics.watch(v.y)
diagnostics.watch(v.z)