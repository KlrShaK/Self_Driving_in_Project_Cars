import tensorflow as tf
from Model import get_model
import os
import numpy as np
import glob


# todo Initializing Our Training Model
model = get_model()
model.summary()


# todo Initialising training Data location
training_dir = r'F:\PycharmProjects\Self_Driving\Training_Data'
# training_dir = os.fsencode(training_dir)
train_list = glob.glob(r'F:\PycharmProjects\Self_Driving\Training_Data\training_data_*.npy')
train_list[:] = [file[46:] for file in train_list]


def data_generator(train_list, batch_size):

    i = 0
    j = 0
    flag = True
    while True:
        # inputs = []
        # outputs = []
        if i < len(train_list):
            if flag == True:
                train_path = os.path.join(training_dir, train_list[i])
                data = np.load(train_path, allow_pickle=True)
                flag = False

            if j >= len(data):
                j = 0
                i += 1
                flag = True
                del data

            else:
                if len(data[j:]) >= batch_size:
                    input_1 = data[j:(j+batch_size), 1] #0
                    input_2 = data[j:(j+batch_size), 1]
                    input_3 = data[j:(j + batch_size), 2]
                    outputs= data[j:(j+batch_size), -1]
                    j += (batch_size)
                    yield {'Input_Branch-1' : input_1,'Input_Branch-2': input_2, 'Input_Branch-3': input_3}, outputs

                elif len(data[j:])< batch_size:
                    input_1 = data[j:, 0]
                    input_2 = data[j:, 1]
                    input_3 = data[j:, 2]
                    outputs= data[j:, -1]
                    j = 0
                    i+= 1
                    flag = True
                    del data
                    yield {'Input_Branch-1': input_1, 'Input_Branch-2': input_2, 'Input_Branch-3': input_3}, outputs

        else:
            i = 0
            del data
            flag = True
            np.random.shuffle(train_list)


batch_size = 5
# dataset = tf.data.Dataset.from_generator(data_generator, args= [train_list, batch_size],
#                                          output_types = ({'Input_Branch-1': tf.uint8, 'Input_Branch-2': tf.uint8, 'Input_Branch-3': tf.float32}, tf.float32),)

dataset = data_generator(train_list, batch_size)
model.compile(optimizer='adam', loss='mse', metrics=['mae'])
model.fit(dataset, epochs=1, steps_per_epoch=200)

