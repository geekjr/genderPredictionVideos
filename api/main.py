from __future__ import print_function
from PIL import Image
import tensorflow as tf
import numpy as np
from io import BytesIO
import uvicorn
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

model = None


def read_image(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    image.save('file.png')
    return image


def predict(image: Image.Image):
    path = 'file.png'
    class_names = ['female', 'male']
    img_height = 398
    img_width = 309
    img = tf.keras.preprocessing.image.load_img(
        path, target_size=(img_height, img_width))

    image_array = tf.keras.preprocessing.image.img_to_array(img)

    image_array = tf.expand_dims(image_array, 0)

    model = tf.keras.models.load_model('gender.h5')

    predicitons = model.predict(image_array)

    score = tf.nn.softmax(predicitons[0])

    print("There is a {} chance the image belongs to {}. ".format(
        100 * np.max(score), class_names[np.argmax(score)]))

    return [class_names[np.argmax(score)], 100 * np.max(score)]


@app.post("/predict")
async def predict_api(file: UploadFile = File(...)):
    image = read_image(await file.read())
    prediction = predict(image)

    return prediction


if __name__ == "__main__":
    uvicorn.run(app, port=3600, debug=True)
