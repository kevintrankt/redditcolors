import colorgram
from os import listdir
from os.path import isfile, join
import pickle

PATH = 'resized'
files = [f for f in listdir(PATH) if isfile(join(PATH, f))]

all_colors = []
for file in files:
    if 'DS_Store' not in file:
        print(file)
        colors = colorgram.extract(PATH + '/' + file, 10)
        for color in colors:
            all_colors.append(color)

# all_colors = sorted(all_colors, key=lambda c: c.hsl.h)
print(len(all_colors))

print(all_colors)

result = map(lambda x: (x.rgb.r, x.rgb.g, x.rgb.b), all_colors)

extracted_colors = list(result)

print(extracted_colors)

with open('extract_colors.pkl', 'wb') as f:
    pickle.dump(extracted_colors, f)
