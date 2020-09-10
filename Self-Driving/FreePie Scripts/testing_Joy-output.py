# to give input values for Joystick
import random
def controls():
    x, y = random.uniform(-1,1), random.uniform(-1,1)
    print(x, y)
    return x, y
