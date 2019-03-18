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
from keras.preprocessing.image import ImageDataGenerator
from keras_preprocessing.image import img_to_array, load_img
from sklearn.model_selection import train_test_split

train_dir = '/asl-data/asl_alphabet_test'
test_dir = '/asl-data/asl_alphabet_train'

test_images = []

#Load Images from directory and store them in an array of test_images
for image_dir in glob.iglob(test_dir + '/**/*.jpg', recursive=True):
    test_images.append(image_dir)

random.shuffle(test_images) #Randomizes Array

image_data, image_labels = label_images.process_and_label(test_images)

#For memory optimization
del test_images
gc.collect()

#Convert image_data, image_labels to numpy arrays
image_data = np.array(image_data)
image_labels = np.array(image_labels)

#80% training data, 20% validation data
data_train, data_val, label_train, label_val = train_test_split(image_data, image_labels, test_size=0.20, random_state=2)
print("Shape of train images is:", data_train.shape)
print("Shape of validiation images is:", data_val.shape)
print("Shape of labels is:", label_train.shape)
print("Shape of label val is:", label_val.shape)

#Clear memory
del image_data
del image_labels
gc.collect()

ntrain = len(data_train)
nval = len(data_val)

batch_size = 16

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu',input_shape=(200, 200, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dropout(0.5))  #Dropout for regularization
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(29, activation='softmax'))  #Softmax function at the end because we have multiple classes

#Lets see our model
model.summary()

#We'll use the RMSprop optimizer with a learning rate of 0.0001
#We use categorical_crossentropy loss because its a multiclass classification
model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])


#This helps prevent overfitting, since we are using a small dataset
train_datagen = ImageDataGenerator(rescale=1./255)  #Scale the image between 0 and 1

val_datagen = ImageDataGenerator(rescale=1./255)  #We only rescale data


#Create the image generators
train_generator = train_datagen.flow(data_train, label_train, batch_size=batch_size)
val_generator = val_datagen.flow(data_val, label_val, batch_size=batch_size)

#The training part
#We train for 64 epochs with about 100 steps per epoch
history = model.fit_generator(train_generator,
                              steps_per_epoch=ntrain // batch_size,
                              epochs=64,
                              validation_data=val_generator,
                              validation_steps=nval // batch_size)

#Save the model
model.save_weights('model_weights.h5')
model.save('model_keras.h5')
