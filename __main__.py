import __utils__
import numpy as np
import tensorflow as tf
import cv2
import time

from PIL import Image as PILImage
from __config__ import CONFIG_PATH

try:
    from configparser import ConfigParser
except ImportError:
    from configparser import SafeConfigParser as ConfigParser

config_file: ConfigParser = ConfigParser()
config_file.read(CONFIG_PATH)

CLASS_LABELS = ['Healthy', 'Sick']
TARGET_SIZE = (256, 256)
PHOTO_DIR = "photos"

def extract_plant_photo(plant_id):
    result = __utils__.get_last_photo(plant_id)
    if result is None:
        return None

    photo_bytes = result[0]  # <-- questo è il vero contenuto della foto
    file_bytes = np.asarray(bytearray(photo_bytes), dtype=np.uint8)
    image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image_bgr is None:
        raise ValueError("Impossibile decodificare l'immagine dal database")

    return image_bgr

def preprocess_image_cv2(image_bgr):
    if image_bgr is None:
        raise ValueError("Immagine non valida o vuota")
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    image = PILImage.fromarray(image_rgb, 'RGB')
    image = image.resize(TARGET_SIZE)
    img_array = np.array(image).astype('float32')
    img_array = np.expand_dims(img_array, axis=0)
    return tf.convert_to_tensor(img_array, dtype=tf.float32)

def check_plant_photo(plant_id, infer_fn, image_path):
    try:
        img_tensor = preprocess_image_cv2(image_path)
        output = infer_fn(img_tensor)
        prediction_value = list(output.values())[0].numpy()[0][0]

        predicted_label = CLASS_LABELS[int(prediction_value > 0.5)]
        print(f"[DEBUG]Plant ({plant_id}) Probabilità Sick: {prediction_value:.2f}, Probabilità Healthy: {1 - prediction_value:.2f}")

        return predicted_label
    except Exception as e:
        print(f"[ERROR] Failed to process image {image_path}: {e}")
        return None

if __name__ == "__main__":
    cnn_no_aug_model = tf.saved_model.load("cnn_no_aug")
    infer_fn = cnn_no_aug_model.signatures["serving_default"]

    while True:
        plants = __utils__.get_plants()
        for plant in plants:
            id = plant["plantId"]
            current_status = plant["status"]
            image_bgr = extract_plant_photo(id)
            prediction = check_plant_photo(id, infer_fn, image_bgr)

            if prediction != current_status:
                __utils__.patch_plant(id, current_status, prediction)
        time.sleep(3600)
    
