import numpy as np
import matplotlib.pyplot as plt
import datapipe as dp
from sklearn.model_selection import train_test_split
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Activation, Convolution2D, Cropping2D, Dense, Dropout
from keras.layers import Flatten, Lambda, MaxPooling2D

DATA_PATH       = './data'
CSV_FILENAME    = '/driving_log.csv'

ACTIVATION_FUNC = 'tanh'
LOSS_FUNC       = 'mse'
LEARNING_RATE   = 1e-4
BATCH_SIZE      = 128
NUM_EPOCH       = 3


samples = dp.read_data_csv(DATA_PATH, CSV_FILENAME)
train_samples, validation_samples = train_test_split(samples, test_size=0.2)

SAMPLE_PER_EPOCH = len(train_samples) * 3

# compile and train the model using the generator function
train_gen = dp.sample_generator(train_samples, DATA_PATH, batch_size=BATCH_SIZE)
validation_gen = dp.sample_generator(validation_samples, DATA_PATH, batch_size=BATCH_SIZE, augment_enable=false)

def build_model():
	""" 
	Building the model for the behavioral cloning net.
	Model is based on Nvidia's
	"End to End Learning for Self-Driving Cars" paper
	"""
	model = Sequential()
	# Normalize the data
	model.add(Lambda(lambda x: x / 255.0 - 0.5, input_shape=(160, 320, 3)))
	# Crop the data 
	model.add(Cropping2D(cropping=((70, 25), (0,0))))
	# Convolution layers
	model.add(Convolution2D(24, 5, 5, subsample=(2, 2), activation=ACTIVATION_FUNC))
	model.add(Convolution2D(36, 5, 5, subsample=(2, 2), activation=ACTIVATION_FUNC))
	model.add(Convolution2D(48, 5, 5, subsample=(2, 2), activation=ACTIVATION_FUNC))
	model.add(Convolution2D(64, 3, 3, subsample=(1, 1), activation=ACTIVATION_FUNC))
	model.add(Convolution2D(64, 3, 3, subsample=(1, 1), activation=ACTIVATION_FUNC))
	# Fully-connected layers
	model.add(Flatten())
	model.add(Dense(100))
	model.add(Dense(50))
	model.add(Dense(10))
	model.add(Dense(1))

	model.compile(optimizer=Adam(lr=LEARNING_RATE), loss=LOSS_FUNC)
	return model

model = build_model()
model.fit_generator(train_gen, samples_per_epoch= \
            SAMPLE_PER_EPOCH, validation_data=validation_gen, \
            nb_val_samples=len(validation_samples), nb_epoch=NUM_EPOCH)

model.save('model.h5')
