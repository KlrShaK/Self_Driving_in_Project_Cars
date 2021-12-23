import carseour
import numpy as np
import time
game = carseour.live()

while True:
    telemetry = []
    telemetry.append(round(game.mSpeed, 1))
    telemetry.append(round(game.mGear, 1))
    telemetry.append(round(game.mSteering, 3))
    telemetry.append(round(game.mThrottle, 3))
    # the Following code might look very inefficient but its the
    # best I could while keeping it all simple.(Due to the fact that the outputs are not float rather ctypes.c_float)
    # Any suggestions is welcome
    for i in range(4):
        telemetry.append(round(game.mTyreSlipSpeed[i], 4))
    for i in range(4):
        telemetry.append(round(game.mTyreGrip[i], 4))
    for i in range(4):
        telemetry.append(round(game.mTerrain[i], 4))

    print(telemetry)
    time.sleep(0.5)
