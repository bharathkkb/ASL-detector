import cv2
import numpy as np
import pandas as pd

import os
import random
import gc

import label_images
import glob

from keras import layers
from keras import models
from keras import optimizers
from keras.applications import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras_preprocessing.image import img_to_array, load_img
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from tensorflow.python.client import device_lib
from keras import backend as K
from keras.callbacks import EarlyStopping, ModelCheckpoint

# gpu
print(device_lib.list_local_devices())
K.tensorflow_backend._get_available_gpus()


train_dir = '../asl-data/asl_alphabet_modified'
test_dir = '../asl-data/asl_alphabet_test'

test_images = []

# Load Images from directory and store them in an array of test_images
for image_dir in glob.iglob(test_dir + '/**/*.jpg', recursive=True):
    test_images.append(image_dir)

proccessed_images = []

#Photopreprocessing
#for image in test_images:
#    proccessed_images.append(equalize_histogram_clahe(cv2.imread(image, cv2.IMREAD_COLOR))


img_h_w = 200

batch_size = 64
vgg_base = VGG16(weights='imagenet', include_top=False,
                 input_shape=(img_h_w, img_h_w, 3))
model = models.Sequential()  # Add the VGG base model
model.add(vgg_base)  # Add new layers
model.add(layers.Flatten())
model.add(layers.Dense(8192, activation='relu'))
model.add(layers.Dropout(0.8))
model.add(layers.Dense(4096, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(29, activation='softmax'))

model.summary()

# We'll use the RMSprop optimizer with a learning rate of 0.0001
# Using categorical_crossentropy as sparse_categorical_crossentropy is not one-hot encoded

#model.compile(loss='categorical_crossentropy',             optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])

model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.SGD(lr=0.001), metrics=['acc'])

# This helps prevent overfitting, since we are using a small dataset
datagen = ImageDataGenerator(rescale=1. / 255,  # Scale the image between 0 and 1
                             rotation_range=40,
                             width_shift_range=0.2,
                             height_shift_range=0.2,
                             shear_range=0.2,
                             zoom_range=0.2,
                             validation_split=0.2,
                             horizontal_flip=True,
                             fill_mode='nearest')


train_generator = datagen.flow_from_directory(
    directory=train_dir,
    target_size=(img_h_w, img_h_w),
    color_mode="rgb",
    batch_size=batch_size,
    class_mode="categorical",
    shuffle=True,
    seed=42,
    subset='training'
)
val_generator = datagen.flow_from_directory(
    directory=train_dir,
    target_size=(img_h_w, img_h_w),
    color_mode="rgb",
    batch_size=batch_size,
    class_mode="categorical",
    shuffle=True,
    seed=42,
    subset='validation'
)

test_generator = datagen.flow_from_directory(
    directory=test_dir,
    target_size=(img_h_w, img_h_w),
    color_mode="rgb",
    batch_size=1,
    class_mode=None,
    shuffle=False,
    seed=42
)
STEP_SIZE_TRAIN = train_generator.n // train_generator.batch_size
STEP_SIZE_VALID = val_generator.n // val_generator.batch_size
STEP_SIZE_TEST = test_generator.n / test_generator.batch_size
print(val_generator.class_indices)
# The training part
# We train for 64 epochs with about 100 steps per epoch
callbacks = [EarlyStopping(monitor='val_loss', patience=2),
             ModelCheckpoint(filepath='best_model.h5', monitor='val_loss', save_best_only=True)]
history = model.fit_generator(train_generator,
                              steps_per_epoch=STEP_SIZE_TRAIN,
                              epochs=64,
                              callbacks=callbacks,
                              validation_data=val_generator,
                              validation_steps=STEP_SIZE_VALID,
                              use_multiprocessing=True,
                              workers=4)

# Save the model
model.save_weights('model_weights.h5')
model.save('model_keras.h5')
# model.evaluate_generator(generator=test_generator)
test_generator.reset()

pred = model.predict_generator(test_generator, verbose=1, steps=STEP_SIZE_TEST)
predicted_class_indices = np.argmax(pred, axis=1)
labels = (train_generator.class_indices)
labels = dict((v, k) for k, v in labels.items())
predictions = [labels[k] for k in predicted_class_indices]
filenames = test_generator.filenames
results = pd.DataFrame({"Filename": filenames,
                        "Predictions": predictions})
print(results)

