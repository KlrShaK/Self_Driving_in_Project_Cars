import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Model

""" Layers are Named in the following Manner " <TYPE> __ <Branch_no> - <Seq_no> " Combined branch is considered as 4th Branch"""

def get_model():
    # Defining inputs
    raw_img_input = Input(shape=(16,100,226,3), name='Input_Branch-1') # inputs = Input(shape = (frames, IMG_SIZE, IMG_SIZE, 3)) # frames=20
    process_img_input = Input(shape=(100,226,3), name='Input_Branch-2')
    telemetry_data_input = Input(shape=(16,), name='Input_Branch-3')


    # Declareing out pre-trained Base Model Inception_V3
    inception_v3_base = InceptionV3(include_top=False, weights='imagenet', input_shape=(100,226,3)) #350,790

    for layer in inception_v3_base.layers[:249]:
        layer.trainable = False
    for layer in inception_v3_base.layers[249:]:
        layer.trainable = True

    inception_v3_out = GlobalAveragePooling2D()(inception_v3_base.output)
    inception_v3 = Model(inception_v3_base.input, inception_v3_out, name='InceptionV3')

    # # The first Branch for raw_image_Input
    # # todo Get the First branch working
    branch_1 = TimeDistributed(inception_v3, name='TimeDist__1-1')(raw_img_input)
    branch_1 = LSTM(128, name= 'LSTM__1-1')(branch_1)
    # branch_1 = Dropout(0.2, name= 'Drop__1-1')(branch_1)
    branch_1 = Dense(2048, activation='relu', name='Dense__1-1')(branch_1)
    # branch_1 = Dropout(0.5, name= 'Drop__1-2')(branch_1)
    branch_1 = Dense(1024, activation='relu', name='Dense__1-2')(branch_1)
    branch_1 = Dropout(0.2, name= 'Drop__1-3')(branch_1)
    branch_1 = Dense(100, activation='relu', name='Branch-1_last')(branch_1)
    branch_1 = Model(raw_img_input, branch_1)

    # The Second Branch for process_img_input
    branch_2 = Conv2D(128, (5,5), activation='relu', name='Conv__2-1')(process_img_input)
    branch_2 = MaxPooling2D(5,5, name='Pool__2-1')(branch_2)
    branch_2 = Conv2D(64, (5,5), activation='relu', name='Conv__2-2')(branch_2)
    branch_2 = MaxPooling2D(2,2, name='Pool__2-2')(branch_2) #3,3
    branch_2 = Conv2D(64, (5,5), activation='relu', name='Conv__2-3')(branch_2)
    branch_2 = MaxPooling2D(2,2, name='Pool__2-3')(branch_2) #3,3
    branch_2 = Flatten(name='Flatten__2-1')(branch_2)
    branch_2 = Dense(1024, activation='relu', name='Dense__2-1')(branch_2)
    branch_2 = Dropout(0.5, name= 'Drop__2-1')(branch_2)
    branch_2 = Dense(100, activation='relu', name='Branch-2_last')(branch_2)
    branch_2 = Model(process_img_input, branch_2)

    # Third Branch For telemetry_data_input
    # branch_3 = LSTM(64,  name='LSTM__3-1')(telemetry_data_input)
    branch_3 = Dense(200, activation='relu', name='Dense__3-1')(telemetry_data_input)
    branch_3 = Dropout(0.5, name= 'Drop__3-1')(branch_3)
    branch_3 = Dense(100, activation='relu', name='Branch-3_last')(branch_3)
    branch_3 = Model(telemetry_data_input, branch_3)

    # Combine Output of Branches
    combined = concatenate([branch_1.output, branch_2.output, branch_3.output],  name='Combine_Branches')

    # Final Dense Layers on Combined Outputs
    combined_branch = Dense(300, activation= 'tanh', name='Dense__4-1')(combined)
    combined_branch = Dropout(0.5, name= 'Drop__4-1')(combined_branch)
    combined_branch = Dense(100, activation= 'tanh', name='Dense__4-2')(combined_branch)
    combined_branch = Dense(50, activation= 'tanh', name='Dense__4-3')(combined_branch)
    combined_branch = Dense(2, activation= 'tanh', name='Final_Predictions')(combined_branch)

    # our model will accept the inputs of the three branches and
    # then output a 2 value  for throttle and steering
    model = Model(inputs=[branch_1.input, branch_2.input, branch_3.input], outputs= combined_branch)

    return model

model = get_model()
