import carseour
import pygame

game = carseour.live()

pygame.init()
pygame.joystick.init()
_joystick = pygame.joystick.Joystick(0)
_joystick.init()

while True:
    pygame.event.get()
    pygame_reading = round(_joystick.get_axis(2), 3)
    carseour_reading = round(game.mSteering, 3)
    print('normal {} , filtered {}'.format(pygame_reading, carseour_reading) )
