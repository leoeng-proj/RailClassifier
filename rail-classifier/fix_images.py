import tensorflow as tf
from tensorflow import keras
from PIL import ImageFile
from PIL import Image, UnidentifiedImageError
import os
from tensorflow.keras.utils import load_img

source_folder = "C:/Users/apoll/Desktop/pxfclassify/data/rails/unsorted"  # Change to your image root folder
fixed = 0
skipped = 0
ImageFile.LOAD_TRUNCATED_IMAGES = True
for root, _, files in os.walk(source_folder):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg")):
            path = os.path.join(root, file)
            try:
                img = Image.open(path)
                img.load()  # Load the image fully (forces error detection)
                img.save(path, format=img.format, quality=95)  # Save over itself
                fixed += 1
            except Exception as e:
                print(f"❌ Skipped {path}: {type(e).__name__} — {e}")
                skipped += 1

print(f"\n✔️ Fixed {fixed} image(s)")
print(f"❌ Skipped {skipped} image(s)")