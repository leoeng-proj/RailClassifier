from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.layers import Lambda
from tensorflow.keras.models import Sequential
import tensorflow as tf

def adjust_contrast(x):
    return tf.image.adjust_contrast(x, 1.5)

def darken(x):
    return tf.image.adjust_brightness(x, -0.3)

def clip_range(x):
    return tf.clip_by_value(x, 0.0, 1.0)