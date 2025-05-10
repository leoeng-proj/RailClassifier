import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

augmentor = ImageDataGenerator(
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    brightness_range=[0.8, 1.2],
    horizontal_flip=True,
    fill_mode='wrap'
)
source_dir = 'C:/Users/apoll/Desktop/pxfclassify/data/rails/sorted/extreme wear'
save_dir = 'C:/Users/apoll/Desktop/pxfclassify/data/rails/sorted/extreme wear/augmented'

target_total = 500 - len(os.listdir(source_dir)) # balance it to match other classes
total_augments_per_image = target_total//len(os.listdir(source_dir))
# total_augments_per_image = 1
for file in os.listdir(source_dir):
    img_path = os.path.join(source_dir, file)
    if not os.path.isfile(img_path):  # checks if the "file" is a file
        continue
    if not os.path.splitext(file)[1] in [".jpg", ".jpeg", ".png"]:  # checks if the file is an image
        continue
    img = load_img(img_path)
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)
    # Generate and save new images
    for i in range(total_augments_per_image):
        gen = augmentor.flow(x, batch_size=1, save_to_dir=save_dir,
                             save_prefix='aug', save_format='jpeg')
        next(gen)
