import cv2
import numpy as np
import pandas as pd

import os
import random
import gc

import label_images
import glob

from process_image import equalize_histogram_clahe
from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras_preprocessing.image import img_to_array, load_img
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from tensorflow.python.client import device_lib
from keras import backend as K
# gpu
print(device_lib.list_local_devices())
K.tensorflow_backend._get_available_gpus()


train_dir = '../asl-data/asl_alphabet_train'
test_dir = '../asl-data/asl_alphabet_test'

test_images = []

img_h_w = 200
ntrain = 78301
nval = 8700

batch_size = 64

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu',
                        input_shape=(img_h_w, img_h_w, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dropout(0.5))  # Dropout for regularization
model.add(layers.Dense(512, activation='relu'))
# Softmax function at the end because we have multiple classes
model.add(layers.Dense(29, activation='softmax'))

# Lets see our model
model.summary()

# We'll use the RMSprop optimizer with a learning rate of 0.0001
# Using categorical_crossentropy as sparse_categorical_crossentropy is not one-hot encoded
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])


# This helps prevent overfitting, since we are using a small dataset
datagen = ImageDataGenerator(rescale=1. / 255,  # Scale the image between 0 and 1
                             rotation_range=40,
                             width_shift_range=0.2,
                             height_shift_range=0.2,
                             shear_range=0.2,
                             zoom_range=0.2,
                             validation_split=0.1,
                             horizontal_flip=True,)


train_generator = datagen.flow_from_directory(
    directory=train_dir,
    target_size=(200, 200),
    color_mode="rgb",
    batch_size=32,
    class_mode="categorical",
    shuffle=True,
    seed=42,
    subset='training'
)
val_generator = datagen.flow_from_directory(
    directory=train_dir,
    target_size=(200, 200),
    color_mode="rgb",
    batch_size=32,
    class_mode="categorical",
    shuffle=True,
    seed=42,
    subset='validation'
)


# The training part
# We train for 64 epochs with about 100 steps per epoch
history = model.fit_generator(train_generator,
                              steps_per_epoch=ntrain // batch_size,
                              epochs=64,
                              validation_data=val_generator,
                              validation_steps=nval // batch_size,
                              use_multiprocessing=True,
                              workers=4)

# Save the model
model.save_weights('model_weights.h5')
model.save('model_keras.h5')
