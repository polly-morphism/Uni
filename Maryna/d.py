from keras.models import Model, Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Activation  
from keras_visualizer import visualizer 
from keras.layers  import Input, Dense 
from keras import regularizers
from keras import models, layers  


#model = Sequential()
#model.add(Dense(10, input_shape=(27,),  activation='tanh'))
#model.add(Dense(5, activation='relu'))
#model.add(Dense(5, activation='tanh'))
#model.add(Dense(10, activation='tanh'))
#model.add(Dense(27, activation='relu'))
#model.summary()
#model.build()
#model.summary()
model = models.Sequential([
 #   layers.Input(shape=(27,)),
    layers.Dense(10, activation='tanh', input_shape=(27,), activity_regularizer=regularizers.l1(10e-5)),
    layers.Dense(5, activation='relu'),
    layers.Dense(5, activation='tanh'),  
    layers.Dense(10, activation='tanh'),
    layers.Dense(27, activation='relu'),
    #layers.Dense(32),  
    #layers.Dense(9, activation='sigmoid')
])  

visualizer(model, format='png', view=True)



