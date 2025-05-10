import os
import sys
import pickle
import numpy as np
from skimage.io import imread
from skimage.transform import resize

#os.getenv()

#load model
if not os.path.isfile('model.p'):
    exit(300)
with open('model.p', 'rb') as file:
    model = pickle.load(file)
    
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
    img = imread(img_path)
    img = resize(img, (15, 15))
    data.append(img.flatten())
data = np.asarray(data)

if data.size == 0:
    exit(200)
# Predict class labels
print("Predicting...")
predictions = model.predict(data)

# Map class labels to folder names
folder_mapping = {0: "empty", 1: "not_empty"}

# Organize samples into folders
print("Classifying...")
output_dir = input_dir
if os.path.isdir(sys.argv[2]):
    output_dir = sys.argv[2]

for i, pred in enumerate(predictions):
    folder_name = folder_mapping[pred]
    os.makedirs(os.path.join(output_dir, folder_name), exist_ok=True)  # Create folder if it doesn't exist
    source = os.path.join(input_dir, img_names[i])
    dest = os.path.join(output_dir, folder_name, img_names[i])
    os.replace(source, dest)
print("Samples classified and saved into folders.")
exit(0)