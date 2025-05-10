import os

input_dir = "C:/Users/apoll/Desktop/pxfclassify/data/rails/test"
for inner_dir in os.listdir(input_dir):
    if os.path.isfile(inner_dir):
        continue
    inner_dir = os.path.join(input_dir, inner_dir)
    for file in os.listdir(inner_dir):
        original = os.path.join(inner_dir, file)
        new = os.path.join(input_dir, file)
        os.replace(original, new)
    os.rmdir(inner_dir)
