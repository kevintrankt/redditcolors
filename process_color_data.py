from PIL import Image
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import pickle

PATH = 'resized'
files = [f for f in listdir(PATH) if isfile(join(PATH, f))]

load_backup = input('Load backup? (y/n): ')
if load_backup == 'y':
    image_colors = {}
    for file in files:
        if 'DS_Store' not in file:
            image = Image.open('resized/' + file)
            by_color = defaultdict(int)
            for pixel in image.getdata():
                by_color[pixel] += 1
            print(file + str(by_color))
            image_colors = {k: image_colors.get(k, 0) + by_color.get(k, 0) for k in set(image_colors) | set(by_color)}

    print(image_colors)
    with open('image_colors.pkl', 'wb') as f:
        pickle.dump(image_colors, f)
else:
    with open('image_colors.pkl', 'rb') as f:
        image_colors = pickle.load(f)
    print(image_colors)
