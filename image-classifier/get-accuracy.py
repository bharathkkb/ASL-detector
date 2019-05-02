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
from keras.models import load_model
from keras.applications import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras_preprocessing.image import img_to_array, load_img
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from tensorflow.python.client import device_lib
from keras import backend as K
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import accuracy_score 
# gpu
print(device_lib.list_local_devices())
K.tensorflow_backend._get_available_gpus()
pd.set_option('display.max_rows', 1000)

train_dir = '/new-2-asl-data/asl-data/asl_alphabet_train'
test_dir = '/new-asl-data/asl_alphabet_test_real_world_+_kaggle'


test_images = []
img_h_w = 200

batch_size = 64


#This helps prevent overfitting, since we are using a small dataset
datagen = ImageDataGenerator(rescale=1. / 255,  # Scale the image between 0 and 1
                             rotation_range=10,
                             width_shift_range=0.1,
                             height_shift_range=0.1,
                             shear_range=0.05,
                             zoom_range=0.1,
                             validation_split=0.2,
                             horizontal_flip=False,
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
print(test_generator.class_indices)

test_generator.reset()
model = load_model('model_keras_new_kushal.h5')
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.SGD(lr=0.0001), metrics=['acc'])
pred = model.predict_generator(test_generator, verbose=1, steps=STEP_SIZE_TEST)
predicted_class_indices = np.argmax(pred, axis=1)
labels = (train_generator.class_indices)
labels = dict((v, k) for k, v in labels.items())
predictions = [labels[k] for k in predicted_class_indices]
filenames = test_generator.filenames
results = pd.DataFrame({"Filename": filenames,
                        "Predictions": predictions})
print(results)
correctlabels=[filename.split("/")[0] for filename in filenames]

acc_score = accuracy_score(correctlabels, predictions)
print("accuracy = {}".format(acc_score))
