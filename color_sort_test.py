import random
from PIL import Image, ImageDraw
import colorsys
import numpy as np
import pickle
import colorgram


with open('extract_colors.pkl', 'rb') as f:
    image_colors_list = pickle.load(f)


print(image_colors_list)
pixels = [
   image_colors_list,
]

# Convert the pixels into an array using numpy
array = np.array(pixels, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array)
new_image.save('test.png')

colors = colorgram.extract('test.png', 8)
result = map(lambda x: (x.rgb.r, x.rgb.g, x.rgb.b), colors)
final_palette = list(result)

print(final_palette)

pixels = [
   final_palette,
]

# Convert the pixels into an array using numpy
array = np.array(pixels, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array)
new_image.show()
new_image.save('battlestations.png')
