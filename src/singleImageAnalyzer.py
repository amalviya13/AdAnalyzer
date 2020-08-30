from sklearn.cluster import KMeans
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np
import cv2
import colorsys
from collections import Counter
import os
from colorthief import ColorThief
from matplotlib.colors import rgb2hex
from colorAnalyzer import *
import webcolors
from scipy.spatial import KDTree
from PIL import Image

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def top_colors(image, number_of_colors, show_chart):
    
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)

    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    ordered_colors = [center_colors[i]/255 for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]*255) for i in counts.keys()]
    rgb_colors = [ordered_colors[i]*255 for i in counts.keys()]
    colorList = []
    for rgb in rgb_colors:
        colorList.append(closest_color(rgb))
    return colorList

def weightedColors(imagePath):
    colorDict = {}
    im = Image.open(imagePath)
    im = im.resize((200, 200))
    width, height = im.size
    for x in range(0,width,2):
        for y in range(0,height,2):
            close_color = closest_color(im.getpixel((x,y)))
            if close_color in colorDict:
                colorDict[close_color] = colorDict[close_color] + 1
            else:
                colorDict[close_color] = 1
    visualizeResults(colorDict)
    return sorted(colorDict.items(), key=lambda x: x[1])

def get_pallete_colors(imagePath):
    color_thief = ColorThief(imagePath)
    palette = color_thief.get_palette(color_count=9)
    colorList = []
    for pal in palette:
        colorList.append(closest_color(pal))
    return colorList

def get_dominant_color(imagePath):
    color_thief = ColorThief(imagePath)
    dominant_color = color_thief.get_color(quality=1)
    return closest_color(dominant_color)

def get_top_colors(imagePath):
    colors = top_colors(get_image(imagePath), 8, True)
    return colors

def resize(path):
    im = Image.open(path)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    f, e = os.path.splitext(path)
    imResize = im.resize((200,200), Image.ANTIALIAS)
    print(imResize)
    imResize.save(f + '.jpg', 'JPEG', quality=90)

def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.CSS2_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def warm_or_cool(imagePath):
    im = Image.open(imagePath)
    im = im.resize((200, 200))
    width, height = im.size
    cool = 0
    warm = 0
    for x in range(0,width,2):
        for y in range(0,height,2):
            requestedPixel = im.getpixel((x,y))
            h, l, s = colorsys.rgb_to_hls(requestedPixel[0]/255, requestedPixel[1]/255, requestedPixel[2]/255)
            hueAngle = h * 360
            if (hueAngle > 90 and hueAngle < 270):
                cool += 1
            else:
                warm += 1
    if cool > warm:
        return "cool"
    return "warm"

def getColorPercentage(imagePath, percentage):
    topPercentColors = []
    colorDict = weightedColors(imagePath)
    pixels = 0
    for color in colorDict:
        pixels += color[1]
    pixels = pixels * (percentage/100)
    currentPixelTotal = 0
    for colors in reversed(colorDict):
        if currentPixelTotal <= pixels:
            topPercentColors.append(colors[0])
            currentPixelTotal += colors[1]
    return topPercentColors

def visualizeResults(colorDict):
	plt.figure(figsize = (8, 6))
	plt.pie(colorDict.values(), labels = colorDict.keys(), colors = colorDict.keys())
	plt.show()
    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--imagePath', default='N/A')
    args = parser.parse_args()
    # resize(args.imagePath)
    print(get_top_colors(args.imagePath)) 
    print(get_dominant_color(args.imagePath)) 
    print(get_pallete_colors(args.imagePath)) 
    print(weightedColors(args.imagePath)) 
    print(getColorPercentage(args.imagePath, 80))
    print(warm_or_cool(args.imagePath))