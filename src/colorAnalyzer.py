from sklearn.cluster import KMeans
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
from colorthief import ColorThief

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_top_colors(image, number_of_colors, show_chart):
    
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    
    counts = Counter(labels)
    
    center_colors = clf.cluster_centers_
    ordered_colors = [center_colors[i]/255 for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]*255) for i in counts.keys()]
    rgb_colors = [ordered_colors[i]*255 for i in counts.keys()]
    return rgb_colors

def get_unique_colors(imagePath):
    # image = get_image(imagePath)
    # b,g,r = cv2.split(image)
    # out_in_32U_2D =  np.int32(b) << 16 + np.int32(g) << 8 + np.int32(r)
    # out_in_32U_1D= out_in_32U_2D.reshape(-1)
    # np.unique(out_in_32U_1D)
    # return len(np.unique(out_in_32U_1D))
    color_thief = ColorThief(imagePath)
    dominant_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=6)
    print(dominant_color)
    print(palette)

def printTopRGB(imagePath):
    colors = get_top_colors(get_image(imagePath), 8, True)
    return colors

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--imagePath', default='N/A')
    args = parser.parse_args()
    # printRGB(args.imagePath)
    # get_unique_colors(args.imagePath)
    get_unique_colors(args.imagePath)
