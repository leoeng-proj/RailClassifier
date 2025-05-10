from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.layers import Lambda
from tensorflow.keras.models import Sequential
import tensorflow as tf
import matplotlib as plt

def adjust_contrast(x):
    return tf.image.adjust_contrast(x, 1.5)

def darken(x):
    return tf.image.adjust_brightness(x, -0.3)

def clip_range(x):
    return tf.clip_by_value(x, 0.0, 1.0)

def main():
    preprocessing = Sequential([
        tf.keras.layers.Rescaling(1. / 255),
        tf.keras.layers.Lambda(adjust_contrast),
        tf.keras.layers.Lambda(darken),
        tf.keras.layers.Lambda(clip_range)
    ])
    # Load image (299x299 to match model input)
    img_path = 'C:/Users/apoll/Desktop/pxfclassify/data/rails/sorted/extreme wear/SomeTrack_SomeLine_20250425_153242_0000_1701154.jpeg'
    img = load_img(img_path, target_size=(299, 299))
    img_array = img_to_array(img)
    img_array = tf.convert_to_tensor(img_array[tf.newaxis, ...])  # Add batch dimension

    # Apply preprocessing
    processed = preprocessing(img_array)

    # Show original and processed side-by-side
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(img)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title("Preprocessed")
    plt.imshow(tf.squeeze(processed).numpy())
    plt.axis('off')
    plt.show()