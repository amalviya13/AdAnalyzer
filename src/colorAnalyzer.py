from sklearn.cluster import KMeans
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
from colorthief import ColorThief
from skimage.color import rgb2lab, deltaE_cie76
from matplotlib.colors import rgb2hex
from colorAnalyzer import *
import os
import webcolors
from scipy.spatial import KDTree

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

def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--imagePath', default='N/A')
    args = parser.parse_args()
    print(get_top_colors(args.imagePath)) #Answers for top colors change each iteration but also gives weightage
    print(get_dominant_color(args.imagePath)) #Most dominant color
    print(get_pallete_colors(args.imagePath)) #Returns top 8 colors - seems more accurate than get_top_colors
