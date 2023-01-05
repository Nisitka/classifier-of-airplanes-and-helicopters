from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.models import Model
import scipy

import os
currentDir = os.getcwd()

# Размер изображений
img_width, img_height = 600, 400
# Путь к каталогу с изображениями для обучения
train_data_dir = currentDir + '\\dataset\\Train'  # dataset/Train'
# Путь к каталогу с изображениями для валидации
validation_data_dir = currentDir + '\\dataset\\Validation'  # 'dataset/Validation'
# Количество изображений для обучения
nb_train_samples = 7798
# Количество изображений для валидации
nb_validation_samples = 3952
# Количество эпох
epochs = 1
# Размер выборки
batch_size = 4

# Загружаем сеть VGG16 без части, которая отвечает за классификацию
base_model = applications.VGG16(weights='imagenet', include_top=False)

# Добавляем слои классификации
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
# Выходной слой с двумя нейронами для классов "верталет" и "самолет"
predictions = Dense(2, activation='softmax')(x)

# Составляем сеть из двух частей
model = Model(inputs=base_model.input, outputs=predictions)

# "Замораживаем" сверточные уровни сети VGG16
# Обучаем только вновь добавленные слои
for layer in base_model.layers:
    layer.trainable = False

# Компилируем модель
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

# Создаем генератор данных для обучения
datagen = ImageDataGenerator(rescale=1. / 255)
train_generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode= 'categorical')

# Создаем генератор данных для валидации
validation_generator = datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode= 'categorical')

# Обучаем модель с помощью генератора
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples)

print("Сохраняем сеть")
# Сохраняем сеть для последующего использования
# Генерируем описание модели в формате json
model_json = model.to_json()
json_file = open("vgg16_planes_helicopters.json", "w")
# Записываем архитектуру сети в файл
json_file.write(model_json)
json_file.close()
# Записываем данные о весах в файл
model.save_weights("vgg16_planes_helicopters.h5")
model.save('network6')  # Сохранение модели
print("Сохранение сети завершено")