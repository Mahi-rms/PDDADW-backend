import io
import keras
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from io import BytesIO
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

def generate_pdf(data):
    pdf_bytes = None
    buffer = BytesIO()

    table_data = []
    for key, value in data.items():
        table_data.append([key, str(value)])

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.5*inch))
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    return pdf_bytes