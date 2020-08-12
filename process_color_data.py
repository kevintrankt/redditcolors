from PIL import Image, ImageDraw
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import pickle
import math
import colorsys

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

    image_colors_list = []
    for key in image_colors:
        if type(key) is tuple:
            # remove 4th tuple value
            if len(key) > 3:
                rgb = key[:3]
            else:
                rgb = key
            for i in range(0, image_colors[key]):
                image_colors_list.append(rgb)

    with open('image_colors_list.pkl', 'wb') as f:
        pickle.dump(image_colors_list, f)

else:
    with open('image_colors.pkl', 'rb') as f:
        image_colors = pickle.load(f)
    with open('image_colors_list.pkl', 'rb') as f:
        image_colors_list = pickle.load(f)

print(image_colors_list)
print(len(image_colors_list))


# print(image_colors)

# image_dim = math.floor(math.sqrt(len(image_colors)))
# im = Image.new("RGB", (image_dim,image_dim), "white")
#
#
# im.show()
