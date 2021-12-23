from screen_grab import grab_screen
import time
import cv2
import numpy as np
import os
import pygame
import carseour

# todo Initialising training location
training_dir = r'F:\PycharmProjects\Self_Driving\Training_Data'


# todo Initialising and Getting the Data from Shared memory of the Game (Project Cars)
# Will produce an error if the code is run and the game is not working in the background
game = carseour.live()


# todo Initializing PyGame and Joystick
pygame.init()
pygame.joystick.init()
_joystick = pygame.joystick.Joystick(0)
_joystick.init()


# Extracting Area of Intrest from the Image
def roi(img, vertices):
    mask = np.zeros_like(img, dtype=np.uint8)
    cv2.fillPoly(mask, vertices, (255,)*4)
    masked = cv2.bitwise_and(img, mask)
    return masked

# Generating Input for Branch 2 (Processed Image Data)
def process_img(image):
    """To apply various filter to captured screen, to  highlight various features"""
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)

    # Kerbs Filter (Red & Yellow)
    hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    lowerRY = np.array([100, 69, 69]) #100,69,100
    upperRY = np.array([150, 200, 200]) #150,200,200
    maskedKerbs = cv2.inRange(hsv, lowerRY, upperRY)
    K_vertices = np.array([[10, 500], [10, 300], [200, 150], [600, 150], [800, 300], [800, 500], [700, 450], [100, 450]])
    filtered_img = roi(maskedKerbs, [K_vertices])

    # White Filter (White & Blue)
    lowerWhite = np.array([0, 0, 105]) # 0,0,105
    upperWhite = np.array([105, 120, 240]) # 70,200,200
    maskedWhite = cv2.inRange(hsv, lowerWhite, upperWhite)
    w_vertices = np.array([[10,500],[10,300],[200,250],[600,250],[800, 300],[800,500],[700,450], [100, 450]])
    maskedWhite = roi(maskedWhite, [w_vertices])

    filtered_img = cv2.bitwise_or(filtered_img, maskedWhite)

    # Pure White Filter (White & Blue)
    lowerPW = np.array([0, 0, 165])
    upperPW = np.array([150, 50, 255])
    maskedPW = cv2.inRange(hsv, lowerPW, upperPW)
    maskedPW = roi(maskedPW, [w_vertices])

    filtered_img = cv2.bitwise_or(filtered_img, maskedPW)

    # Extracting Region of Image/Intrest(ROI)
    vertices = np.array([[10,500],[10,300],[200,150],[600,150],[800, 300],[800,500],[700,450], [100, 450]])
    processed_img = roi(processed_img, [vertices])

    combine_img = cv2.bitwise_or(processed_img, filtered_img)
    return combine_img

# Generating Input for Branch 1 (10-Frames RGB Input)
def screen_processing():
    """To capture the Screen and Extract the region of Intrest """
    screen = np.array(grab_screen([0, 40, 800, 640]))
    new_screen = process_img(screen) # Processes the captured Screen to highlight Edges and Kerbs
    new_screen = np.array(new_screen[150:500, 10:800])
    vertices = np.array([[10, 500], [10, 300], [200, 150], [600, 150], [800, 300], [800, 500], [700, 450], [100, 450]])
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    roi_screen = roi(screen, [vertices])
    roi_screen = np.array(roi_screen[150:500, 10:800])
    new_screen = cv2.resize(new_screen, (226,100))
    new_screen = np.array(new_screen)
    roi_screen = cv2.resize(roi_screen, (226,100)) #226,100
    roi_screen = np.array(roi_screen)
    return roi_screen, new_screen

# Generating Input for Branch 3 (Telemetry Data)
def get_telemetry():
    telemetry = []
    telemetry.append(round(game.mSpeed, 1))
    telemetry.append(round(game.mGear, 1))
    telemetry.append(round(game.mSteering, 4))
    telemetry.append(round(game.mThrottle, 4))
    # the Following code might look very inefficient but its the
    # best I could while keeping it all simple.(Due to the fact that the outputs are not float rather ctypes.c_float)
    # Any suggestions is welcome
    for i in range(4):
        telemetry.append(round(game.mTyreSlipSpeed[i], 4))
    for i in range(4):
        telemetry.append(round(game.mTyreGrip[i], 4))
    for i in range(4):
        telemetry.append(round(game.mTerrain[i], 3))

    telemetry = np.array(telemetry)
    return telemetry

# todo before runnning whole program, run this section individually to see for any errors/Problems
def get_user_input():
    user_input = []
    pygame.event.get()
    user_input.append(round(game.mSteering, 3))
    user_input.append(round(_joystick.get_axis(1) , 3))

    user_input = np.array(user_input)
    return user_input

if __name__ == '__main__':

    training_data = []
    file_count = 0
    frame_list = []
    Pause = False
    while True:
        while not Pause:
            # Name of file in which data is saved
            file_name = r'training_data_{}.npy'.format(file_count)
            train_path = os.path.join(training_dir, file_name)

            flag = False
            # last_time = time.time()
            roi_screen, processed_img = screen_processing()
            telemetry_data = get_telemetry()
            user_input = get_user_input()

            # todo show the captured screen at the heavy expense of loss of framerate
            # suggest to keep this commented (use for debugging purpose only)
            # cv2.imshow('window', processed_img)
            # cv2.imshow('window2', roi_screen)
            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()
            #     break

            # todo convert into a list of 10 frames
            if len(frame_list) < 16:
                frame_list.append(roi_screen)
                print(len(frame_list))
                continue
            else:
                frame_list.pop(0)
                frame_list.append(roi_screen)
                flag = True

            final_seq_frames = np.array(frame_list)
            # cv2.imshow('window2', roi_screen)
            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()
            #     break
            training_data.append(np.array([final_seq_frames, processed_img, telemetry_data, user_input]) )

            if len(training_data) % 1000 == 0:
                np.save(train_path, training_data)
                file_count += 1
                print(len(training_data))
                training_data = []

            # print('Frame Per Seconds: {}'.format(1 / (time.time() - last_time)))

            # Pause Mechanics
            pygame.event.get()
            if _joystick.get_button(7):  # 7 is right Trigger
                Pause = True
                print('---------------PAUSED!!!--------------')
                time.sleep(0.5)

        pygame.event.get()
        if _joystick.get_button(7):  # 7 is right Trigger
            frame_list = []
            Pause = False
            print('Starting Up.............')
            time.sleep(0.5)
