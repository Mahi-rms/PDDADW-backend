import requests
import io
import keras
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import numpy as np
import cv2
p_model=keras.models.load_model('./MODELS/PN_MODEL')
t_model=keras.models.load_model('./MODELS/TB_MODEL')
""" r=requests.get("https://demo.storj-ipfs.com/ipfs/QmdBEhjTNExiTvnLgAD5EHz6Ygf1rFnnUpXy9sKbYe7z7D",stream=True, verify=False, 
                headers={"Accept-Encoding": "identity"}) """
def gray_to_rgb(file):
    gray_image = np.frombuffer(file, np.uint8)
    gray_image = cv2.imdecode(gray_image, cv2.IMREAD_GRAYSCALE)
    rgb_image = np.zeros((gray_image.shape[0], gray_image.shape[1], 3), dtype=np.uint8)
    rgb_image[:, :, 0] = gray_image
    rgb_image[:, :, 1] = gray_image
    rgb_image[:, :, 2] = gray_image
    _, encoded_image = cv2.imencode('.png', rgb_image)
    byte_stream = io.BytesIO(encoded_image)
    return Image.open(byte_stream)

def pneumonia_detection(file):
    img = gray_to_rgb(file)
    target_size=(64,64)
    test_image = img.resize(target_size)
    test_image = tf.keras.utils.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = p_model.predict(test_image)
    if result[0][0] == 0:
        prediction = 'Negative (Normal)'
    else:
        prediction = 'Positive (Pneumonia)'
    return prediction

def tuberculosis_detection(file):
    img = gray_to_rgb(file)
    target_size=(28,28)
    test_image = img.resize(target_size)
    test_image = tf.keras.utils.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = t_model.predict(test_image)
    if result[0][0] == 0:
        prediction = 'Negative (Normal)'
    else:
        prediction = 'Positive (Tuberculosis)'
    return prediction