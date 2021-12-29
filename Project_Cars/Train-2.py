# todo  Using the Same Method as in NXP Competition

import tensorflow as tf
from Model import get_model
import os
import numpy as np
import glob
from random import shuffle

# Initialising training Data location
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

def give_seqImgs(data, start_point, size=15):
    new_data = np.zeros((900, 100, 226, 3), dtype=int)
    new_data[0] = data[0][0]
    for i in range(len(data)):
        new_data[i] = data[i][0]
    temp_x1 = np.asarray([new_data[(i - start_point): i] for i in range(start_point, len(data))], dtype=int)
    temp_x1 = np.reshape(temp_x1, (-1, 15, width, height, 3))
    return temp_x1


def get_train_data(npData, start_point):
    X1 = np.array(give_seqImgs(npData, start_point))
    X2 = np.array([npData[i, 1] for i in range(start_point, len(npData))]).reshape(-1, width, height, 1)
    X3 = np.array([npData[i, 2] for i in range(start_point, len(npData))]).reshape(-1, 16)
    Y = np.array([npData[i, 3] for i in range(start_point, len(npData))]).reshape(-1, 2)
    return X1, X2, X3, Y


def train_model(EPOCHS=40):
    epoch_count = 0
    verbose_flag = -1  # Verbose = 1 only for one new epoch else verbose = 0
    loss_hist = []
    val_loss_hist = []

    print("************Starting Training**********")
    print("********EPOCH-{}**********".format(0))
    for e in range(EPOCHS):
        data_order = [i for i in range(0, len(train_list))]
        shuffle(data_order)


        for i in data_order:
            file_name = r'F:\PyCharm Projects\Self_Driving_in_Project_Cars\Training_Data\training_data_{}.npy'.format(i)
            train_data = np.load(file_name, allow_pickle=True)
            # print('training_data_{}.npy'.format(i), len(train_data))

            # splitting b/w training and testing data
            test_split = 0.1
            train_len = int(len(train_data) * (1 - test_split))
            train = train_data[:train_len]
            test = train_data[train_len:]

            # Getting data in correct Form
            start_point = look_ahead
            X1, X2, X3, Y = get_train_data(train, start_point)
            TX1, TX2, TX3, TY = get_train_data(test, start_point=(start_point + train_len))

            # Fitting Model
            # todo Add Verbose Silencing if not on epoch
            history = model.fit(x={'Input_Branch-1': X1, 'Input_Branch-2': X2, 'Input_Branch-3': X3},
                                y={'Final_Predictions': Y},
                                epochs=1, validation_data=(
                    {'Input_Branch-1': TX1, 'Input_Branch-2': TX2, 'Input_Branch-3': TX3}, {'targets': TY}), verbose=1)
            val_loss_hist.append(history.history['val_loss'][0])
            loss_hist.append(history.history['loss'][0])

            del train_data

        # implement early stopping
        if epoch_count % 1 == 0 and epoch_count != 0:
            print('SAVING MODEL!')
            model.save('Training_Data/weights/Weights_{}'.format(epoch_count))
            val_loss_hist_np = np.array(val_loss_hist)
            loss_hist_np = np.array(loss_hist)
            np.save("Training_Data/weights/val_loss.npy", val_loss_hist_np)
            np.save("Training_Data/weights/loss_hist.npy", loss_hist_np)
            del val_loss_hist_np
            del loss_hist_np

        if epoch_count % len(train_list) == 0 and epoch_count != 0:
            epoch_count += 1
            print("********EPOCH-{}**********".format(epoch_count))


if __name__ == '__main__':
    input_shape = (216, 216, 3)
    pool_size = (2, 2)
    # Initializing Our Training Model
    model = get_model()
    # TO print Model Summary
    # model.summary()
    try:
        # Transfer Learning
        model = tf.keras.models.load_model("weights/Weights_6-old")
        print("************************Model Weights LOADED*****************")
    except:
        print("Prev model not available")
    train_model(40)
