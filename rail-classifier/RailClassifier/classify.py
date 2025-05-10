import numpy as np
import tensorflow as tf
import os
import sys
import PIL
from tensorflow.keras.preprocessing import image
from preprocessing import adjust_contrast, darken, clip_range
from sys import exit

#load model
if not os.path.isfile('model.keras'):
    exit(300)
tf.keras.config.enable_unsafe_deserialization()
model = tf.keras.models.load_model('model.keras', custom_objects={
    'adjust_contrast': adjust_contrast,
    'darken': darken,
    'clip_range': clip_range
})

#load and prep data
input_dir = sys.argv[1]
data = []
img_names = []
print("Preparing data...")
for file in os.listdir(input_dir):
    img_path = os.path.join(input_dir, file)
    if not os.path.isfile(img_path):    #checks if the "file" is a file
        continue
    if not os.path.splitext(file)[1] in [".jpg", ".jpeg", ".png"]: #checks if the file is an image
        continue
    img_names.append(file)
    img = image.img_to_array(image.load_img(img_path, target_size=(299,299)))
    data.append(img)

#put data into 4d array
data = np.asarray(data)
if data.size == 0:
    exit(200)

#predict
print("Predicting...")
predictions = model.predict(data, verbose=0)

#classify with predictions
print("Classifying...")
class_mapping = {0: "anomalous", 1: "extreme wear", 2: "heavy wear", 3: "min wear", 4: "new"}
output_dir = input_dir
if os.path.isdir(sys.argv[2]):
    output_dir = sys.argv[2]
for i, pred in enumerate(predictions):
    predicted_index = np.argmax(pred)
    folder_name = class_mapping[predicted_index]
    os.makedirs(os.path.join(output_dir, folder_name), exist_ok=True)  # Create folder if it doesn't exist
    source = os.path.join(input_dir, img_names[i])
    dest = os.path.join(output_dir, folder_name, img_names[i])
    os.replace(source, dest)
print("Samples classified and saved into folders.")
exit(0)