import praw
import sys
import json
import re
import requests
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
from resizeimage import resizeimage
import colorgram
import numpy as np


def createImage(list_of_RGB):
    pixels = [
        list_of_RGB,
    ]

    # Convert the pixels into an array using numpy
    array = np.array(pixels, dtype=np.uint8)

    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(array)
    return new_image


if __name__ == "__main__":
    SUBREDDIT = 'PlaydeadsInside'
    DOWNLOAD_LIMIT = 100
    VERBOSE = True
    TIME_FILTER = "all"
    MAX_WIDTH = 350
    TOTAL_PALETTES = 10
    INT_PALETTES = 10

    SKIP_DOWNLOAD = True
    SKIP_RESIZE = True

    DONT_USE_RESIZE = False

    MIN_HSL_LIGHTNESS = 0
    MIN_HSL_SATURATION = 0

    # open config containing reddit client id & secret
    with open('config.json') as f:
        config = json.load(f)

    # initialize reddit session
    reddit = praw.Reddit(client_id=config['client_id'],
                         client_secret=config['client_secret'],
                         user_agent="Reddit Top Downloader")

    # terrible way to make directories lol
    try:
        os.mkdir(SUBREDDIT)
    except:
        pass

    try:
        os.mkdir(SUBREDDIT + '/resized/')
    except:
        pass

    try:
        os.mkdir(SUBREDDIT + '/raw_downloads/')
    except:
        pass

    if not SKIP_DOWNLOAD:
        # download top posts to {subreddit}/raw_downloads
        submissions = reddit.subreddit(SUBREDDIT).top(limit=DOWNLOAD_LIMIT, time_filter=TIME_FILTER)
        count = 0
        for submission in submissions:
            count += 1
            file_name = re.findall("\\w+\\.png$|\\w+\\.jpg$", submission.url)
            if len(file_name) > 0:
                if VERBOSE:
                    print(str(count) + ': Downloading ' + submission.url)
                try:
                    r = requests.get(submission.url, allow_redirects=True)
                    open(SUBREDDIT + '/raw_downloads/' + file_name[0], 'wb').write(r.content)
                except:
                    print('error')

    files = [f for f in listdir(SUBREDDIT + '/raw_downloads') if isfile(join(SUBREDDIT + '/raw_downloads', f))]

    # resize images to {subreddit}/resized
    if not SKIP_RESIZE:
        for file in files:
            if 'DS_Store' not in file:
                with open(SUBREDDIT + '/raw_downloads/' + file, 'r+b') as f:
                    with Image.open(f) as image:
                        try:
                            cover = resizeimage.resize_cover(image, [MAX_WIDTH, MAX_WIDTH])
                            cover.save(SUBREDDIT + '/resized/' + file, image.format)
                            if VERBOSE:
                                print('Resized: ' + file)
                        except:
                            print('Skipped: ' + file)

    # generate color palette for each image
    if DONT_USE_RESIZE:
        folder = '/raw_downloads/'
    else:
        folder = '/resized/'
        files = [f for f in listdir(SUBREDDIT + '/resized') if isfile(join(SUBREDDIT + '/resized', f))]

    all_colors = []
    for file in files:
        if 'DS_Store' not in file:
            if VERBOSE:
                print('Getting colors for ' + file)
            colors = colorgram.extract(SUBREDDIT + folder + file, INT_PALETTES)
            for color in colors:
                if color.hsl.l > MIN_HSL_LIGHTNESS and color.hsl.s > MIN_HSL_SATURATION:
                    all_colors.append(color)
    all_colors = list(map(lambda x: (x.rgb.r, x.rgb.g, x.rgb.b), all_colors))

    # create image for all colors
    all_colors_image = createImage(all_colors)
    all_colors_image.save(SUBREDDIT + '/all_colors.png')

    # create palette from all colors
    colors = colorgram.extract(SUBREDDIT + '/all_colors.png', TOTAL_PALETTES)
    result = map(lambda x: (x.rgb.r, x.rgb.g, x.rgb.b), colors)
    final_palette = list(result)
    final_palette_image = createImage(final_palette)
    final_palette_image.save(SUBREDDIT + '/final_palette.png')
