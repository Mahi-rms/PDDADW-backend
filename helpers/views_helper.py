import requests
import io
import keras
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import numpy as np
p_model=keras.models.load_model('./MODELS/PN_MODEL')
t_model=keras.models.load_model('./MODELS/TB_MODEL')
""" r=requests.get("https://demo.storj-ipfs.com/ipfs/QmdBEhjTNExiTvnLgAD5EHz6Ygf1rFnnUpXy9sKbYe7z7D",stream=True, verify=False, 
                headers={"Accept-Encoding": "identity"}) """

def gray_to_rgb(file):
    gray_image = Image.open(io.BytesIO(file)).convert("L")
    rgb_image = Image.new("RGB", gray_image.size)
    for x in range(gray_image.width):
        for y in range(gray_image.height):
            gray_value = gray_image.getpixel((x, y))
            rgb_image.putpixel((x, y), (gray_value, gray_value, gray_value))
    
    return rgb_image

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