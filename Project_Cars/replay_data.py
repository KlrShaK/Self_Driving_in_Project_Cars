# todo View the saved training data

import os
import numpy as np
import glob
import sys
import cv2
from random import shuffle

# todo Initialising training Data location
training_dir = r'F:\PyCharm Projects\Self_Driving_in_Project_Cars\Training_Data'
# training_dir = os.fsencode(training_dir)
train_list = glob.glob(r'F:\PyCharm Projects\Self_Driving_in_Project_Cars\Training_Data\training_data_*.npy')
if train_list == []:
    print("***************No Training Files found***************")
    exit()
print(train_list)

width = 100
height = 226
look_ahead = 15


def get_data(npData):
    X1 = npData[0]
    X2 = npData[1]
    X3 = npData[2]
    Y = npData[3]
    return X1, X2, X3, Y


def replay_data():
    print("************Starting Training**********")

    data_order = [i for i in range(0, len(train_list))]
    for i in data_order:
        file_name = r'F:\PyCharm Projects\Self_Driving_in_Project_Cars\Training_Data\training_data_{}.npy'.format(i)
        train_data = np.load(file_name, allow_pickle=True)
        print("loading File: {}".format(file_name))
        # print('training_data_{}.npy'.format(i), len(train_data))
        for data_elem in train_data:
            # Getting data in correct Form
            X1, X2, X3, Y = get_data(data_elem)
            show_imgs(X1, X2)
            telemetry = X3
            print(X3)
            print(Y)
            # sys.stdout.flush()
    print("**********END OF AVAILABLE DATA************")


def show_imgs(X1, X2):
    # todo show the captured screen at the heavy expense of loss of framerate
    # suggest to keep this commented (use for debugging purpose only)
    cv2.imshow('window', X1)
    cv2.imshow('window2', X2)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


if __name__ == '__main__':
    replay_data()
