from keras import models  
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Activation  
from keras_visualizer import visualizer  

model = models.Sequential()
model.add(Dense(10, input_shape=(27,1)))
model.add(Activation('tanh'))
model.add(Dense(5))
model.add(Activation('relu'))
model.add(Dense(5))
model.add(Activation('tanh'))
model.add(Dense(10))
model.add(Activation('tanh'))
model.add(Dense(27, input_shape=(27,1)))
model.add(Activation('relu'))

visualizer(model, format='png', view=True)
