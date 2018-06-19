
# coding: utf-8

# # Train Network
# 
# This notebook trains a Convolutional Neural Network using categorized images.

# ### Install Packages
# 
# This notebook requires `Pillow`, `tensorflow` and `keras`. You may uncomment and run the cell below to have Jupyter Notebook install these for you.

# In[4]:


# !pip install Pillow, tensorflow, keras


# ### Configuration
# 
# Set the variables below to specify where the categorical images are located, which classes to train and what the filename should be for saved training data. If you would like to train all 45+ categories, set `classes = None`.

# In[1]:


import os

image_path = 'capture_data'
epochs = 100

classes = [ "forward", "slight_left", "left", "sharp_left", "slight_right", "right", "sharp_right" ]
checkpoint_path = 'weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5'


# In[2]:


import matplotlib.image as mpimg
import sys
from PIL import Image
sys.modules['Image'] = Image
from PIL import Image
import Image
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten

def create_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(64, 64, 1)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(classes), activation='softmax'))
    return model


# In[3]:


def train():
    from keras.preprocessing.image import ImageDataGenerator
    from keras.callbacks import ModelCheckpoint

    model = create_model()
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_acc', verbose=1, save_best_only=True, mode='max',period=1)

    datagen = ImageDataGenerator(rescale = 1.0 / 255.0,  
                                 rotation_range=10, width_shift_range=0.2, height_shift_range=0.2,
                                 zoom_range=0.2,shear_range=20,
                                 validation_split=0.2)

    training_set = datagen.flow_from_directory(image_path, classes=classes, target_size=(64, 64), 
                                               color_mode='grayscale', batch_size=32, shuffle=True,
                                               subset="training")
    validation_set = datagen.flow_from_directory(image_path, classes=classes, target_size=(64, 64), 
                                               color_mode='grayscale', batch_size=32, shuffle=True,
                                               subset="validation")

    history = model.fit_generator(training_set,
                                  validation_data=validation_set,
                                  epochs=epochs, verbose=1, callbacks=[ checkpoint ])
    
train()


# In[41]:


def load_trained_model(weightfile):
    from keras.models import load_model
    model = load_model(weightfile)
    return model


# In[42]:


trained_model = load_trained_model("sample_weights.hdf5")


# In[45]:


import cv2
import numpy as np
image = cv2.imread("capture_data/forward/Groot1529091688.png", 0)
image = np.array([ image.reshape(64, 64, 1) ])
print(classes[trained_model.predict_classes(image)[0]])

