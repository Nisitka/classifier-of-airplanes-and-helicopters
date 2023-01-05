import keras
from keras import layers
from keras.models import load_model
import tensorflow as tf
import numpy as np

import cv2

# загрузка обученной модели
net = keras.models.load_model('network5')

image_path = 'test4.jpg'
# image_path = 'dataset/Validation/helicopters/image_00053.jpeg'

classes = ['helicopters', 'planes']

image = tf.keras.preprocessing.image.load_img(image_path)
image.show()

input_arr = tf.keras.preprocessing.image.img_to_array(image)
input_arr = cv2.resize(input_arr, (600, 400), interpolation=cv2.INTER_AREA)
input_arr = 255 - input_arr
input_arr /= 255
input_arr = np.expand_dims(input_arr, axis=0)

prediction = net.predict(input_arr)
print(prediction)
prediction = np.argmax(prediction)

print("Номер класса:", prediction)
print("Название класса:", classes[prediction])
