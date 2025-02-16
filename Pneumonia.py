import os
import sys
sys.path.append(os.path.dirname(__file__))

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

def predictPneumonia(upload_image):
    model = load_model(r'Ai-Models\my_modelv.2.keras')  # Use raw string
    img_path = upload_image  # Path to the image

    img = image.load_img(img_path, target_size=(224, 224), color_mode='grayscale') # Load the image
    img_array = image.img_to_array(img) # Convert image to numpy array
    img_array = np.expand_dims(img_array, axis=0) # Convert single image to a batch.
    img_array = img_array / 255.0 # Normalize the image

    # Make the prediction
    prediction = model.predict(img_array)

    # return the result
    if prediction[0] > 0.5:
        return "The image is classified as PNEUMONIA (Not Healthy)."
    else:
        return "The image is classified as NORMAL (Healthy)."