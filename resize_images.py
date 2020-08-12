from PIL import Image
from resizeimage import resizeimage
from os import listdir
from os.path import isfile, join

PATH = 'downloads'
files = [f for f in listdir(PATH) if isfile(join(PATH, f))]

for file in files:
    with open('downloads/' + file, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [50, 50])
            cover.save('resized/' + file, image.format)
    print(file)
