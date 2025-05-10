import tensorflow as tf
import numpy as np
from tensorflow import keras
from sklearn.utils import class_weight
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from tensorflow.keras.utils import load_img, image_dataset_from_directory
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout, Input, Conv2D, MaxPool2D, Rescaling, RandomFlip, RandomRotation, RandomZoom, RandomTranslation, RandomContrast, BatchNormalization, GlobalAveragePooling2D, Lambda
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from preprocessing import adjust_contrast, darken, clip_range

#establish train and validation directories
train_ds = image_dataset_from_directory(
    'C:/Users/apoll/Desktop/pxfclassify/data/rails/sorted',                      # root folder containing class subfolders
    validation_split=0.2,          # 20% of data goes to validation
    subset="training",
    seed=123,                      # for reproducibility
    image_size=(299, 299),         # resize images to this shape
    batch_size=16
)
val_ds = image_dataset_from_directory(
    'C:/Users/apoll/Desktop/pxfclassify/data/rails/sorted',
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(299, 299),
    batch_size=16
)

#establish class weights as some classes will have far less data than others
labels = []
for _, label in train_ds:
    labels.extend(label.numpy())
labels = np.array(labels)
class_weights_array = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(labels),
    y=labels
)
class_weights = dict(enumerate(class_weights_array))
print(class_weights)

num_classes = 5  # update if different
def one_hot_encode(image, label):
    return image, tf.one_hot(label, depth=num_classes)
train_ds = train_ds.map(one_hot_encode)
val_ds = val_ds.map(one_hot_encode)

#preprocessing
preprocessing = Sequential([
    Rescaling(1. / 255),
    Lambda(adjust_contrast),
    Lambda(darken),
    Lambda(clip_range)
])
data_augmentation = Sequential([
    RandomFlip("horizontal"),
    RandomZoom(0.2),
    RandomTranslation(0.2, 0.2),
    RandomContrast(0.1)
])

#build model
model = Sequential([
    # data_augmentation,
    preprocessing,
    Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same'),
    MaxPool2D(2, 2),
    Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'),
    MaxPool2D(2, 2),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.7),
    Dense(5, activation='softmax')
])
# tf.keras.config.enable_unsafe_deserialization()
# model = tf.keras.models.load_model("model.keras", custom_objects={
#     'adjust_contrast': adjust_contrast,
#     'darken': darken,
#     'clip_range': clip_range
# })
model.summary()
model.compile(loss='categorical_crossentropy', #labels are either 1 or 0
             optimizer='adam',
              metrics=['acc']) #tracks accuracy during training/validation



#checkpoint the best model
checkpoint = ModelCheckpoint(
    filepath='model.keras',       # or 'best_model.h5'
    monitor='val_loss',
    mode='min',
    save_best_only=True,
    verbose=1,
    save_freq = 'epoch'
)

#train model
history = model.fit(
    train_ds,
    epochs=15,
    verbose=1,
    validation_data=val_ds,
    class_weight=class_weights,
    callbacks = [checkpoint]
)

#confusion matrix
# model = tf.keras.models.load_model("model.keras")
# y_true = []
# y_pred = []
# for images, labels in val_ds:
#     preds = model.predict(images)
#     y_true.extend(labels.numpy())
#     y_pred.extend(np.argmax(preds, axis=1))
# y_true = np.array(y_true)
# y_pred = np.array(y_pred)
# cm = confusion_matrix(y_true, y_pred)
# disp = ConfusionMatrixDisplay(confusion_matrix=cm)
# disp.plot(cmap='Blues', xticks_rotation=45)
# plt.title("Confusion Matrix")
# plt.show()