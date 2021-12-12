from keras import models, layers  
from keras_visualizer import visualizer  

model = models.Sequential([  
    layers.Input(shape=(27,1)),  
    layers.Dense(6, activation='softmax'),  
    layers.Dense(32),  
    layers.Dense(9, activation='sigmoid')])  

visualizer(model, format='png', view=True)
