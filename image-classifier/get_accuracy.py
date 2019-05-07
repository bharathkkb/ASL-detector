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
from sklearn.metrics import confusion_matrix
import pylab as pl

# gpu
print(device_lib.list_local_devices())
K.tensorflow_backend._get_available_gpus()
pd.set_option('display.max_rows', 1000)

#train_dir = '/new-2-asl-data/asl-data/asl_alphabet_train'
test_dir = '../new-asl-data/asl_alphabet_test_real_world_+_kaggle/modified'
#test_dir = '../asl-data/asl_alphabet_test'

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
    directory=test_dir,
    target_size=(img_h_w, img_h_w),
    color_mode="rgb",
    batch_size=batch_size,
    class_mode="categorical",
    shuffle=True,
    seed=42,
    subset='training'
)
val_generator = datagen.flow_from_directory(
    directory=test_dir,
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

i = 0
prevLetter =""
correct = 0
current_acc = 0
total = 0
for label in correctlabels:
    if label == predictions[i]:
        if label == prevLetter:
            total+=1
            correct+=1
            current_acc =float(correct/total)
        else:
            print("Accuracy for " + prevLetter + " is ")
            print(current_acc)
            current_acc = 1
            total = 1
            correct = 1
            prevLetter = label
    else:
        if label == prevLetter:
            total+=1
            current_acc = float(correct/total)
        else:
            print("Accuracy for " + prevLetter + " is ")
            print(current_acc)
            current_acc = 0
            total = 1
            correct = 0
            prevLetter = label
    i+=1

labels_cm = ["A", "B", "C", "D", "E", "F", "G","H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "del", "nothing", "space"]
cm = confusion_matrix(correctlabels, predictions, labels_cm)
print(cm)
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(cm)
plt.title('Confusion matrix of the classifier')
fig.colorbar(cax)
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

acc_score = accuracy_score(correctlabels, predictions)
print("accuracy = {}".format(acc_score))