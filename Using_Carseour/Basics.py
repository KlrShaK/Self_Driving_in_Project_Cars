import carseour
import time

game = carseour.live()
print(type(game))
while True:
    print("Speed: " + str(round(game.mSpeed*(18/5), 1))+ " km/h")
    print('steering ', round(game.mSteering,3))
    print('steering ', round(game.mSteering, 3))
    print('TyreSlipSpeed ', *game.mTyreSlipSpeed, sep=',')
    print('TyreGrip ', *game.mTyreGrip, sep=',')
    print('Terrain ', *game.mTerrain, sep=',')
    print('rain', game.mRainDensity)
    time.sleep(0.5)
    print(type(game.mTyreSlipSpeed))
    print([game.mTyreSlipSpeed[x] for x in range(4)], end=', ')
    print('\n')