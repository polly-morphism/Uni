import numpy
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Flatten, Activation
from keras.layers import Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.optimizers import SGD
(X_train, y_train), (X_test, y_test) = cifar10.load_data()
# Розмір міні-вибірки
batch_size = 32
# Кількість класів зображень
nb_classes = 10
# Кількість епох навчання 
nb_epoch = 25
# Розмір зображення
img_rows, img_cols = 32, 32
# Кількість каналів: RGB
img_channels = 3
# Нормалізація даних
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)
# Створення нейромережевої моделі
model = Sequential()

# Перший шар згортки
model.add(Conv2D(32, (3, 3), padding='same',
                        input_shape=(32, 32, 3), activation='relu'))
# Друний шар згортки
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
# Перший шар субдискретизаії 
model.add(MaxPooling2D(pool_size=(2, 2)))
# Перший шар Dropout
model.add(Dropout(0.25))

# Третій шар згортки
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
# Четвертий шар згортки
model.add(Conv2D(64, (3, 3), activation='relu'))
# Другий шар субдисктеризації
model.add(MaxPooling2D(pool_size=(2, 2)))
# Другий шар Dropout
model.add(Dropout(0.25))
# Шар перетворення вхідних даних 
model.add(Flatten())
# Повнозв’язний шар
model.add(Dense(512, activation='relu'))
# Третій шар Dropout
model.add(Dropout(0.5))
# Вихідний шар 
model.add(Dense(nb_classes, activation='softmax'))
# Параметри оптимізації
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])
%%time

# Навчання  моделі
model.fit(X_train, Y_train,
              batch_size=batch_size,
              epochs=nb_epoch,
              validation_split=0.1,
              shuffle=True,
              verbose=2)
# Оцінка якості навчання на тестових даних
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Accuracy on test data: %.2f%%" % (scores[1]*100))
# Збереження моделі
model.save('my_model.h5')
numpy.savez('test_data.npz', X_test=X_test, y_test=y_test)




import numpy as np
from keras.utils import np_utils
from keras.models import load_model
%matplotlib inline
import matplotlib.pyplot as plt
data = np.load('test_data.npz')
X_test = data['X_test']
y_test = data['y_test']
model = load_model('my_model.h5')    
for i in range(9):
    plt.subplot(350 + 1 + i) #\
    plt.imshow(X_test[i], interpolation='bicubic')
plt.show()
plt.imshow(X_test[1], interpolation='bicubic')
plt.show()

X_test = X_test.astype('float32')
X_test /= 255

Y_test = np_utils.to_categorical(y_test, 10)

labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
counter_label
