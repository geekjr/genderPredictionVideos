import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.data.ops.dataset_ops import AUTOTUNE

class_names = ["female", "male"]

img_height = 398
img_width = 309

img = keras.preprocessing.image.load_img(
    'image.jfif', target_size=(img_height, img_width))

image_array = keras.preprocessing.image.img_to_array(img)
image_array = tf.expand_dims(image_array, 0)

model = tf.keras.models.load_model('gender.h5')

predicitons = model.predict(image_array)

score = tf.nn.softmax(predicitons[0])

print("There is a {} chance the image belongs to {}. ".format(
    100 * np.max(score), class_names[np.argmax(score)]))
