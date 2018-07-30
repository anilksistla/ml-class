from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.utils import np_utils

import wandb
from wandb.keras import WandbCallback

# logging code
run = wandb.init()
config = run.config

# load data
(X_train, y_train), (X_test, y_test) = mnist.load_data()

img_width = X_train.shape[1]
img_height = X_train.shape[2]

# normalize the training and test data
X_train = X_train.astype("float32")/255.
X_test = X_test.astype("float32")/255.

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
labels = range(10)

num_classes = y_train.shape[1]

# create model
model=Sequential()
model.add(Flatten(input_shape=(img_width,img_height))) # first layer image flattening
#model.add(Dense(num_classes))
model.add(Dense(num_classes, activation="softmax")) # activation function
# model.compile(loss='mse', optimizer='adam',
model.compile(loss='categorical_crossentropy', optimizer='adam',
                metrics=['accuracy']) # loss function. 

# Fit the model
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test),
                    callbacks=[WandbCallback(validation_data=X_test, labels=labels)])


